# Benefits of Rewriting your Statistical Language Model using Smoothing
See "Text Information Systems - CS410/Week4/Lesson 2 Statistical Language Model/RewriteRankingFunctionViaSmoothingBenefits.png"
## 2 Benefits
- You better understand the ranking function
    - Smoothing gives you TF-IDF weighting (p(w|C) gives you TF logic) (p_seen(w_i | C) gives you IDF logic) and doc length normalization (nlog(alpha_d) gives you normalization logic)
        Longer docs = less smoothing
- Boxed sum (from image) does not change ranking
- MLE zeros kill the ranking without a rewrite

- Enable efficient computation