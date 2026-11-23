BASELINE_JUDGMENTS = [
    {"verdict": "wrong",   "cause": "other"},       # Q1: right clip retrieved; model returned only timestamp
    {"verdict": "correct", "cause": ""},            # Q2
    {"verdict": "wrong",   "cause": "other"},       # Q3: model said it couldn't find clip
    {"verdict": "partial", "cause": "retrieval"},   # Q4: 5:30 clip with the rest of the answer not retrieved
    {"verdict": "partial", "cause": "retrieval"},   # Q5: defined moment (7:25) not retrieved; a different valid answer given
]
