# Quiz notes

## 1. True or false? NetPLSA leverages the power of both the text and the network structure to mine topics.

**Context.** NetPLSA is PLSA plus a network regularizer (graph harmonic function) that encourages neighboring nodes to have similar topic distributions. The joint objective uses both the text likelihood and the network structure.

**Correct answer.** True

**Why.** NetPLSA is explicitly defined as combining topic modeling on text with network regularization, so it uses both signals.

---

## 2. True or false? NetPLSA tries to smooth the topic transitions by forcing neighbor nodes in the network to have different topic coverage.

**Context.** The NetPLSA regularizer is a squared-difference penalty on topic coverage of adjacent nodes: larger differences raise the loss, smaller differences lower it. Smoothing means encouraging similar coverage across edges.

**Correct answer.** False

**Why.** The regularizer forces neighboring nodes toward similar topic distributions, not different ones. Forcing different coverage would increase the regularizer loss.

---

## 3. Contextual Probabilistic Latent Semantic Analysis (CPLSA) can be applied to which of the following tasks?

**Context.** CPLSA extends PLSA by adding context variables (time, location, etc.) that condition topic coverage and optionally word distributions. This supports temporal and spatiotemporal analyses.

**Correct answer.** All of the above

**Why.** CPLSA can model topic coverage over time alone (temporal trends) and over joint time–location contexts (how coverage evolves across places over time). Both tasks are direct applications of the model.

---

## 4. Suppose we are interested in discovering topics whose coverage in Twitter has strong correlations with airline prices. Which method would be best suited for this task?

**Context.** The task needs topics whose coverage correlates with an external numeric time series. Standard topic models do not target this; methods that feed the series back into topic estimation do.

**Correct answer.** Iterative Topic Modeling with Time Series Feedback

**Why.** ITMTF iteratively measures correlation of topic coverage with the external series and feeds strong correlating words back as priors. CPLSA can condition on time but does not optimize for correlation with an external numeric series. Plain PLSA and LDA ignore the external series.

---

## 5. Deep learning is a new topic emerging in machine learning. Suppose we are interested in knowing whether US researchers and those outside the US have different focuses when working on this topic. For this purpose, we can collect research publications with metadata such as the author names, their affiliations, and locations. Which of the following text mining techniques is most suitable for this task?

**Context.** The goal is to compare topical focus across two groups of researchers using metadata (affiliations, locations) as context. This is a cross-context comparative topic analysis problem.

**Correct answer.** Contextual PLSA (CPLSA)

**Why.** CPLSA treats location/affiliation as an explicit context variable that conditions topic coverage, so the fitted parameters directly quantify the difference in focus between groups. Text clustering ignores the metadata and only partitions by content. Iterative Topic Modeling with Time Series Supervision is for correlation with an external numeric series, not for comparing author-location contexts.

---

## 6. What is the additional input other than text in causal topic mining?

**Context.** Causal topic mining (ITMTF) jointly analyzes text and an external numeric series so that discovered topics are both coherent and correlated with that series.

**Correct answer.** Time

**Why.** The method takes documents plus a time-aligned external series. Anchor text and links are not inputs to this framework.

---

## 7. To measure the causality between two series, which of the following is true?

**Context.** In the causal-topic-mining material, causality between a topic-coverage series and an external series is assessed with a standard econometric test that checks whether one series improves prediction of the other after accounting for its own past.

**Correct answer.** Granger is often used.

**Why.** The ITMTF / InCaToMi framework explicitly applies Granger tests to decide which topics are causally related to the external time series. Alignment of peaks/dips or raw lagged correlation can be suggestive but are not the measure the method relies on.

---

## 8. If one is interested in finding out the trending topics in different countries in Twitter with the location information provided, what kind of technique should be used?

**Context.** The task requires topics whose coverage varies by geographic location. Location is an explicit context variable that should condition topic coverage.

**Correct answer.** Contextual PLSA (CPLSA)

**Why.** CPLSA incorporates location as a context variable so that topic coverage given location is estimated directly. Plain PLSA and LDA ignore the location metadata. Iterative Topic Modeling with Time Series Feedback is for aligning topics with an external numeric series, not for comparing locations.