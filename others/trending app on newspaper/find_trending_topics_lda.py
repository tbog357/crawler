import os
import json
import time
import pickle
import numpy as np
import pandas as pd

from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim.parsing.preprocessing import strip_punctuation, strip_numeric, strip_multiple_whitespaces, strip_non_alphanum

def preprocess(sample):
    processed = strip_punctuation(sample)
    processed = strip_non_alphanum(processed)
    processed = strip_numeric(processed)
    processed = strip_multiple_whitespaces(processed)
    return processed

def keywords_extraction():
    return 

NUMBER_WORDS = 20
NUMBER_TOPICS = 5
TOPIC_THRESHOLD = 0.1
# load data
t0 = time.time()
DATA_FOLDER = "crawler/data"
contents = []
sources = []
titles = []
for file_name in os.listdir(DATA_FOLDER):
    # print(file_name)
    with open(os.path.join(DATA_FOLDER, file_name), "r", encoding="utf-8") as file:
        data = json.load(file)
    # print(data)
    for article in data:
        if article["content"].strip() != "" and article["link"] not in sources:
            contents.append(preprocess(article["content"] + " " + article["title"]))
            sources.append(article["link"])
            titles.append(article["title"])

print("Number of articles: ", len(contents)) 
print("Load data time: ", time.time() - t0)

t0 = time.time()
count_vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=10)
count_vectorizer.fit(contents)
features = count_vectorizer.get_feature_names()
# import stopwords 
with open("vietnamese-stopwords.txt", "r", encoding="utf-8") as file:
    stopwords = file.readlines()
stopwords = [d.strip() for d in stopwords]
print("Number of stopword", len(stopwords))

new_features = []
for term in features:
    if term not in stopwords:
        new_features.append(term)
print("Number of terms", len(new_features))
tfidf_vectorizer = CountVectorizer(ngram_range=(1, 2), vocabulary=new_features)
tfidf_data = tfidf_vectorizer.fit_transform(contents)

print("Feature Extraction time: ", time.time() - t0)

t0 = time.time()
lda = LDA(n_components=NUMBER_TOPICS, random_state=1, max_iter=30)
y_pred = lda.fit_transform(tfidf_data)
y_pred[y_pred <= TOPIC_THRESHOLD] = 0
topic_strengs = np.sum(y_pred, axis=0)
print(np.sum(y_pred, axis=0))
print("LDA time: " ,time.time() - t0)


def print_topic(model, vectorizer, n_top_words):
    words = vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\n Topic #%d:" %topic_idx)
        print(", ".join([words[i] for i in topic.argsort()[:-n_top_words-1:-1]]))

idx_article_cluster = [[] for i in range(NUMBER_TOPICS)]
for idx_article, y in enumerate(y_pred):
    idx_cluster = np.argmax(y)
    idx_article_cluster[idx_cluster].append([idx_article, y[idx_cluster]])

# sort cluster follow number of articles
num_articles = []
for idx, cluster in enumerate(idx_article_cluster):
    num_articles.append(len(cluster))
# num_articles = np.count_nonzero(y_pred, axis=0)
num_articles = np.array(num_articles)
print(num_articles)
print(sum(num_articles))
topic_strengs = topic_strengs / num_articles
sorted_cluster = np.argsort(topic_strengs)[::-1]
print(sorted_cluster)
topics = np.array(lda.components_, dtype=object)
idx_article_cluster = np.array(idx_article_cluster, dtype=object)
topics = topics[sorted_cluster]
idx_article_cluster = idx_article_cluster[sorted_cluster]

words = tfidf_vectorizer.get_feature_names()
with open("words.txt", "w", encoding="utf-8") as file:
    words_copy = words.copy()
    words_copy = sorted(words_copy, key=lambda x: len(x.split()))
    for w in words_copy:
        file.write(w + "\n")
keywords = []
titles_real = []

for idx, cluster in enumerate(idx_article_cluster):
    idx_article_cluster[idx] = sorted(cluster, key=lambda x: x[1], reverse=True)
    print("Cluster {} have {}".format(idx, len(cluster)))
    topic = topics[idx]
    id_topic_streng = sorted_cluster[idx]
    print("Topic streng: ", topic_strengs[id_topic_streng])
    print(", ".join([words[i] for i in topic.argsort()[:-NUMBER_WORDS-1:-1]]))
    keywords.append(", ".join([words[i] for i in topic.argsort()[:-NUMBER_WORDS-1:-1]]))
    print(idx_article_cluster[idx][:3])
    # print(contents[idx_article_cluster[idx][0][0]])
    all_titles = ""
    for i in range(3):    
        print(sources[idx_article_cluster[idx][i][0]])
    for i in range(10):    
        #print(titles[idx_article_cluster[idx][i][0]])
        all_titles += titles[idx_article_cluster[idx][i][0]] + "\n"
    print(all_titles)
    titles_real.append(all_titles)
                                  
                                  

# write result to csv [num_idx_cluster, keywords, title, link , sources]
result = {"keywords": keywords, "titles": titles_real}

df = pd.DataFrame(result, columns= ['keywords', 'titles'])
df.to_csv("result_lda.csv", index=False)