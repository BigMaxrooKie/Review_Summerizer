# sentiment.py

# Extensive sentiment weights for YouTube comments
sentiment_weights = {
    # Very positive
    "best": 4, "awesome": 3, "amazing": 3, "funny": 2, "hilarious": 2, "love": 3, "loved": 3,
    "yay": 2, "favorite": 3, "brilliant": 3, "cool": 2, "wow": 2, "incredible": 4, "amazing": 3,
    "impressive": 2, "nice": 2, "cute": 2, "fabulous": 3, "epic": 3, "legendary": 3, "bestever": 4,
    "amazinggg": 3, "perfect": 4, "superb": 3, "fantastic": 4, "phenomenal": 4, "masterpiece": 4,

    # Slightly positive
    "good": 2, "great": 3, "fun": 2, "ok": 1, "okay": 1, "interesting": 1, "meh": 0, "decent": 2,
    "acceptable": 1, "coolio": 2, "alright": 1, "impressive": 2, "yayyy": 2, "awesomeee": 3,

    # Neutral / mixed
    "average": 0, "hmm": 0, "🤔": 0, "👀": 0, "idk": 0, "notbad": 1, "somewhat": 0, "maybe": 0,
    "so-so": 0, "neutral": 0, "fine": 1, "kinda": 0, "eh": -1, "alrighty": 1, "soso": 0,

    # Slightly negative
    "sad": -2, "disappointed": -2, "ugh": -2, "meh": -1, "confusing": -1, "rip": -2, "ohno": -2,
    "oops": -1, "wtf": -2, "huh": -1, "smh": -2, "fail": -3, "oopsie": -1, "dang": -1,
    "bleh": -1, "yikes": -2, "ughgh": -2, "oopsies": -1,

    # Negative
    "bad": -2, "worst": -4, "awful": -3, "terrible": -3, "stupid": -3, "idiot": -4, "moron": -4,
    "dumb": -3, "loser": -3, "dislike": -3, "hated": -4, "hate": -3, "boring": -2, "scam": -4,
    "fraud": -4, "criminal": -3, "bullshit": -3, "broken": -2, "trash": -3, "heartbreak": -3,
    "💔": -3, "lame": -2, "failed": -3, "rip": -2, "lied": -3, "ugh": -2, "worstever": -4,
    "garbage": -3, "sucks": -3, "trashiest": -3, "terribad": -3, "crap": -3, "annoying": -2,
    "disgusting": -3, "failures": -3, "horrible": -3, "losers": -3,

    # Internet slang & emojis
    "😂": 2, "🤣": 2, "😭": -2, "😅": 1, "😡": -3, "❤️": 3, "❤": 3, "💵": 1, "🙌": 2, "🤗": 2,
    "🎉": 2, "🌟": 2, "👩": 1, "🇺🇸": 0, "🌏": 0, "omg": 2, "lmao": 2, "lol": 1, "funneh": 2,
    "funnyhaha": 2, "hahaha": 2, "rofl": 2, "xd": 2, "bruh": -1, "smh": -2, "wtf": -2, "fml": -2,
    "gg": 2, "yass": 2, "yaaas": 2, "lit": 2, "pog": 2, "poggers": 2, "rip": -2, "rippp": -2,
    "ripninja": -2,

    # YouTube specific phrases
    "mostdisliked": -4, "mosthated": -4, "dislikecount": -2, "clickthedislike": -3,
    "funneh": 2, "youtube": 0, "reupload": 0, "rewind": 0, "viral": 1, "trending": 1, "sub": 1,
    "subscribed": 1, "subscribers": 0, "views": 0, "millionviews": 1, "milliondislikes": -3,
    "ripvideo": -2, "ripninjabusdriver": -2,

    # Repeated letters or emphasis
    "awwwww": 2, "nooooo": -3, "yeeeeees": 2, "loooool": 2, "hahahahah": 2, "omgggg": 2,

    # Misc positive words
    "amazingvideo": 3, "sofunny": 2, "greatjob": 3, "wellplayed": 2, "impressed": 2, "legend": 3,
    "epicwin": 3, "sohappy": 2, "thankyou": 2, "appreciate": 2, "bravo": 3, "kudos": 2,

    # Misc negative words
    "disaster": -3, "failvideo": -3, "ruined": -3, "destroyed": -3, "terribad": -3, "worstvideo": -4,
    "unwatchable": -3, "trashvideo": -3, "lamevideo": -3, "annoyed": -2, "hateit": -3,

    # Neutral fillers
    "like": 1, "comment": 0, "share": 0, "subscribe": 0, "video": 0, "link": 0, "channel": 0,
    "view": 0, "views": 0, "time": 0, "minute": 0
}


def score_comments(comments):
    total_score = 0
    for comment in comments:
        words = comment.lower().split()
        for word in words:
            # Remove punctuation for better matching
            word = word.strip(".,!?*()[]{}\"':;")
            if word in sentiment_weights:
                total_score += sentiment_weights[word]
    return total_score


def map_score_to_verdict(score):
    if score > 20:
        return "Positive"
    elif score > 5:
        return "Slightly Positive"
    elif score == 0:
        return "Neutral"
    elif score > -5:
        return "Slightly Negative"
    else:
        return "Negative"
