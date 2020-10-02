import json
import requests
import nltk
import streamlit as st
import numpy
import plotly.express as px
import pandas as pd
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from pprint import pprint


from wordcloud import WordCloud
import matplotlib.pyplot as plt

# nltk.download("punkt")
# nltk.download("stopwords")

api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

# streamlit interface
st.title("COP 4813 - Web Application Programming")
st.title("Project 1")

st.write("## Part A - The Stories API")

st.write("This app uses the NYT Top Stories API to display the most common words used "
         "in the top current articles. It then converts these words into a WordCloud image "
         "for the user.")

st.subheader("I - Topic Selection")

name = st.text_input(
    "Please enter your name"
)

#Q2 - Select a topic
topic = st.selectbox(
    "Select a topic of your interest",
    ["arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine",
     "movies", "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview",
     "technology", "theater", "t-magazine", "travel", "upshot", "us", "world"]
)
'Hi' ' ' + name + ',' ' ' + 'your topic of interest is',topic

top_url = "https://api.nytimes.com/svc/topstories/v2/" + topic + ".json?api-key=" + api_key

response = requests.get(top_url).json()

main_functions.save_to_file(response,"JSON_Files/response.json")

my_articles = main_functions.read_from_file("JSON_Files/response.json")

print(type(my_articles))

# pprint(my_articles)

str1 = ""

for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

# print(str1)

sentences = sent_tokenize(str1)

# print(len(sentences))
#
# print(sentences)

words = word_tokenize(str1)

# print(len(words))
#
# print(words)

fdist = FreqDist(words)

# print(fdist.most_common(10))

words_no_punc = []

for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

# print(words_no_punc)

fdist2 = FreqDist(words_no_punc)

pprint(fdist2.most_common(10))

stopwords = stopwords.words("english")

# print(stopwords)

clean_words=[]

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

print(len(clean_words))

fdist3 = FreqDist(clean_words)

pprint(fdist3.most_common(10))

wordcloud = WordCloud().generate(str1)

plt.figure(figsize=(12,12))
plt.imshow(wordcloud)

plt.axis("off")
plt.show()

# 2 - Frequency Distribution
st.subheader("II - Frequency Distribution")

if st.checkbox("Click here to display a frequency distribution graph"):
    most_common = pd.DataFrame(fdist3.most_common((10)))
    df = pd.DataFrame({"words": most_common[0],"count":most_common[1]})
    fig = px.line(df, x="words", y="count",title='')
    st.plotly_chart(fig)

# 3 - Wordcloud
st.subheader("III - Wordcloud")
if st.checkbox("Click here to generate a WordCloud for your interest"):
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.show()
    st.pyplot()

# Part B - preferred set of articles
st.write("## Part B - Most Popular Articles")

st.write("Would you like to see the most shared, viewed, or emailed articles?")

share_type = article_set = st.selectbox(
"Select your preferred set of articles",
    ["shared","emailed","viewed"]
)

# period of time
period = article_time = st.selectbox(
"Select the age of your article (in days)",
    ["1","7","30"]
)

popular_url = "https://api.nytimes.com/svc/mostpopular/v2/" + share_type + "/" + period + ".json?api-key=" + api_key

response = requests.get(popular_url).json()

main_functions.save_to_file(response, "JSON_Files/response2.json")

my_articles1 = main_functions.read_from_file("JSON_Files/response2.json")

str2 = ""

for i in my_articles1["results"]:
    str2 = str2 + i["abstract"]

# Part B - wordcloud
if st.checkbox("Click here to generate a WordCloud for your topic"):
    wordcloud1 = WordCloud().generate(str2)
    plt.figure()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.imshow(wordcloud1)
    plt.axis("off")
    plt.show()
    st.pyplot()

