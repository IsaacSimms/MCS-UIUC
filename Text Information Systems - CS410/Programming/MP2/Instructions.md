## Code Files

## Overview

Retrieval-augmented generation (RAG) is a commonly used technique to improve the performance of large language models (LLMs) on many tasks. The basic idea is to first retrieval some relevant content from a collection of text documents to a problem to be solved by an LLM, and then pass the retrieved information together with the original problem to the LLM. The original motivation of RAG was to help alleviate the problem of hallucination of LLMs by providing explicit reliable text content as a way to “encourage” the LLM to pay more attention to such reliable information when generating text (otherwise, the LLM would tend to generate text solely based on the model parameters, leading to hallucination). However, later, researchers have found that the additional relevant information is generally helpful as additional context for solving a problem, leading to the rapid growth of research in RAG. Most research examined how to improve the information retrieval component in RAG with some also attempting to optimize the use of retrieved information for prompting the LLM.  RAG provides a natural integration of information retrieval techniques with LLMs. There is also another important reason why LLMs must use a retrieval system, which is that the LLMs generally do not have access to the newest information (e.g., today’s weather or sports game results), and thus an LLM must be able to leverage a search engine to retrieve such up-to-date information. In general, the integration of information retrieval techniques with LLMs is expected to become increasingly important in the future. 

If you want to learn more about RAG, you may read the following introduction article: 

Church KW, Sun J, Yue R, Vickers P, Saba W, Chandrasekar R. Emerging trends: a gentle introduction to RAG. 
Natural Language Engineering
. 2024;30(4):870-881. doi:10.1017/S1351324924000044

Here’s a useful video explaining how to implement RAG: https://www.youtube.com/watch?v=sVcwVQRHIc8
 

In this assignment, you will build, test, and extend a Retrieval-Augmented Generation (RAG) system using LangGraph, Pyserini, and Ollama. You will first reproduce a working baseline system, then enhance its usability and reasoning ability through a series of incremental tasks. This MP will help you understand how retrieval and generation components interact in a RAG pipeline and give you hands-on experience in improving retrieval effectiveness and user interaction.

## Learning Objectives

By completing this assignment, you will:

    Understand how a retrieval-augmented generation (RAG) system is structured.

    Gain experience integrating a local LLM with a document retriever.

    Learn how to evaluate and improve a RAG system’s usability and performance.

    Develop practical Python skills in LangGraph orchestration and Pyserini retrieval.

## Provided Materials

You will start from the demo code: The code contains:

    main.py — main entry point for the agent

    agent.py — defines the LangGraph pipeline

    utils/ — helper modules for retrieval, configuration, and state

    A detailed README.md for environment setup and usage

## Task 1: Reproduce the Baseline Demo (30 points)

### Goal

Set up and run the baseline RAG system using the provided instructions. Your goal is to understand how the entire end-to-end pipeline works.

### Steps

1. Follow the README.md to install dependencies and set up the environment.

2. Configure .env variables (retriever settings, model choice, etc.).

3. Build an index from the provided documents and run the demo. The demo reuses the same pipeline setup as in MP1 for data preparation and indexing.

4. Ask the system at least three questions related to the indexed content.

5. Record and analyze the responses.

Note: 

1. This demo provides a basic retriever based on the BM25 algorithm using the apnews dataset. You are welcome to modify it based on what you did in MP1.

2.  If you do not have access to a GPU, Ollama will still run in CPU mode, though generation may be noticeably slower.

### Deliverables

    Screenshots showing the system running and responding to queries.

    A short discussion addressing:    

        Which cases did the system answer well, and why?    

        Which cases did it fail on, and what might be the cause (e.g., retrieval error, hallucination, missing context)?

### Task 2: Improve User Interaction (40 points)

In Task 2, you will have an opportunity to explore RAG to improve the performance of an LLM. 

### Goal

Make the system’s retrieval and answer presentation more user-friendly so users can tell why the agent answered that way. You can choose from the list below or propose your own. Implement at least two improvements.

    Display the retrieved document or snippets before showing the generated answer.

    Highlight which passages/sentences the answer is based on.

    Add a simple scoring or ranking explanation (e.g., “Doc A – Score 1.23”).

    Use color or formatting to separate retrieved text and generated responses.

### Deliverables

    Modified code files (main.py, retriever.py, or agent.py) that implement at least two interaction-friendly improvements.

    Screenshots or terminal output showing the improved user experience.

    A short explanation of what was changed and why it improves usability.

## Task 3: Support Long Descriptive Queries (30 points)

### Goal

Extend the system to handle complex, multi-sentence user needs by enabling query decomposition and result fusion. This will help the agent retrieve more relevant evidence for broad or ambiguous questions. You can achieve this by:

    Accepting a paragraph-length description of an information need.

    Automatically generating multiple sub-queries.

    Fusing the retrieval results before passing them to the LLM.

An example can be:

Original question: “I’m learning how to build a retrieval-augmented generation agent. Could you explain the main components such as retrievers, embeddings, and vector databases, and how they work together?”

Decomposed sub-queries:

    "What are the main components of a retrieval-augmented generation system?"

    "How do retrievers, embeddings, and vector databases function individually in a RAG pipeline?"

    "How do these components interact to support retrieval and generation in a RAG agent?"

Expected effect: Each sub-query retrieves more specific evidence, which can then be combined (fused) into a single, richer context for the LLM to answer from.

Note: You may trigger the long-query branch when the input has more than 200 characters or more than one sentence.

### Suggested approach

1. Modify agent.py or retriever.py to:    

    Use the LLM to paraphrase or decompose the user description into 2–4 concise queries.    

    Retrieve top-K documents for each query.    

    Merge or re-rank the combined results.

2. Feed the merged documents into the answer-generation module.

### Deliverables

    Code implementing query generation and result fusion.

    A short report describing your method and one test example:    

        Show the long query.    

        List the generated sub-queries.    

        Show the retrieved snippets and the final answer.    

        Briefly discuss whether the new design improved result relevance.

## Submission Requirements

Please see MP2 Submission and Peer Review to submit and review others' submissions.

Items to be submitted:

1. A concise report in PDF summarizing your experiments, results, and insights.

2. Python files (e.g., with .py extension) used for implementing and running the experiments.

You should submit a single .zip containing your report PDF and your modified code.

## Grading Criteria

Task 1: Reproduce the Baseline Demo (30%)

    10%: Set up the environment and build/load the index so the agent runs without fatal errors.

    20%: Demonstrate at least three successful queries with screenshots or logs.

    30%: Analyze successful vs. failed cases and provide a plausible diagnosis.

Task 2: Improve User Interaction (40%)

    15%: Implement the first user-facing improvement.

    30%: Implement the second user-facing improvement.

    40%: Explain your design choices and compare the improved output with the baseline to show why it is more usable.

Task 3: Support Long Descriptive Queries (30%)

    10%: Enable the agent to decompose long queries into 2–4 focused sub-queries.

    20%: Retrieve and fuse results from multiple sub-queries and pass the merged context to the LLM.

    30%: Document one end-to-end example and comment on whether relevance improved.