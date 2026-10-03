# Continuation of previous lecture
## Threshold learning
- The act of learnign the cutoff the binary classifier uses to accept or reject any one document.
- Deliver the document if its score is greater then 'theta'

### Difficulties in Threshold learning
- censored data i.e. judgments can only be made on available / delievered documents. (cant know if doc is above threshold if it has never been delievered to user)
- almost no data being labeled in the docs
- exploration vs exploitation
Exploting = only delivering documents well above theta
Exploring = delivering documents near or below theta to acquire missing labels (at the cost of bad deliveries getting through)
You want to explore as you can discover user preference and new interests for the user, but you do not want to explore to much, as you will over-deliver bad matches.

### Fixing these difficulties (Empirical Utility Optimization)
- Pick the cutoff score (theta) by measuring the utility function on labeled training documents and keeping the cutoff that scores the highest on that dataset. 
- Can be difficult due to biased training sets
Disregarded items could be interesting to the user.
can only use upper bound for true optimal threshold
**solution to this is the use of heuristic adjustment (lowering) of the Threshold**

#### Beta-Gamma Threshold Learning
A form of "lowering the threshold"
- The cutoff position (theta) gets lowered for each doc in correlation with the descending order of doc scores from the ranking perspective
- "Theta Optimal" = the point in which it will achieve the maximum utility if the system had chosen that value as the cutoff threshold
- "Zero utility threshold" = when the theta value is at 0 (any doc accepted at that point) (a safe starting point to explore the potential thresholds)