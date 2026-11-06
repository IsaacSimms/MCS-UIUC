# Quiz notes

## 1. True or false, Opinion mining can be used to decompose ratings into different aspects?

**Context.** Aspect-based opinion mining (e.g., Latent Aspect Rating Analysis / LARA) treats an overall rating as a combination of ratings on latent or explicit aspects.

**Correct answer.** True

**Why.** Opinion mining can infer aspect-level ratings and weights from review text + overall ratings, decomposing the single rating into aspect-specific scores.

---

## 2. Which is NOT true about Contextual Text Mining?

**Context.** Contextual Text Mining treats time, location, authors, etc. as first-class context that shapes topics.

**Correct answer.** Context does not influence both coverage and content variation of topics

**Why.** Context partitions text and supplies meaning to topics; models such as contextual PLSA explicitly analyze both coverage variation (how much a topic appears under a context) and content variation (how a topic’s word distribution changes across contexts). The first two statements are true; the third is not.

---

## 3. Which of the following are applications of Latent Aspect Rating Analysis?

**Context.** LARA jointly recovers latent aspects, per-aspect ratings, and aspect weights from review text + overall ratings. Those three outputs directly enable the listed uses.

**Correct answer.** All of the above

**Why.** Aspect ratings + weights support opinion-based entity ranking (rank by preferred aspects). Aspect ratings support aspect-level opinion summarization. Aspect weights reveal reviewer preferences. The LARA papers list exactly these three applications.

---

## 4. Imagine some analysts are interested in understanding any factors related to the fluctuating currency exchange rates of their country in the past year. They collected the companion text data including the news articles with time stamps in the past year and hope to gain potential insights from such text data. Which of the following text mining techniques would you recommend to them?

**Context.** The scenario supplies a companion text stream (timestamped news) plus an external time series (exchange rates). Contextual Text Mining covers both CPLSA (context as a view/coverage variable) and the more specific iterative causal topic modeling that treats a time series as supervision.

**Correct answer.** Iterative topic modeling with time series supervision

**Why.** CPLSA can partition topics by time and examine coverage/content variation, but it does not use an external numeric time series as a supervisory signal. The course technique that discovers topics whose coverage is correlated with a given time series is iterative topic modeling with time series supervision.

---

## 5. Non-text data can also help with text mining.

**Context.** Context and non-text signals (timestamps, ratings, time series, authors, locations, etc.) are treated as first-class inputs that improve topic discovery, opinion analysis, and causal mining.

**Correct answer.** True

**Why.** Contextual text mining, LARA, and time-series-supervised topic models all exist precisely because non-text data supplies the context or supervision that pure text analysis lacks.

---

## 6. Text data can help interpret patterns discovered from non-text data.

**Context.** Joint text + non-text mining is bidirectional: non-text can supervise or contextualize text, and text can supply the semantic interpretation for patterns found in non-text data.

**Correct answer.** True

**Why.** Topics or opinion themes recovered from companion text (news, reviews, etc.) are routinely used to explain movements in a time series, clusters in numeric data, or other non-text patterns.

---

## 7. True or false, CPLSA is an extension of PLSA?

**Context.** PLSA models documents as mixtures of latent topics. Contextual PLSA (CPLSA) adds context variables (time, location, author, etc.) so that both topic coverage and topic content can depend on context.

**Correct answer.** True

**Why.** CPLSA is defined as a direct extension of the PLSA generative model by introducing context into the topic and word distributions.