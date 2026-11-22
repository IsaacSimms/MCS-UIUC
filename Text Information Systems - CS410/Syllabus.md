# Syllabus

Created by: Isaac Simms
Created time: August 26, 2026 9:50 PM
Category: CS410
Last edited by: Isaac Simms
Last updated time: August 26, 2026 10:11 PM

# Syllabus

# CS 410: Text Information Systems

## Course Description

The growth of “big data” created unprecedented opportunities to leverage computational and statistical approaches, which turn raw data into actionable knowledge that can support various application tasks. This is especially true for the optimization of decision making in virtually all application domains, such as health and medicine, security and safety, learning and education, scientific discovery, and business intelligence. This course covers general computational techniques for building intelligent text information systems to help users manage and make use of large amounts of text data in all kinds of applications.

Text data include all data in the form of natural language text (e.g., English text or Chinese text), including all web pages, social media data such as tweets, news, scientific literature, emails, government documents, and many other kinds of enterprise data. Text data play an essential role in our lives. Since we communicate using natural languages, we produce and consume a large amount of text data every day covering all kinds of topics. The explosive growth of text data makes it impossible for people to consume all the relevant text data in a timely manner.

The two main techniques to assist people in consuming, digesting, and making use of the text data are:

1. Text retrieval, which helps identify the most relevant text data to a particular problem from a large collection of text documents, thus avoiding processing a large number of non-relevant documents
2. Text mining, which helps users further analyze and digest the found relevant text data and extract actionable knowledge for finishing a task

This course covers both text retrieval and text mining, so as to provide you with the opportunity to see the complete spectrum of techniques used in building an intelligent text information system. Most lectures are based on two MOOCs covering the same topic and thus available on Coursera, but additional new lectures that cover the newest development on large language models (LLMs) and interactive task agents will be provided in the second half of the semester, which may not necessarily be available on Coursera (if not, they will most likely be available on Illinois Media Space).  On top of the lectures, the course also includes programming assignments (i.e., "Machine Problems") and a course project. With all these components,  this course enables you to learn the basic concepts, principles, and general techniques in text retrieval and mining, as well as gain hands-on experience with using software tools to develop interesting text data applications.

## Course Goals and Objectives

Upon successful completion of this course, you will be able to:

- Explain all the basic concepts in text retrieval and text mining.
- Explain the main ideas behind the major models and algorithms for text retrieval and text mining.
- Explain how the major models and algorithms for text retrieval and text mining work.
- Explain how to implement some of the commonly used algorithms for text retrieval and text mining.
- Explain how to evaluate applications of text retrieval and text mining.

## Textbook

There is not a required textbook for this course, but there are several optional readings suggested in each week's overview page. All readings listed in the weekly overview pages are optional and are primarily from the following textbook. A PDF version of the book is available via ACM Digital Library, which you all should have access at  [https://dl.acm.org/doi/pdf/10.1145/2915031](https://dl.acm.org/doi/pdf/10.1145/2915031)

Zhai, C. & Massung, S. (2016). *Text data management and analysis: A practical introduction to information retrieval and text mining.* ACM Book Series. Morgan & Claypool Publishers.

This book is under revision. A draft version of the new version with addition of large language models and agents is expected to be available later in the semester.  The new content to be added is primarily about LLMs and intelligent agents and how they can be used for text data management and analysis. You can read the three new chapters at [https://files.campuswire.com/b1412ac3-c3de-48bf-ae6b-d0e82cd6ad80/8e069ae2-fb6d-4738-8bf0-d5f2218dcb58/LLM-textdata.pdf](https://files.campuswire.com/b1412ac3-c3de-48bf-ae6b-d0e82cd6ad80/8e069ae2-fb6d-4738-8bf0-d5f2218dcb58/LLM-textdata.pdf)

## Tentative Course Outline (You may assume that the first three weeks are accurate; everything after Week 4 will be updated later)

| **Week** | **Dates** | **Topics** |
| --- | --- | --- |
| **Week 1** | August 24 - Aug. 30 | Part of Speech tagging, syntactic analysis, semantic analysis, ambiguity, “bag of words” representation, push, pull, querying, browsing, probability ranking principle, relevance, vector space model, dot product, bit vector representation |
| **Week 2** | Aug. 31 - September 6 | Term frequency (TF), document frequency (DF), and inverse document frequency (IDF), TF transformation, pivoted length normalization, BM25, inverted index and postings, binary coding, unary coding, gamma-coding, d-gap, Zipf’s law |
| **Week 3** | September 7 -13 | Cranfield evaluation methodology, precision and recall, average precision, mean average precision (MAP), geometric mean average precision (gMAP), reciprocal rank, mean reciprocal rank, F-measure , Normalized Discounted Cumulative Gain (nDCG), statistical significance test |
| **Week 4** | September 14 - 20 | <u>**All the content after this week is under construction</u>.** 
p(R=1|q,d), query likelihood, p(q|d), statistical and unigram language models, maximum likelihood estimate, background, collection, and document language models, smoothing of unigram language models, relation between query likelihood and TF-IDF weighting, linear interpolation (i.e., Jelinek-Mercer) smoothing, Dirichlet Prior smoothing |
| **Week 5** | September 21 - 27 | Relevance feedback, pseudo-relevance feedback, implicit feedback, Rocchio feedback, Kullback-Leiber divergence (KL-divergence) retrieval function, mixture language model, scalability and efficiency, spams, crawler, focused crawling, and incremental crawling, Google File System (GFS), MapReduce, link analysis and anchor text, PageRank |
| **Week 6** | September 28 - October 4 | Content-based filtering, collaborative filtering, Beta-Gamma threshold learning, linear utility , user profile, exploration-exploitation tradeoff, memory-based collaborative filtering, cold start |
| **Week 7** | October 5 - 11 | Text representation (especially bag-of-words representation), context of a word, context similarity, paradigmatic relation, syntagmatic relation. |
| **Week 8** | October 12 - 18 | Entropy, conditional entropy, mutual information, topics, coverage of topic , language model, generative model, unigram language model, word distribution, background language model, parameters of a probabilistic model, likelihood, Bayes rule, maximum likelihood estimation, prior and posterior distributions, Bayesian estimation & inference, maximum a posteriori (MAP) estimate, prior model, posterior mode.
 |
| **Week 9** | October 19 - 25 | Mixture model, component model, constraints on probabilities, Probabilistic Latent Semantic Analysis (PLSA), Expectation-Maximization (EM) algorithm, E-step and M-step, hidden variables, hill climbing, local maximum, Latent Dirichlet Allocation (LDA) |
| **Week 10** | October 26 - November 1 | Clustering, document clustering, term clustering, clustering bias, perspective of similarity, Hierarchical Agglomerative Clustering, k-Means, direction evaluation (of clustering), indirect evaluation (of clustering), text categorization, topic categorization, sentiment categorization, email routing , spam filtering, naïve Bayes classifier, smoothing
**Week of Exam** |
| **Week 11** | November 2 - 8 | Generative classifier vs. discriminative classifier, training data, logistic regression, K-Nearest Neighbor classifier, classification accuracy, precision, recall, F measure, macro-averaging, micro-averaging, opinion holder, opinion target, sentiment, opinion representation, sentiment classification, features, n-grams, frequent patterns, overfitting |
| **Week 12** | November 9 - 15 | Text-based prediction, the “data mining loop”, context (of text data), contextual text mining, contextual probabilistic latent semantic analysis (CPLSA), views of a topic, coverage of topics, spatiotemporal trends of topics, event impact analysis, network-regularized topic modeling, NetPLSA, causal topics, iterative topic modeling with time series supervision |
| **Week 13** | November 16 - 22 | Project work week. |
| **Week 14** | November 23 - November 29 | *Thanksgiving Break* |
| **Week 15** | Nov 30 - December 6 | No new content - work on your final project! |
| **Week 16** | December 7 - 13 | Final Project Presentation and Report Due Start of Finals Week |

## Elements of This Course

- **Lecture videos.** Each week your instructor will teach you the concepts you need to know through a collection of short video lectures. You may either stream these videos for playback within the browser by clicking on their titles, or you can download each video for later offline playback by clicking the download icon. **The videos usually total 1.5 to 2 hours each week**, but you generally need to spend at least the same amount of time digesting the content in the videos. The actual amount of time needed to digest the content will naturally vary according to your background.
- **Quizzes.** Most weeks will include one for-credit quiz. You will have two attempts for each quiz, with your highest score used toward your final grade. We will drop the two lowest quiz scores).
- **Exam**. This course will have one 1-hour exam. The exam is intended to test your understanding of the material you learn in the course and will contain questions similar to those seen in the weekly quizzes.
- **Programming Assignments.** The programming assignments for this course, also called "Machine Problems (MPs)", provide an opportunity for you to practice your programming skills and experiment with algorithms and data sets based on what you've learned in the course. Set aside about 2-4 hours each week to work on the programming assignment during the period of completing the programming assignments.
- **Tech Review (required onlyfor 4-credit students).** It will require you to generate a brief review on an interesting course-related cutting-edge technology topic not covered in any lecture.
- **Final Course Project.** There will also be one culminating project due at the end of course. It will require you to work in groups (a one-person group is also allowed) to apply what you've learned in the course to solve a real world problem by developing a new useful application or extending an existing tool to add new functions. The software developed by you along with documentation will be made publicly available. You are expected to produce a presentation to demonstrate how to use the software that you have developed.

## Grading

Your final grade will be calculated based on the activities listed in the table below. As a note, the grade on Coursera will NOT accurately reflect your grade in the course.

| **Activity** | **Percent of Final Grade** |
| --- | --- |
| Quizzes | 20% |
| Programming Assignments | 30% |
| Course Project | 30% |
| Exam | 20% |
|  |  |

| **Letter Grade** | **Points Needed** | **Letter Grade** | **Points Needed** | **Letter Grade** | **Points Needed** |
| --- | --- | --- | --- | --- | --- |
| **A+** | 95 | **B+** | 80 | **C** | 60 |
| **A** | 90 | **B** | 75 | **D** | 55 |
| **A-** | 85 | **B-** | 70 | **F** | <55 |

Your final grade will be calculated based on the activities listed in the table below. Your official final course grade will be listed in [Enterprise](https://apps.uillinois.edu/selfservice/). The course grade you see displayed in Coursera may not match your official final course grade.

## Additional Course Policies

### Student Code and Policies

A student at the University of Illinois at the Urbana‑Champaign campus is a member of a University community of which all members have at least the rights and responsibilities common to all citizens, free from institutional censorship; affiliation with the University as a student does not diminish the rights or responsibilities held by a student or any other community member as a citizen of larger communities of the state, the nation, and the world. See the [University of Illinois Student Code](http://studentcode.illinois.edu/index.html) for more information.

The CS department also maintains a policies handbook for graduate student. For more information, see the [Graduate Student Handbook](https://cs.illinois.edu/sites/default/files/images/CSGraduateStudentHandbook_web.15-16.pdf).

Additionally, all Coursera learners are required to follow an [Honor Code](https://learner.coursera.help/hc/en-us/articles/209818863-Coursera-Honor-Code) and a [Code of Conduct](https://learner.coursera.help/hc/en-us/articles/208280036-Coursera-Code-of-Conduct). Please review both of these items before commencing your studies.

### Academic Integrity

All students are expected to abide by [the campus regulations on academic integrity found in the Student Code of Conduct](http://admin.illinois.edu/policy/code/article1_part4_1-401.html). These standards will be enforced and infractions of these rules will not be tolerated in this course. Sharing, copying, or providing any part of a homework solution or code is an infraction of the University’s rules on academic integrity. We will be actively looking for violations of this policy in homework and project submissions. Any violation will be punished as severely as possible with sanctions and penalties typically ranging from a failing grade on this assignment up to a failing grade in the course, including a letter of the offending infraction kept in the student's permanent university record.

Again, a good rule of thumb: *Keep every typed word and piece of code your own*. If you think you are operating in a gray area, you probably are. If you would like clarification on specifics, please contact the course staff.

### Disability Accommodations

Students with learning, physical, or other disabilities requiring assistance should contact the instructor as soon as possible. If you’re unsure if this applies to you or think it may, please contact the instructor and [Disability Resources and Educational Services (DRES)](http://disability.illinois.edu/) as soon as possible. You can contact DRES at 1207 S. Oak Street, Champaign, via phone at (217) 333-1970, or via email at [disability@illinois.edu](mailto:disability@illinois.edu).

### Late Policy

Late homework and homework by email will not be accepted by the TA or the instructors without prior instructor approval.