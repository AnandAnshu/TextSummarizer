from flask import Flask, request, render_template

import numpy as np
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

application=Flask(__name__)

app=application

#Route for a home page
@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/predictdata',methods=['GET','POST'])
def summarize():
    if request.method=='GET':
        return render_template('home.html')
    else:
        text=request.form.get('message')
            
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tokens = [token.text for token in doc]
    punct =  punctuation + '\n'
    word_freq = {}

    stop_words = list(STOP_WORDS)

    for word in doc:
        if word.text.lower() not in  stop_words:
            if word.text.lower() not in punct:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1  

    max_freq = max(word_freq.values())
    sent_tokens = [sent for sent in doc.sents]
    sent_score = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower()in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text.lower()]
                else:
                    sent_score[sent] += word_freq[word.text.lower()]  

    summary = nlargest(n = 8, iterable= sent_score, key = sent_score.get)
    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)
    len_text= len(text)
    len_summ= len(summary)
    return render_template('home.html',article=text, lena=len_text, lens=len_summ, results=summary)

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)      