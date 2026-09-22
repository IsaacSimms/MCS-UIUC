# CS410 MP1 — Fedora env setup and warmup start

**Date:** 2026-09-22
**Type:** setup
**Environment / Systems:** Fedora Linux desktop (Isaac Simms); Miniconda 26.7.1; conda env `pyserini`; Pyserini 2.4.0; OpenJDK 21.0.10 (conda-forge); system OpenJDK 25 left in place

## TL;DR
Stood up a local Pyserini toolchain on Fedora after dropping a GNOME Boxes VM. Env works (`lucene ok`, package 2.4.0). Starter `main.py` needed an API alias and the datasets folder renamed to `data/`. Warmup run has not yet produced a score.

## Context & Goal
Start CS410 Programming Assignment 1 (Pyserini / BM25 experiments). User asked to go step-by-step, not complete the assignment. First goal: installable environment on Fedora, then course code + datasets, then a stock `main.py` warmup.

## Key Points Explored
- Official path is conda + Python 3.12 + **Java 21**. Fedora’s default `java` is **25**; that is incompatible with Anserini/Pyserini. Do not uninstall 25; isolate 21 in the env.
- `pip install pyserini` on system Python is the wrong first step. `pyserini==latest` is not a real PyPI version; current release is **2.4.0**.
- GNOME Boxes / Ubuntu guest was considered, then abandoned. Work stays on the Fedora host.
- Miniconda lives in `~/miniconda3` and is removable (`rm -rf ~/miniconda3` plus the `~/.bashrc` conda init block).
- First `conda create` failed on Anaconda Terms of Service for `pkgs/main` and `pkgs/r`. Accepted via `conda tos accept`.
- `conda-forge` OpenJDK 21 download failed once (`Network is unreachable`); retry succeeded. Persist 21 with `$CONDA_PREFIX/etc/conda/activate.d/java21.sh`.
- `pyserini.__version__` does not exist; `importlib.metadata.version("pyserini")` → `2.4.0`. `from pyserini.search.lucene import LuceneSearcher` → `lucene ok`.
- Course zip was packed on macOS (`__MACOSX` deleted). Datasets landed as `CS410-MP1-code/CS410-MP1-data/{apnews,cranfield,new_faculty}` instead of `data/`.
- VS Code / run button used `/usr/bin/python` (no tqdm). Integrated Pylance was on Python 3.14 until the interpreter was switched to the conda env.
- Pyserini 2.4.0 renamed `IndexReader` → `LuceneIndexReader`. Starter code import was stale.
- After the import fix, stock `main.py` died on `data/apnews/apnews.dat` (folder still named `CS410-MP1-data`).

## Decisions & Outcomes
- No VM. Miniconda on Fedora.
- Env: `conda create -n pyserini python=3.12`, then `openjdk=21` + `maven` from conda-forge, CPU PyTorch, `pip install pyserini==2.4.0`.
- Skip `pyserini[optional]`, faiss, development install, and official MS MARCO verification.
- Assignment files live under  
  `/home/isaacsimms/Desktop/MCS-UIUC/Text Information Systems - CS410/Programming/MP1/`  
  not under `~/miniconda3`.
- Import in `main.py`:  
  `from pyserini.index.lucene import LuceneIndexReader as IndexReader`
- Next filesystem fix: `mv CS410-MP1-data data` inside `CS410-MP1-code`.

## Open Questions / Next Steps
- Confirm `data/apnews/apnews.dat` exists after the rename.
- Run `python main.py` from `(pyserini)` in `CS410-MP1-code` until a score prints and `results.json` appears.
- Point VS Code Run at `~/miniconda3/envs/pyserini/bin/python`, not `/usr/bin/python`.
- Warmup `###` switches in `main.py` after one clean default run.
- Graded work not started: Task 1 BM25 `k`/`b` on Cranfield; Task 2 two extra rankers; Task 3 cross-dataset. Report + zip due for peer review (10/25).

## Artifacts
- Conda env: `/home/isaacsimms/miniconda3/envs/pyserini`
- JDK pin script: `$CONDA_PREFIX/etc/conda/activate.d/java21.sh`
- Course tree: `.../Programming/MP1/CS410-MP1-code/main.py`
- Code zip: https://drive.google.com/file/d/1oB4Nc4XpdAqPWEG92DVF9XGFoG4D8L8c/view
- Dataset zip: https://drive.google.com/file/d/1FCcBPYRHC1cAUAUbptIGOV5sJaMw_aXN/view
- Pyserini install doc used: https://github.com/castorini/pyserini/blob/master/docs/installation.md