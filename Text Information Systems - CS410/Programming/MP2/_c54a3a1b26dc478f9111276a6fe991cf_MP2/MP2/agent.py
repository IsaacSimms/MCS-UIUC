"""
agent.py
=========================
LangGraph-based RAG agent for MP2.

Pipeline:
1) retrieve(state)        -> one BM25 search, or 2-4 sub-queries fused for a long question
2) generate_answer(state) -> prompts an LLM (Ollama) with the retrieved context

State keys (GraphState):
- question: str                     # user question (required)
- context: List[str]                # accumulated evidence passages
- subqueries: List[str]             # long-question search lines; empty otherwise
- retriever: Optional[BaseRetriever]# allow injection (for testing)
- final_answer: Optional[str]       # model's answer
- error: Optional[str]              # error message if any
- current_step: str                 # "retrieve" | "generate_answer"
"""

import logging
import re
from typing import List

from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate

from utils.llm import OllamaLLM
from utils.retriever import create_retriever
from utils.state import GraphState
from utils.config import Config

# ---------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()


# ---------------------------------------------------------------------
# Graph construction (entry for main.py)
# ---------------------------------------------------------------------
def create_agent():
    """
    Build and compile the LangGraph workflow:
       retrieve -> generate_answer -> END
    """
    workflow = StateGraph(GraphState)

    # Define nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate_answer", generate_answer)

    # Entry and edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate_answer")
    workflow.add_edge("generate_answer", END)

    return workflow.compile()


# ---------------------------------------------------------------------
# Long questions: decompose, search each line, fuse
# ---------------------------------------------------------------------
# More than 200 characters, or more than one sentence, uses this branch.
RRF_K = 60  # reciprocal rank fusion constant


def is_long_query(question: str) -> bool:
    text = question.strip()
    if len(text) > 200:
        return True
    parts = [part for part in re.split(r"[.!?]+", text) if part.strip()]
    return len(parts) > 1


def parse_subqueries(text: str) -> List[str]:
    queries = []
    for line in (text or "").splitlines():
        cleaned = re.sub(r"^(?:\d+[\.\)\:]\s*|[\-\*\u2022]\s+)", "", line).strip()
        if not cleaned:
            continue
        queries.append(cleaned)
        if len(queries) == 4:  # assignment cap
            break
    return queries


def decompose_query(question: str) -> List[str]:
    try:
        llm = OllamaLLM(model=config.OLLAMA_MODEL)
        prompt = ChatPromptTemplate.from_template(
            "Break the user question into 2 to 4 concise search queries.\n"
            "Cover different parts of the question. Each query is a short phrase or a single question.\n"
            "Put one query per line. Do not number the lines. Do not add any other text.\n"
            "\n"
            "Question:\n"
            "{question}\n"
            "\n"
            "Queries:"
        )
        response = (prompt | llm).invoke({"question": question})
        content = response if isinstance(response, str) else str(response)
        return parse_subqueries(content)
    except Exception:
        logger.exception("Query decomposition failed")
        return []


def search_once(retriever, query: str):
    docs = retriever.invoke(query)
    if not docs and hasattr(retriever, "base_retriever"):
        logger.info("Compression yielded 0 docs; falling back to base retriever.")
        docs = retriever.base_retriever.invoke(query)
    return docs


def fuse_subqueries(retriever, subqueries: List[str]):
    searcher = retriever.base_retriever if hasattr(retriever, "base_retriever") else retriever
    scores = {}
    best_rank = {}
    chosen = {}
    for subquery in subqueries:
        hits = searcher.invoke(subquery)  # BM25 only; compression stays on the single-query path
        for rank, doc in enumerate(hits, start=1):
            metadata = getattr(doc, "metadata", None) or {}
            docid = str(metadata.get("docid", id(doc)))
            scores[docid] = scores.get(docid, 0.0) + 1.0 / (RRF_K + rank)
            if docid not in chosen or rank < best_rank[docid]:
                chosen[docid] = doc
                best_rank[docid] = rank
    ranked = sorted(scores, key=lambda docid: (-scores[docid], best_rank[docid], docid))
    return [chosen[docid] for docid in ranked[: config.RETRIEVER_K]]


# ---------------------------------------------------------------------
# Node 1: Retrieval
# ---------------------------------------------------------------------
def retrieve(state: GraphState) -> GraphState:
    """
    Retrieve evidence passages for the given question.

    A short question uses one search. A long question is split into 2-4
    sub-queries, each searched with BM25, then fused to the top passages.
    """
    try:
        logger.info("Starting retrieval")
        state["subqueries"] = []

        query = (state.get("question") or "").strip()
        if not query:
            state["error"] = "Empty question"
            state["current_step"] = "retrieve"
            logger.warning("Retrieval aborted: empty question")
            return state

        # Allow DI for tests; otherwise create from config
        retriever = state.get("retriever") or create_retriever()

        if is_long_query(query):
            subqueries = decompose_query(query)
            if len(subqueries) >= 2:
                state["subqueries"] = subqueries
                logger.info(f"Using sub-queries: {subqueries}")
                docs = fuse_subqueries(retriever, subqueries)
            else:
                logger.info("Searching the original question once.")
                docs = search_once(retriever, query)
        else:
            docs = search_once(retriever, query)

        # Build/extend context
        ctx: List[str] = list(state.get("context") or [])
        ctx.extend([getattr(d, "page_content", str(d)) for d in docs])

        state["context"] = ctx
        state["current_step"] = "retrieve"
        logger.info(f"Retrieved {len(docs)} documents")
        return state

    except Exception as e:
        logger.exception("Error in retrieve")
        state["error"] = str(e)
        state["current_step"] = "retrieve"
        return state


# ---------------------------------------------------------------------
# Helpers for prompting
# ---------------------------------------------------------------------
def build_prompt(max_sentences: int = 7) -> ChatPromptTemplate:
    """
    Create the QA prompt.

    Notes:
    - You can experiment with different instruction styles here (e.g., chain-of-thought
      vs. concise answers, citing sources, etc.).
    """
    template = f"""You are an assistant for question answering.

Use ONLY the context below to answer the question. If the answer is not in the context, say you don't know.

Context:
{{context}}

Question:
{{question}}

Answer in at most {max_sentences} sentences, concise and to the point.
Answer:"""
    return ChatPromptTemplate.from_template(template)


# ---------------------------------------------------------------------
# Node 2: Answer generation
# ---------------------------------------------------------------------
def generate_answer(state: GraphState) -> GraphState:
    """
    Generate a concise answer using Ollama with the retrieved context.
    Safely stringifies all context items before prompting.

    Notes:
    - In Task 3, the retrieval step may store *structured* context in state["context"],
      e.g. a list like:
          [
            {"subquery": "what is RAG", "results": ["RAG is ...", "A RAG agent ..."]},
            {"subquery": "how do retrievers and vector DBs work together",
             "results": ["retriever uses embeddings ...", "vector DB stores ..."]},
            "Doc from baseline run"
          ]
      You can first turn each structured item into a text block like
          "Sub-query: ...\n---\nretrieved docs...\n---"
      in the retrieval step, which is compatible with the original format.
    """
    try:
        logger.info("Starting answer generation")

        # Initialize local LLM (Ollama)
        llm = OllamaLLM(model=config.OLLAMA_MODEL)

        ########## Prepare context string ##########
        # Flatten state["context"] into one string for the LLM.
        # If later you have multiple sub-queries, you can format them here.
        context_strings: List[str] = []
        for item in state.get("context") or []:
            context_strings.append(item if isinstance(item, str) else str(item))
        context_strings = "\n".join(context_strings)
        ###########################################

        # Build prompt and call the model
        prompt = build_prompt(max_sentences=7)
        chain = prompt | llm

        response = chain.invoke({
            "question": state.get("question", ""),
            "context": context_strings
        })

        # Update state
        state["final_answer"] = response
        state["current_step"] = "generate_answer"
        logger.info("Answer generation completed")
        return state

    except Exception as e:
        logger.error(f"Error in generate_answer: {e}")
        state["error"] = str(e)
        state["current_step"] = "generate_answer"
        return state
