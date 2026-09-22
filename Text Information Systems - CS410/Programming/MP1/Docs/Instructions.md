# Programming Assignment 1 (MP1)

**Overview**

**Motivation:** The goal of this assignment is to provide you hands-on experience with using and experimenting with the pyserini toolkit for indexing and search  ([https://github.com/castorini/pyserini](https://github.com/castorini/pyserini)). It is a research-oriented toolkit built on top of another research toolkit, called anserini ([https://github.com/castorini/anserini](https://github.com/castorini/anserini)), which is based on the Lucene search engine toolkit ([https://lucene.apache.org/](https://lucene.apache.org/)). Lucene is the most popular commercial search engine toolkit, which powers virtually all the most popular commercial search engine toolkits, e.g.,  Slor([https://solr.apache.org/](https://solr.apache.org/)),  ElasticSearch ([https://www.elastic.co/](https://www.elastic.co/)) , and OpenSearch ([https://opensearch.org/](https://opensearch.org/)).  Pyserini allows you to easily experiment with many cutting-edge retrieval algorithms to learn about their behavior. The focus of this assignment is on BM25, which is the most well-known retrieval function used in all search engines. It is quite robust and generally performs reasonably well in all kinds of retrieval applications. You will also have a chance to explore some other retrieval algorithms in Pyserini. Being familiar with the retrieval algorithms in Pyserini would not only be useful if you would like to use the toolkit to build your own search engine applications but also allow you to use it to support an intelligent agent or a large language model (LLM) for Retrieval-Augmented Generation (RAG), a topic that will be covered later in the semester. The assignment also provides you with an opportunity to learn how to run retrieval experiments and analyze retrieval results, a skill useful for both optimizing/improving an existing retrieval algorithm and testing any new algorithm that you can propose. 

**Tasks:** You will install the toolkit, download the datasets, and experiment with various algorithms. You will summarize your experiments and results in a report, which will be submitted for grading.  

**Grading:** As this is an open exploration assignment, the grading will be done by peer reviewing, which will give you a chance to learn from the reports of others as well as provide feedback to them, thus achieving the goal of collaborative learning.  Please finish the peer review on time, as the grade won't be available until the peer review is completed.

**Installation and Datasets**

Please follow [https://github.com/castorini/pyserini/blob/master/docs/installation.md\#pypi-installation-walkthrough](https://github.com/castorini/pyserini/blob/master/docs/installation.md#pypi-installation-walkthrough) for installation instruction on your computer (for Mac and Linux).  Make sure each installation command finishes running without errors. Please do not use Development Installation. You also do not need to go through the "Verifying the Installation" section as it might have server issues. 

**Special instructions on installation on Windows:** Please **do not directly install Pyserini on Windows** using the installation link as it might not have Windows support. If you don't have access to any Linux machines or server, your best option is to install Windows Subsystem for Linux (WSL). While it will take a bit of extra time, it is likely to be useful to you in the future if you continue working with such applications.

The first step is to follow the instructions for installing wsl here:  [https://learn.microsoft.com/en-us/windows/wsl/installOpens in a new tab](https://learn.microsoft.com/en-us/windows/wsl/install)  Once installed, you should be able to run WSL by searching wsl or the name of the distribution in windows search. Next, install anaconda, following instructions for linux:  [https://docs.anaconda.com/anaconda/install/linux/Opens in a new tab](https://docs.anaconda.com/anaconda/install/linux/) 

Finally, proceed with Linux section in  [https://github.com/castorini/pyserini/blob/master/docs/installation.md\#pypi-installation-walkthroughOpens in a new tab](https://github.com/castorini/pyserini/blob/master/docs/installation.md#pypi-installation-walkthrough)  . **Please do not use Development Installation.**

Note: You can also check out  [https://campuswire.com/c/G454D3A2F/feed/84Opens in a new tab](https://campuswire.com/c/G454D3A2F/feed/84)  if you encounter installation errors in Ubuntu.

**Bonus Tip:** VSCode for WSL While you can edit files in nano or vim on WSL, it is much more convenient to use the VSCode WSL extension. VSCode lets you mount to WSL so that you can edit your WSL files while still having all the benefits of a modern code editor. Further, it allows you to easily drag and drop files into your WSL file system. As such, it is recommended that you use this tool if you are using WSL. You can install it following the instructions here:  [https://code.visualstudio.com/docs/remote/wslOpens in a new tab](https://code.visualstudio.com/docs/remote/wsl) 

### **Linux Access for Mac**:  Please only try this step if you are unable to install on Mac directly using the assignment instruction. We discovered that the Pyserini package could occasionally introduce installation difficulties for certain Mac versions. If you use a Mac and find tricky installation issues, an efficient solution is to use a Linux environment. While it might take a few minutes to set up, it could save you time in the long run by helping you avoid many system-specific barriers in your future projects.

(Option 1\) UIUC server [https://answers.uillinois.edu/illinois.engineering/81727](https://answers.uillinois.edu/illinois.engineering/81727) (where you do not need to install anything locally)

(Option 2\) Mac Local VM [https://multipass.run/install](https://multipass.run/install)

Before kicking off the instance, specify CPU, Disk, and Memory for the VM by going to the Detail tab in the Multipass UI (you can follow [https://multipass.run/docs/about-performance](https://multipass.run/docs/about-performance) for how much to specify, usually reserve 2 threads and 4GB mem for the host end should be good).

Now start an instance and a multipass terminal with the Multipass UI (e.g, the installed application on mac).

You can follow the below guide to access local data on multipass  [https://multipass.run/docs/share-data-with-an-instance](https://multipass.run/docs/share-data-with-an-instance)

Make sure to enable multipassd in full disk access from Mac privacy and Security to enable mounting.


If you go for the mounting option, make sure to run the mounting command in mac terminal. Also, you would need to use the exact path you use for local path. For instance if you do `multipass mount /Users/username/Documents/CS410/ instance-name`, then you can `cd` into `/Users/username/Documents/CS410/` in multipass. Make sure you know which local folder you are at in multipass by, for example, `ls` or `pwd`.

After the server or virtual machine has been set up, follow [https://docs.anaconda.com/anaconda/install/linux/](https://docs.anaconda.com/anaconda/install/linux/) for anaconda installation. For Mac M chip with Multipass, download from AWS Graviton2/ARM64 instead of Linux x86. When running the `bash` line, make sure not directly copying `...~/Downloads/...` and modify the path to be where the installer is.

Notes: Please search on the web first for resolving package installation errors since they vary for systems. ChatGPT may also provide help for resolving such errors. If you encounter subprocess error from spacy when `pip install pyserini`, try `conda install -c conda-forge spacy` and redo `pip install pyserini`

After you finish the installation without any errors, download and extract the experimental code from  [https://drive.google.com/file/d/1oB4Nc4XpdAqPWEG92DVF9XGFoG4D8L8c/view?usp=drive\_link](https://drive.google.com/file/d/1oB4Nc4XpdAqPWEG92DVF9XGFoG4D8L8c/view?usp=drive_link)

and datasets from [https://drive.google.com/file/d/1FCcBPYRHC1cAUAUbptIGOV5sJaMw\_aXN/view?usp=drive\_link](https://drive.google.com/file/d/1FCcBPYRHC1cAUAUbptIGOV5sJaMw_aXN/view?usp=drive_link) 

Move the data folder into the code folder.

The ranker will be evaluated using NDCG@10 score on 3 datasets:

1\) Cranfield dataset, which was among the first-generation information retrieval test collections constructed in 1960s, well known for establishing the Cranfield Evaluation Methodology, in which the researchers first introduced popular measures such as Precision and Recall, which are still used widely today.  (see [https://en.wikipedia.org/wiki/Cranfield\_experiments](https://en.wikipedia.org/wiki/Cranfield_experiments)).

2\)  An AP news dataset, which consists of news articles from Associate Press around the time of 1989-1990. It was one of the earliest data sets used by TREC, a US government-initiated evaluation conference, which has significantly impacted information retrieval research over all these years via the many test collections it has created and released ([https://www.nist.gov/programs-projects/text-retrieval-conference-trec](https://www.nist.gov/programs-projects/text-retrieval-conference-trec)).

3\) A web page dataset created by the students in a previous CS410 class, which includes faculty home pages crawled from the Web. Experimenting with multiple datasets would allow you to  see somewhat different behaviors of ranking algorithms on different data sets (thus the best parameter setting on one dataset is not necessarily best on another).

**Tasks**

**Warmup Task**

Modify main.py and look for places with "\#\#\#"'s to change specifications. If the installation is correct, the execution should print out score and results.json should appear in the corresponding dataset folder.

If you want to rebuild preprocessed corpus or index, simply delete the corresponding data folder in \`indexes/\` and \`processed\_corpus/\`

For people who are new to coding in Python, it's an excellent opportunity to learn python development. Python is one of the most popular programming languages nowadays and is widely used in AI development. There are many online tutorials (e.g., Python's official tutorial) and code assistant AI (like Copilot and Claude Sonnet) that could help you learn.

You can try to test a basic retriever such as BM25  by varying its parameters and explore the following questions: 1\) How does each parameter impact the retrieval accuracy? Do some values work better than other values? (2) Are the optimal parameter values the same or similar on those different test collections? (3) How would different configurations of main.py affect the retrieval performance in general?

**Graded Tasks**

1\. BM25 Parameter Exploration (40% of total grade)

Using the Cranfield dataset, experiment with the two parameters of BM25: k and b.

\- Plot two curves showing how nDCG@10 (already provided) and Precision@10 (which you can implement easily) vary as b or k changes. The interpretation of being relevant or not for Precision@10 is open. You can treat a relevance score larger than 0 as being relevant, for instance, 0=non-relevant, {1,2,3}=relevant, or you can also interpret only a score larger than 2 as being relevant. There is no restriction on how many data points to draw for the curve. You can use any plotting tool of your choice (e.g., matplotlib, excel):

a) One plot (with two curves for two metrics) for b with k set to any fixed value

b) One plot for k with b set to any fixed value

\- Report and interpret your observations

2\. Algorithm Comparison (40% of total grade)

\- Choose two additional ranking algorithms/models (e.g., TF-IDF, pseudo-relevance feedback, embedding-based methods). Pyserini provides some traditional ranking algorithms in LuceneSearcher (e.g., pyserini.search.lucene.\_searcher.LuceneSearcher) class and dense retrieval models in FaissSearcher for which you can take a look at, detailed at https://github.com/castorini/pyserini/tree/master?tab=readme-ov-file\#-how-do-i-search.

\- Compare their performance against the base BM25 on a dataset and a metric of your choice. See the warm-up assignment for dataset details. You do not need to plot like in Task 1\. Only reporting the performance for each algorithm is sufficient (e.g., algorithm x has NDCG@10 of y). You can use any hyperparameter for the algorithm (e.g., for BM25, you can use any b and k you find performing well from the previous Task 1). You can use the datasets we provided in the warm-up assignment.

\- Analyze and discuss the results, identifying the best-performing algorithm

3\. Cross-Dataset Analysis (20% of total grade)

\- Replicate the experiments from Task 2 on a different dataset

\- Compare the results with your initial findings in Task 2\. Discuss whether the "winning" algorithm remains consistent across datasets. If there are any differences, provide potential explanations.

**Deliverables & Submission** 

1\. A concise report in PDF summarizing your experiments, results, and insights.

2\. python files (e.g., with .py extension) used for implementing and running the experiments, which can be in either a zip or separate files.

**Please submit a single zip file containing all the deliverables.**