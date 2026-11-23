# Removing the CS410 Environment

Everything for the MP work lives in one folder, `~/.cs410/` (about 4.7 GB):

- `~/.cs410/jdk`: Temurin JDK 21
- `~/.cs410/venv`: Python 3.12 venv (Pyserini, LangGraph, google-genai, pandas, requests, Jupyter)
- `~/.cs410/ollama`: standalone Ollama binary, its server log, and the downloaded models (`llama3.2`, about 2 GB) in `models/`
- `~/.cs410/gemini_key`: your Gemini API key (revoke it at https://aistudio.google.com/apikey if you no longer want it valid)
- `JAVA_HOME`, the Ollama `PATH`, `OLLAMA_MODELS`, and `GEMINI_API_KEY` are set only inside `~/.cs410/venv/bin/activate`. Nothing was added to `~/.zshrc`.

## 1. Remove the environment

```sh
pkill -f "ollama serve"    # stop the Ollama server if it is running
deactivate 2>/dev/null     # leave the venv if it is active
rm -rf ~/.cs410
rm -rf ~/.ollama           # Ollama's key pair and cache (about 12 KB), created outside OLLAMA_MODELS
```

This removes Java, Python packages, Ollama with its models, and the environment variables in one step.

## 2. Remove Python 3.12 (installed with Homebrew)

```sh
brew uninstall python@3.12
brew autoremove            # drops dependencies nothing else uses
```

Skip this step if you want to keep Python 3.12 for other work.

## 3. Optional leftovers

These are created only if you used the related tool. Check before deleting.

```sh
rm -rf ~/Library/Caches/pip          # pip cache (packages were installed with --no-cache-dir, so likely empty)
rm -rf ~/.cache/pyserini             # prebuilt indexes, only if you downloaded any
rm -rf ~/.cache/huggingface          # model downloads, only if a library fetched models
rm -rf ~/.jupyter ~/Library/Jupyter  # Jupyter config and runtime files
```

Per-assignment output such as `mp3_work/` and `mp3_transcript.json` is in the repo next to the notebook. Delete it there if you want it gone.
