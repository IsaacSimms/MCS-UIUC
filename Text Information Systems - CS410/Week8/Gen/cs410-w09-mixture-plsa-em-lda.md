# CS410: Week 9 — Mixture models, PLSA, EM, and LDA

**CS 410 · Week 9 (Oct 19–25), catch-up note.** Syllabus keywords: mixture model, component model, constraints on probabilities, PLSA, EM algorithm, E-step and M-step, hidden variables, hill climbing, local maximum, LDA. ([Syllabus](https://app.notion.com/p/3c903d35d683801a87e5cdfbb10577d3)) Builds directly on [CS410: Week 8 — Entropy, mutual information, and topics as word distributions](https://app.notion.com/p/3f703d35d683811b90e4f8f3705b5b72) (unigram LM, MLE vs. MAP, Dirichlet pseudo-counts).

> 📚 **Source note.** Course material comes from Zhai's own slides for the topic-model lectures (mixture of unigram LMs → LDA), archived on GitHub, cross-checked against Hofmann (1999), Blei, Ng & Jordan (2003), and Blei (2012). The ACM Zhai & Massung PDF returned HTTP 403 again. Zhai's "Note on the EM Algorithm" (old UIUC/TIMAN URL) and Dempster–Laird–Rubin (1977, JSTOR) were not reachable from my box, so neither is cited for content.

## Why a mixture at all

Week 8 ended on an embarrassment: fit one unigram LM to one document by MLE and the top words are *the*, *a*, *is*. The model isn't wrong. Those words really are the most frequent. The problem is that one distribution has to explain *every* token. Zhai's fix is to give the document two generators and let them divide the work. With probability $\lambda_B$ a token comes from a fixed **background** LM $\theta_B$ (estimated from a large collection), and with probability $1-\lambda_B$ it comes from the unknown **topic** $\theta_d$:

$$
p(w\mid d) = \lambda_B\, p(w\mid\theta_B) + (1-\lambda_B)\, p(w\mid\theta_d)
$$

Each $\theta$ is a **component model**. The **constraints on probabilities** are that every component sums to one over $V$ and the mixing weights sum to one. The log-likelihood is $\sum_w c(w,d)\log[\lambda_B p(w\mid\theta_B) + (1-\lambda_B)p(w\mid\theta_d)]$. The log of a sum doesn't decouple, so there is no closed form like the $c(w,d)/|d|$ you get with one component ([Zhai, Mixture of Unigram LMs](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.1.pdf)).

Why does this factor out common words? Zhai's estimation lectures make the argument as a collaboration-and-competition game. To maximize likelihood, each component wants to put its probability on the words the *other* component gives low probability to. Since $\theta_B$ already gives *the* high probability, $\theta_d$ gains more by spending its limited mass on *text* and *mining*. Two corollaries are on the slides and are quiz favorites. First, high-frequency words in the document pull probability toward themselves in $\theta_d$ regardless. Second, the larger $\lambda_B$ is, the more aggressively background words are pushed out of the topic ([Zhai 3.2](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.2.pdf), [3.3](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.3.pdf)). The code below shows the second effect: at $\lambda_B=0.5$ *the* is still the top topic word, and at $\lambda_B=0.8$ it drops to zero.

## EM: guess the hidden labels, then count

If we knew which component produced each token, estimation would be trivial: count the topic-labeled tokens and normalize. That label is a **hidden variable** $z\in\{0,1\}$ (0 = topic, 1 = background). EM alternates between guessing it softly and counting with the guess ([Zhai 3.4–3.6](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.4.pdf)).

The **E-step** is Bayes rule for the posterior over $z$, given the current parameters:

$$
p^{(n)}(z=0\mid w) = \frac{(1-\lambda_B)\,p^{(n)}(w\mid\theta_d)}{(1-\lambda_B)\,p^{(n)}(w\mid\theta_d) + \lambda_B\, p(w\mid\theta_B)}
$$

The **M-step** treats those posteriors as *fractional counts* and re-normalizes:

$$
p^{(n+1)}(w\mid\theta_d) = \frac{c(w,d)\,p^{(n)}(z=0\mid w)}{\sum_{w'} c(w',d)\,p^{(n)}(z=0\mid w')}
$$

The M-step is just the Week 8 MLE with discounted counts. It is the solution of the Lagrangian $\sum_w \tilde c(w)\log\theta_w + \mu(1-\sum_w\theta_w)$, which gives $\theta_w = \tilde c(w)/\mu$, and the constraint forces $\mu = \sum_w \tilde c(w)$. That's all Lagrange multipliers do in this unit: they turn "sums to one" into "divide by the total." Every M-step you'll write, PLSA's included, has this normalize-the-expected-counts shape. Note that $z$ is per word *type* in the single-document case because identical tokens get identical posteriors.

**Hill climbing and local maxima.** Zhai's picture: the E-step builds a lower bound on the log-likelihood that touches it at the current guess, and the M-step jumps to the top of that bound. So the likelihood **never decreases**, which makes a free bug detector. If your log-likelihood ever drops, your code is wrong. The flip side is that EM is a local method. It converges to a local maximum (or a saddle point) that depends on the initialization. The standard practice is several random restarts, keeping the run with the highest likelihood ([Zhai 3.6](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.6.pdf)). The two-component case with a fixed background is benign because only one distribution is free. PLSA is where restarts really matter.

## PLSA: $k$ topics, per-document coverage

PLSA generalizes the mixture to $k$ unknown topics, each document having its own coverage $\pi_{d,j}$ (Zhai keeps the background component in):

$$
p_d(w) = \lambda_B\,p(w\mid\theta_B) + (1-\lambda_B)\sum_{j=1}^k \pi_{d,j}\,p(w\mid\theta_j)
$$

The hidden variable now says *which* topic produced $w$ in $d$. E-step: $p(z_{d,w}=j) \propto \pi_{d,j}\,p(w\mid\theta_j)$, normalized over $j$, plus a separate $p(z_{d,w}=B)$ for background. M-step: the fractional count $c(w,d)(1-p(z_{d,w}=B))\,p(z_{d,w}=j)$ is normalized over $j$ to give $\pi_{d,j}$, and summed over documents and normalized over $w$ to give $p(w\mid\theta_j)$ ([Zhai 3.7–3.8](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.7.pdf)). Hofmann's original "aspect model" is the same latent-class decomposition, $P(d,w)=\sum_z P(z)P(w\mid z)P(d\mid z)$, without the background, framed as a probabilistic answer to LSA's SVD ([Hofmann 1999](https://arxiv.org/pdf/1301.6705)).

**Count the parameters.** $k|V|$ word probabilities plus $Nk$ coverage values ($k(|V|-1)+N(k-1)$ free). Blei, Ng & Jordan put it bluntly: $kV + kM$ parameters, growing linearly with the corpus, "which leads to serious problems with overfitting," and no principled way to assign probability to a document outside the training set ([Blei et al. 2003](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)). Hofmann was already aware of this. His paper introduces **tempered EM**, which damps the E-step posteriors with an exponent and early-stops on held-out data, specifically to fight overfitting. Zhai's counterpoint is worth holding on to: for text *mining*, where you only want to explain the documents in hand, overfitting is less of a problem than it is for prediction ([Zhai 3.9](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.9.pdf)).

Zhai's "user-controlled PLSA" is the bridge to LDA. Put a conjugate prior on a topic, for example $p(w\mid\theta'_j)$ with *battery* 0.5 and *life* 0.5, and MAP estimation is still EM. The only change is that the M-step adds $\mu\,p(w\mid\theta'_j)$ pseudo-counts to the numerator and $\mu$ to the denominator. $\mu=0$ recovers PLSA, and $\mu\to\infty$ pins the topic to the prior. It's the Week 8 Dirichlet pseudo-count trick in a new place.

## LDA: PLSA with Dirichlet priors

LDA makes PLSA a real generative model by drawing both sets of parameters from Dirichlets: $\vec\pi_d \sim \text{Dir}(\vec\alpha)$ for coverage, and $\vec\theta_j\sim\text{Dir}(\vec\beta)$ for topics ([Zhai 3.10](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.10.pdf)). Zhai calls it "the Bayesian version of PLSA." The per-word likelihood inside is identical to PLSA's. What LDA adds is the integral over $\vec\pi_d$ (and over $\theta$):

$$
p(d\mid\vec\alpha,\{\theta_j\}) = \int \prod_{w\in V}\Big[\sum_{j=1}^k \pi_{d,j}\,p(w\mid\theta_j)\Big]^{c(w,d)} p(\vec\pi_d\mid\vec\alpha)\,d\vec\pi_d
$$

Three consequences. First, the *parameters* are now just $\vec\alpha$ and $\vec\beta$, and their number doesn't grow with $N$. Second, a new document has a well-defined probability: integrate over a fresh $\vec\pi$. Third, $\theta_j$ and $\pi_{d,j}$ are no longer estimated. They are *inferred* as posteriors, and that posterior is intractable because of the coupling between $\pi$ and $\theta$ inside the integral ([Blei et al. 2003](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)). So in practice you use approximate inference. Blei et al. use **variational EM**, which optimizes a factorized approximating distribution to tighten a bound, the same lower-bound idea as EM. **Collapsed Gibbs sampling** integrates out $\pi$ and $\theta$ and resamples each token's topic given all the others ([Blei 2012](https://www.cs.columbia.edu/~blei/papers/Blei2012.pdf)). For this course, knowing that and why these methods exist is enough. Zhai's slide also notes that for mining purposes LDA and PLSA give comparable topics. Small $\alpha$ encourages documents to concentrate on a few topics, and small $\beta$ encourages peaky topics. Blei 2012's sparsity discussion is the intuition.

## Programming notes

Here is the background-plus-topic EM, run on my box (numpy). The assertion checks the monotone-likelihood property on every iteration:

```py
import numpy as np

def em_bg_topic(counts, p_bg, lam_bg=0.5, iters=200, tol=1e-10, seed=0):
    rng = np.random.default_rng(seed)
    theta = rng.random(len(counts)); theta /= theta.sum()
    trace = []
    for _ in range(iters):
        top = (1 - lam_bg) * theta
        mix = top + lam_bg * p_bg
        trace.append(float(counts @ np.log(mix)))
        post = top / mix                    # E-step: p(z = topic | w)
        frac = counts * post                # fractional counts
        theta = frac / frac.sum()           # M-step: normalize
        if len(trace) > 1 and trace[-1] - trace[-2] < tol:
            break
    return theta, post, trace

vocab  = ["the", "a", "is", "text", "mining", "clustering", "algorithm"]
counts = np.array([20, 15, 10, 8, 6, 4, 3], float)
p_bg   = np.array([.40, .30, .20, .04, .03, .02, .01])
theta, post, ll = em_bg_topic(counts, p_bg, lam_bg=0.8)
assert all(b >= a - 1e-12 for a, b in zip(ll, ll[1:]))
```

With $\lambda_B=0.8$ it converges in 114 iterations (log-likelihood −121.94 → −116.96). The topic ends up as *text* 0.373, *mining* 0.280, *clustering* 0.187, *algorithm* 0.160, and *the/a/is* ≈ 0. With $\lambda_B=0.5$ the same data gives *the* 0.206 as the top topic word. That is Zhai's "larger $\lambda_B$ pushes background words out" made concrete. Practical habits: log the likelihood every iteration and assert it is monotone. Stop on *relative* change. Initialize randomly, not uniformly. For multi-topic PLSA a uniform start is symmetric, so every topic stays identical forever. Add a tiny $\epsilon$ before taking logs. For PLSA, keep the posterior as a $(N,|V|,k)$ array only for toy data; on real data, loop over nonzero $(d,w)$ cells of a sparse matrix. For LDA, don't write your own. Use gensim or scikit-learn and spend your time on $k$, $\alpha$, and preprocessing.

## Sources

- CS410 Syllabus, Week 9 row: [Syllabus](https://app.notion.com/p/3c903d35d683801a87e5cdfbb10577d3)
- C. Zhai, *Text Mining and Analytics* lecture slides (Coursera; CS410 Week 9 lectures), archived on GitHub: Mixture of Unigram LMs [3.1](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.1.pdf) · Mixture Model Estimation [3.2](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.2.pdf), [3.3](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.3.pdf) · EM Algorithm [3.4](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.4.pdf), [3.5](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.5.pdf), [3.6](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.6.pdf) · PLSA [3.7](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.7.pdf), [3.8](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.8.pdf) · LDA [3.9](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.9.pdf), [3.10](https://raw.githubusercontent.com/rikenshah/text-mining-course/master/Week3/singlePDFs/3.10.pdf)
- T. Hofmann, "Probabilistic Latent Semantic Analysis," UAI 1999: [https://arxiv.org/pdf/1301.6705](https://arxiv.org/pdf/1301.6705)
- D. Blei, A. Ng & M. Jordan, "Latent Dirichlet Allocation," *JMLR* 3, 2003: [https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)
- D. Blei, "Probabilistic Topic Models," *CACM* 55(4), 2012: [https://www.cs.columbia.edu/\~blei/papers/Blei2012.pdf](https://www.cs.columbia.edu/~blei/papers/Blei2012.pdf)
- Not read (blocked or unreachable): Zhai & Massung ACM PDF [https://dl.acm.org/doi/pdf/10.1145/2915031](https://dl.acm.org/doi/pdf/10.1145/2915031) (403); Dempster, Laird & Rubin 1977, JSTOR (blocked); Zhai, "A Note on the EM Algorithm" (UIUC TIMAN URL unreachable).

## For the podcast

- **Audience:** MCS students in CS410 who know the Week 8 unigram LM, MLE, and Dirichlet pseudo-counts. Connect to those; don't re-derive them.
- **Emphasize:** why a fixed background makes the topic drop common words (competition for probability mass, and the effect of $\lambda_B$); EM as "guess the hidden labels softly, then count"; monotone likelihood but only a local max; PLSA's parameter count growing with $N$; LDA as "PLSA plus Dirichlet priors." **Skip:** the variational derivation, Gibbs conditionals, tempered EM details, and anything about clustering or categorization (Week 10).
- **Say clearly:** *Hofmann*, *Blei* (BLIGH), *Ng*, *Jordan*, *Dirichlet* (dee-ree-KLAY), *PLSA* (P-L-S-A; also "pLSI"), *LDA*, *lambda-B* for background weight, *pi d j* for coverage, *theta j* for a topic, *z* for the hidden variable.
- **E and M aloud:** E-step is "for each word, what fraction of its count does the topic deserve, versus background, given what we currently believe." M-step is "add up those fractional counts and divide by the total." Monotonicity is "each round climbs the hill; it can never go downhill, but it may stop on a small hill."
- **Misconceptions:** "EM finds the global maximum" (no, use restarts); "the background is learned" (it's fixed, and so is $\lambda_B$ in Zhai's setup); "LDA gives better topics than PLSA" (for mining they're comparable; LDA's gain is generativity and regularization); "Lagrange multipliers are an extra algorithm" (they just yield normalize-by-total); "$z$ is observed" (it's the whole point that it isn't); "uniform init is safe" (symmetric topics never separate).
