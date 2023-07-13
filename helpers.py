## Imports
import bs4 as bs
import urllib.request
import re
import nltk
import nltk.tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import heapq
import math
import numpy as np
from transformers import T5Tokenizer, T5ForConditionalGeneration
stop_words = set(stopwords.words('english'))

## IDF Calculation
def idf(sent_list, word_sent):
    return math.log(len(sent_list)/word_sent)

## Pull Wikipedia Text 
def pull_text(article_url):
    
    scraped_data = urllib.request.urlopen(article_url)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article,'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    return article_text

## Format Text
def fix_it_up(article_text):
    ## Remove square brackets and extra spaces 
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text) # Remove extra space 
    ## Remove everything else 
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    return formatted_article_text, article_text

## Tokenize Sentences, Find Word Frequency
def sentence_tokenize(formatted_article_text, article_text, stop_words = stop_words):
    
    ## Tokenize the sentences in the OG article text, initialize stopwords
    sentence_list = nltk.sent_tokenize(article_text)
    stp_wds = stop_words
    word_frequencies = {} # A dictionary of words and how often they show up 
    ## Fill up word_freq dict with (you guessed it) word frequencies
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stp_wds:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies, sentence_list

# Create IDF values for individual words 
def word_idf_create(sent_list, word_freq):
    word_idf = {}
    for word in word_freq.keys():
        word_idf[word] = idf(sent_list, word_freq[word])
    return word_idf

## Find IDF Values for Sentences
def sent_idf_create(sent_list, word_idf):
    sent_vec = [word_tokenize(val) for val in sent_list]
    sent_idf = {}
    for sent in sent_vec:
        sent_counter = 0.0
        sent_idx = sent_vec.index(sent)
        for word in sent:
            if word in word_idf.keys():
                sent_counter += word_idf[word]
        sent_trueVal = sent_list[sent_idx]
        sent_idf[sent_trueVal] = sent_counter
    return sent_idf

## Sort Top N IDF Values
def top_n(sent_idf, num_sents):
    all_sents = list(sent_idf.keys())
    all_stats = list(sent_idf.values())
    final_sents = []
    top_idx = list(np.argsort(all_stats)[-1*num_sents:])
    top_idx.sort()
    for idx in top_idx:
        final_sents.append(all_sents[idx])
    return final_sents

## Full pipeline from wikipedia article
def wiki_to_sents(article_url, num_sents):
    article_text = pull_text(article_url)
    formatted_article_text, article_text = fix_it_up(article_text)
    word_freq, sent_list = sentence_tokenize(formatted_article_text, article_text, stop_words)
    word_F = word_idf_create(sent_list, word_freq)
    sent_F = sent_idf_create(sent_list, word_F)
    top_sents = top_n(sent_F, num_sents=num_sents)
    return top_sents

## Full pipeline from text
def text_to_sents(article_text, num_sents):
    formatted_article_text, article_text = fix_it_up(article_text)
    word_freq, sent_list = sentence_tokenize(formatted_article_text, article_text, stop_words)
    word_F = word_idf_create(sent_list, word_freq)
    sent_F = sent_idf_create(sent_list, word_F)
    top_sents = top_n(sent_F, num_sents=num_sents)
    return top_sents

def abstract_summarize(input_text):
    # Load the T5 tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained('t5-base')
    model = T5ForConditionalGeneration.from_pretrained('t5-base')

    # Preprocess the input text
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors='pt', max_length=512, truncation=True)

    # Generate the summary
    outputs = model.generate(inputs, max_length=150, min_length=40, num_beams=4, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary