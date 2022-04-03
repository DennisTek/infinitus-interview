#!/usr/bin/python
from flask import Flask, request, Response
import json


# PAST_CONVERSATIONS is a list of dicts {"utterance": <msg>, "intent": <intent>}
with open("./app/prior_conversations.json") as json_file:
    PAST_CONVERSATIONS = json.load(json_file)
    PAST_CONVERSATIONS = PAST_CONVERSATIONS["chatLog"]


app = Flask(__name__)


def jaccard_similarity(s1: str, s2: str) -> float:
    # first remove punctuation, namely commas and end-of-sentence characters
    punc = '!?.,;'
    for char in s1:
        if char in punc:
            s1 = s1.replace(char, '')
    for char in s2:
        if char in punc:
            s2 = s2.replace(char, '')
    # now split words, lowercase them, and put into sets (no dupes)
    word_set1 = set(map(str.lower, s1.split()))
    word_set2 = set(map(str.lower, s2.split()))
    # calcluate intersection, exclusive union, and return result
    intersection = len(word_set1.intersection(word_set2))
    excl_union = (len(word_set1) + len(word_set2)) - intersection
    return float(intersection) / excl_union


@app.route('/health', methods=['GET'])
def health():
    return "<p>Service is up and running!</p>"


# takes "message", returns intent
@app.route('/detect_intent', methods=['POST'])
def detect_intent() -> float:
    message = request.form.get('message')
    if not message:
        return Response("'message' parameter not found, please supply.", status=422)
    jaccard_vals = []
    for chat_log in PAST_CONVERSATIONS:
        j_val = jaccard_similarity(message, chat_log['utterance'])
        jaccard_vals.append((j_val, chat_log['intent']))
    # after populating a list of `(jaccard_vals, intent)``, sort by the jaccard
    # value and return the intent corresponding to the largest one
    jaccard_vals.sort()
    return jaccard_vals[-1][1]


if __name__ == "__main__":
    # just run the app on localhost, port 5000
    app.run(host="0.0.0.0", port=5000)
