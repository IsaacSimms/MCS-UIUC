# MP3: VideoRAG

The goal of this MP is to build a system that takes a video as input, lets you ask natural language questions about it, and returns answers grounded in what was actually said and shown. Think of it as giving a video a memory.

Video is one of the most common ways people learn, yet finding one answer inside a long video is slow. Video platforms and AI assistants now let users ask questions about a video, jump to the moment that answers them, and read automatically generated chapters and summaries. These features rely on video retrieval-augmented generation (VideoRAG).

In a VideoRAG system, the video is converted into text with timestamps, the text is indexed, and a language model answers each question from the retrieved moments. In MP2, you built a RAG system over text documents with LangGraph, Pyserini, and Ollama. In this assignment, you will reuse that pipeline and extend it with the parts that are specific to video: transcription with timestamps, text for what is shown on screen, questions that refer to a time, and summaries of the whole video.

This MP will help you understand how each stage of a VideoRAG system works and how to evaluate what each stage contributes.

## What Does a Minimal Pipeline Look Like?

At minimum, your pipeline should ingest a video, extract its content in some form (audio, frames, or other ways), store it in a way that supports search, and answer questions about it.

1. **Ingest:** read the video from its YouTube link.
2. **Extract:** turn speech into a transcript with timestamps, and turn what is shown on screen into text.
3. **Store:** split the timeline into clips and index each clip for search.
4. **Answer:** retrieve the clips that match a question, and have an LLM answer from them and cite their times.

We have sketched one way to do this in the provided Jupyter notebook. Feel free to change any part of it to fit your needs and goals, and explain your choices in your reflection.

## Provided Materials

- `mp3_videorag.ipynb`: a notebook that walks through the suggested pipeline in five parts, with progress check cells and evaluation code.
- The video for this MP: *How Google Translate Turns 134 Languages Into Math | WSJ Tech Behind*. The notebook reads it from its link; nothing is downloaded.
- Your MP2 setup: Pyserini (with Java 21), Ollama, and LangGraph.

If you want to learn more about VideoRAG, you may read the following paper:

Ren X, Xu L, Xia L, Wang S, Yin D, Huang C. *VideoRAG: Retrieval-Augmented Generation with Extreme Long-Context Videos*. arXiv:2502.01549, 2025. Code: HKUDS/VideoRAG.

## Submission Requirements

Please see MP3 Submission and Peer Review to submit and review others' submissions.

Items to be submitted:

- Your notebook or script with the implemented pipeline, with outputs. Include a PDF export of the notebook so reviewers can read it without running it.
- Your reflection inside the notebook (half a page is fine).

You should submit a single `.zip` containing your notebook or script and its PDF export. Do not include your API key.

## Grading Criteria

This MP should be graded on effort and understanding. We want to see that you engaged with the ideas: what you tried, what broke, and what you learned. Your system does not need to answer every question correctly.

**Minimum to pass:** a working end-to-end pipeline (Parts 0 and 1, plus the reflection). Give it a video, ask it a question, and get an answer. It does not have to be perfect; it has to reflect your learning effort.

### Part 0: Watch the Video and Write Your Questions (5%)

- 5%: Write 5 natural questions with your own answers and times.

### Part 1: Baseline VideoRAG (20%)

- 5%: Transcribe the video with an API and save a transcript with times.
- 15%: Run the baseline on your 5 questions and record verdicts and causes.
- 20%: Explain which questions worked, which failed, and why.

### Part 2: Add What Is Shown on Screen (20%)

- 5%: Generate screen descriptions and merge them into the clip text.
- 15%: Build the new index and rerun the questions the baseline missed.
- 20%: Explain where screen text helped or hurt, and your prompt choices.

### Part 3: Route Time Questions and Summary Questions (20%)

- 5%: Route questions and answer time questions from the right time window.
- 15%: Produce chapters and a summary of the whole video.
- 20%: Explain your classifier, one misrouted question, and your chapter choices.

### Part 4: Evaluation (20%)

- 5%: Record verdicts for your own questions on the full system.
- 15%: Run the course question, summary, and cost cells.
- 20%: Answer the four Part 4 questions using your results.

### Reflection (15%)

- 15%: Describe what you built, your approach, what broke, what you learned, and how you would extend the project.
