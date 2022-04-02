#!/usr/bin/python
from flask import Flask, request  # redirect, url_for, request
import json


# PAST_CONVERSATIONS is a list of dicts {"utterance": <msg>, "intent": <intent>}
with open("./app/prior_conversations.json") as json_file:
    PAST_CONVERSATIONS = json.load(json_file)
    PAST_CONVERSATIONS = PAST_CONVERSATIONS["chatLog"]


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/health', methods=['GET'])
def success():
    return "<p>Service is up and running!</p>"


# takes "message", returns intent
@app.route('/detect_intent/<message>', methods=['POST'])
def detect_intent(message: str) -> float:
    """
    TEST CASES

    Input: "OK, your order is a large pizza and garlic bread."
    Output: "ConfirmItem"

    Input: "Ready in 30"
    Output: "DurationBeforePickupAnswer"
    """
    # message = request.args.get('message')
    print(request.form)
    print(request.form.get('message'))
    # return request.form
    # jaccard_vals = [jaccard_similarity(message, s) for s in PAST_CONVERSATIONS]
    jaccard_vals = []
    for chat_log in PAST_CONVERSATIONS:
        j_val = jaccard_similarity(message, chat_log['utterance'])
        jaccard_vals.append((j_val, chat_log['intent']))
    # after populating a list of `(jaccard_vals, intent)``, sort by the jaccard
    # value and return the intent corresponding to the largest one
    jaccard_vals.sort()
    return jaccard_vals[-1][1]


def jaccard_similarity(s1: str, s2: str) -> float:
    """
    TEST CASES

    "OK, and what's your order?"
    "I'm ready for your order."
    Output: 0.25

    "I'd like a medium supreme pizza."
    "Can I get a pepperoni pizza, medium?"
    Output: 0.3

    "Hi there, how can I help you?"
    "Hi there, how can I help you?"
    Output: 1.0

    "Is your order for one large pizza?"
    "Thanks, please come again."
    Output: 0.0
    """
    # first remove punctuation, namely commas and end-of-sentence characters
    punc = '!?.,'
    for char in s1:
        if char in punc: s1 = s1.replace(char, '')
    for char in s2:
        if char in punc: s2 = s2.replace(char, '')
    word_set1 = set(s1.split())
    word_set2 = set(s2.split())
    intersection = len(list(word_set1.intersection(word_set2)))
    excl_union = (len(word_set1) + len(word_set2)) - intersection
    return float(intersection) / excl_union


if __name__ == "__main__":
    # just run the app on localhost, port 5000
    app.run(host="0.0.0.0", port=5000)
