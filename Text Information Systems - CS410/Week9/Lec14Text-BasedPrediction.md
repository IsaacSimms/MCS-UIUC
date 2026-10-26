# Text-Based Prediction

CS 410 puts this week after categorization and sentiment analysis. The short lecture names two ideas: **text-based prediction** and the **data mining loop**. The rest of the week is joint analysis of text and non-text data, taught as contextual text mining.

The slide wording of that short lecture is unpublished. Definitions below are labeled by where they come from: the week’s own terms, the instructor’s later statement of the same task, or the papers whose problem names are the week’s keywords.

## The task

**Text-based prediction** uses text to estimate a value that lives outside the text.

The instructor’s later statement of this task (Jiang, Zhai, and Mei, 2018) sets it up as supervised learning: a map from documents to a numerical response. Examples there are restaurant ratings from comments, product sales from consumer feedback, and movie revenue from reviews. That paper calls the text “data reported by human sensors,” and says people are far more intelligent than physical sensors.

A forecasting whitepaper often paired with this topic (Smith, 2010) states a related challenge: given text about a social phenomenon, predict a measurement of that phenomenon that can be observed only later. Examples there include pre-release reviews predicting opening-weekend revenue, Form 10-K text predicting later return volatility, political posts predicting who comments and how much, and a Twitter positive-to-negative word ratio tracked against an economic confidence index.

## How this differs from categorization

Categorization assigns a category to the text (topic, sentiment, spam). Text-based prediction is also supervised learning, and it can start from the same surface words, but the target is a quantity the wording usually never states.

The 2018 paper’s running example is product reviews used to predict sales. The sales figure is very unlikely to appear in the review, and the correlation with raw lexical features can be weak. Smith draws the same line on movies: sentiment classification asks whether the critic is positive; forecasting asks what the film will earn.

## Two ways to use the text

**A separate predictor.** Represent the document, then train an ordinary model. Smith’s forecasters do this: elastic-net linear regression on words, bigrams, trigrams, and dependency relations; support-vector regression on words and bigrams; latent Dirichlet allocation topic weights inside a predictor, compared with a bag-of-words naive Bayes baseline. The 2018 paper notes the usual starting representation is surface words and phrases, with sentiment polarity as one intermediate feature. Topic models and sentiment classifiers can supply those features. Once the features exist, the predictor is ordinary regression or classification.

**Context inside the topic model.** The rest of this week does this. Non-text data enters the topic model as context, so the topics themselves depend on time, place, author, network, or an external series. The causal-topic paper says a pipeline that freezes the topics first and only afterward tests correlation cannot aim the topics at a chosen series. Those topics would be the same no matter which series you cared about.

## The data mining loop, and the semantic gap

The week’s own process term is the **data mining loop**. The public syllabus names it and does not list its steps. The loop diagram is omitted here because the slides were not available.

The textbook’s general claim about text systems is the nearest statement of why a person stays involved: people understand natural language better than computers, so the system is built to assist a person.

**Semantic gap** is the instructor’s 2018 name for the modeling difficulty, and it is absent from the week’s keyword list. It is the gap between the target variable and the surface features usually used to represent text. The text was written for a person. The number you want is rarely sitting in the words. The bridge proposed in that 2018 paper is a knowledge graph. This week teaches the contextual topic models below.

## Context

**Contextual text mining** treats context as part of the mining, and asks how topics vary across it.

A context is any metadata value that groups documents. Documents that share a value sit in the same context. One document can sit in several contexts at once. Any combination of metadata is a complex context.

- Explicit context: time, location, author, source, age group, occupation, citation frequency.
- Implicit context: the sentiment an author had while writing.
- Complex context: a social network, a citation graph, or a geographic network. Edges are handled by NetPLSA below.

Context partitions the collection so themes can be compared across the parts. Sample settings from the contextual-text-mining thesis: search logs in the context of a user, reviews in the context of sentiment, and blogs or papers in the context of a social network.

## CPLSA

**Contextual probabilistic latent semantic analysis** extends PLSA. Context chooses which view and which coverage generate the words. Parameters are still estimated with expectation-maximization.

- A **view** is a set of word distributions for the themes. The same theme can be worded differently in different contexts. This is content variation.
- A **coverage** is a distribution over themes. A theme can be strong in one context and weak in another. This is strength variation.
- A **global view**, shared by the whole collection, keeps one common version of each theme.

Two restrictions:

- **Fixed coverage.** Ask how the wording changes. This covers theme evolution, and shared themes set beside collection-specific themes.
- **Fixed view.** Ask how the strength changes. This covers theme life cycles, and a theme’s strength across time and place.

Cross-collection comparison is the fixed-coverage case with one global view and one view per subcollection. Shared themes can be set beside themes specific to each collection. That comparison is the KDD 2004 cross-collection mixture model.

## Spatiotemporal trends

Fixed-view CPLSA on blog posts retrieved for Hurricane Katrina, with week and U.S. state as context. Themes keep one global wording. Coverage changes. One illustrated theme is aid and donations, mapped across states over six weeks.

A separate view comparison on the same disaster: in states that were hit directly, the aid theme shifts toward medical care, and in the later weeks toward rebuilding and returning evacuees.

The earlier weblog study of Katrina and Rita separates two pictures:

- **Theme life cycle:** strength over time at a place.
- **Theme snapshot:** strength over places at one time.

Themes in that study include government response, New Orleans, and oil price. Katrina discussion in Louisiana rose again as Rita approached.

## Event impact analysis

Compare the wording of themes in documents from before an event with the wording from after it.

The CPLSA demonstration is 28 years of SIGIR abstracts and two events: the start of TREC in 1992, and the introduction of language models into information retrieval in 1998. Contexts may overlap. Everything before 1998 overlaps everything before 1993. A retrieval-model theme moves from vector-space and Boolean wording before TREC, toward collection, judgment, and ranking after TREC, and toward language-model, likelihood, and smoothing after 1998.

The Katrina maps track coverage over time and place. Event impact tracks wording before and after.

## NetPLSA

**Network-regularized topic modeling** applies when the context is a graph: co-authorship, friendship, citation, email reply, hyperlinks, or geography. Vertices connected by an edge should carry similar topic weights. The objective mixes ordinary topic-model likelihood with a graph smoother. With the smoother off, the model is ordinary PLSA. With PLSA as the topic model, the method is **NetPLSA**.

The output is a set of topics, a map of each topic onto the network, and topical communities. The smoother makes neighboring vertices agree. The topic model ties distant parts of the graph together through the text. A text-only topic model ignores the edges. A network-only community method has no guarantee of a coherent topic.

Author-as-a-label in CPLSA is a separate use of authorship. There, author and time are context labels, and one frequent-pattern theme is worded differently for each author and each era. NetPLSA uses the edges between people or places.

## Causal topics

A **causal topic** is a computational claim: a topic that is semantically coherent and strongly associated with an external time series, possibly with a lag. A positive or negative lag means the topic may lead the series or follow it. What “cause” means is left to the application. The method finds candidate associations for an analyst. Motivating pairs are news with stock prices, ads or reviews with sales, and campaign news with polls.

**Iterative topic modeling with time series supervision:**

1. Build topics.
2. Test which topics correlate with the series, including lags.
3. Inside those topics, test which frequent words correlate, and keep the sign of the impact.
4. Build a prior that favors those words. Split words with a positive impact from words with a negative impact, so they are not forced into one topic.
5. Run the topic model again under that prior.
6. Repeat.

A topic’s time series is its total coverage in the documents of each time bin. Experiments use news against prices from the Iowa Electronic Markets, and against American Airlines and Apple stock prices.

The series has to steer how topics are formed. Topics discovered first, then correlated, stay the same for every series.

## Core ideas

- Text-based prediction estimates an outside value from text. The week names that task and the data mining loop, then teaches joint mining.
- A separate predictor can take words, topic weights, or sentiment as features. This week’s models fold context into the topic model.
- CPLSA adds a context-dependent view (wording) and coverage (strength) on top of PLSA, still fit by expectation-maximization. A global view stays shared.
- Spatiotemporal trends track coverage over time and place (Katrina). Event impact tracks wording before and after an event (TREC, then language models).
- NetPLSA adds a network smoother so linked nodes share topic weight.
- Causal topics are steered by a time series through an iterative prior, including lag and the sign of each word’s impact.
