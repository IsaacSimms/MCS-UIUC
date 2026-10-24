"""RAG REPL for CS410 MP2. Task 2 only changes what is printed."""

import logging
import re
from agent import create_agent
from utils.retriever import create_retriever
from utils.config import Config
from utils.state import GraphState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# == Snippet window == #
# Whole-word question terms, minus stopwords and tokens of two letters or fewer.
# The window starts at the earliest hit, takes 500 characters, and extends to the
# next whitespace. If no term hits, it starts at the beginning of the article.
SNIPPET_CHARS = 500  # characters from the hit, then the next whitespace
STOPWORDS = frozenset({ # prevents function words from deciding where a snippet starts
    "the", "and", "for", "was", "were", "are", "been", "what", "how", "did",
    "does", "this", "that", "when", "who", "whom", "which", "into", "over",
    "after", "before", "than", "then", "not", "from", "with", "have", "has",
    "had", "you", "your", "about", "would", "could", "should", "there",
    "their", "they", "them", "his", "her", "she", "him", "its", "also",
    "can", "may", "might",
})


def content_words(question: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z]+", question.lower())
    return [token for token in tokens if len(token) > 2 and token not in STOPWORDS]


def snippet_start(text: str, words: list[str]) -> int:
    lowered = text.lower()
    starts = []
    for word in words:
        match = re.search(rf"\b{re.escape(word)}\b", lowered)
        if match:
            starts.append(match.start())
    return min(starts) if starts else 0  # no hit: start of the article


def make_snippet(text: str, question: str) -> str:
    start = snippet_start(text, content_words(question))
    end = min(len(text), start + SNIPPET_CHARS)
    if end < len(text):
        whitespace = re.search(r"\s", text[end:])
        if whitespace:
            end = end + whitespace.start()
        else:
            end = len(text)  # no whitespace left; take the tail
    snippet = " ".join(text[start:end].split())
    if end < len(text):
        snippet += " ..."  # article continues past the window
    return snippet


# == Printed result == #
# One yellow snippet per retrieved passage, then the answer in green.
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


def print_result(question: str, result: dict) -> None:
    context = result.get("context") or []
    print(f"\n{YELLOW}Retrieved{RESET}")
    passages = []
    for item in context:
        text = item if isinstance(item, str) else str(item)
        if text.strip():
            passages.append(text)
    if not passages:
        print(f"{YELLOW}No passages were retrieved.{RESET}")
    else:
        for index, text in enumerate(passages, start=1):
            if index > 1:
                print()
            print(f"{YELLOW}{index}. {make_snippet(text, question)}{RESET}")

    if result.get("final_answer"):
        print(f"\n{GREEN}Answer{RESET}")
        print(f"{GREEN}{result['final_answer']}{RESET}")
    elif result.get("error"):
        print(f"\nError occurred: {result['error']}")  # default color
    else:
        print("\nNo answer or error was returned.")


# == REPL == #
def main():
    try:
        config = Config()
        logger.info(f"Loaded configuration: {config}")

        retriever = create_retriever()
        agent = create_agent()

        while True:
            question = input("Please enter your question (or type 'exit' to quit): ")

            if question.lower() == 'exit':
                print("Exiting the program. Goodbye!")
                break

            logger.info(f"Running agent with question: {question}")

            initial_state = GraphState(
                question=question,
                context=[],
                current_step="",
                final_answer="",
                retriever=retriever,
                web_search_tool=None,
                error=None,
                selected_namespaces=[],
                web_search_results=[]
            )

            result = agent.invoke(initial_state)
            print_result(question, result)

            print("\n" + "-" * 50 + "\n")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
