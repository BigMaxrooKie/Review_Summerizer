# sentiment.py


sentiment_weights = {
    "best": 4,         # Highest positive
    "excellent": 3,
    "good": 2,
    "poor": -3,        # Worse than bad
    "bad": -2,
    "worst": -4        # Most negative
}

def score_comments(comments):
    total_score = 0
    for comment in comments:
        words = comment.lower().split()
        for word in words:
            if word in sentiment_weights:
                total_score += sentiment_weights[word]
    return total_score

def map_score_to_verdict(score):
    if score > 10:
        return "Positive"
    elif score > 0:
        return "Slightly Positive"
    elif score == 0:
        return "Neutral"
    elif score > -10:
        return "Slightly Negative"
    else:
        return "Negative"