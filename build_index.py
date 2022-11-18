import os
import sys
import pickle
import json
from math import log
from bs4 import BeautifulSoup

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import 	WordNetLemmatizer

lem = WordNetLemmatizer()
english_stopwords = stopwords.words('english')
TITLE, BODY = "title", "body"
STRONG, BOLD, H1, H2, H3 = 'strong', 'b', 'h1', 'h2', 'h3'
global index_data

# conver text to valid token
def text_to_tokens(text):
    text = text.lower()     # lowercase
    tokens = word_tokenize(text)
    valid_tokens = []
    for token in tokens:
        if "." in token: #special token
            for x in token.split("."):
                if is_valid_token(x):
                    valid_tokens.append(x)

        token = is_valid_token(token)
        if token:
            valid_tokens.append(token)
    return valid_tokens

# judge token is the valid token
def is_valid_token(token):
    if len(token) == 0:
        return

    if token.isnumeric():
        return

    if not token.isalnum():
        return

    if token in english_stopwords:
        return

    token = lem.lemmatize(token)
    return token

#generate inverted index and record the inverted index to a seperate file
def build_index_file(directory):
    global index_data
    index_data = {TITLE: {}, BODY: {}, STRONG: {}, BOLD: {}}  # all index data here
    with open(os.path.join(directory, "bookkeeping.json")) as f:
        bookkeeping = json.load(f)

    parse_num, fail_num = 0, 0,

    for doc in bookkeeping:
        # try:
        print("reading "+doc)
        with open(os.path.join(directory, doc), "rb") as f:
            bs = BeautifulSoup(f, "lxml")

            index_sub(bs, doc, TITLE)
            index_sub(bs, doc, STRONG)
            index_sub(bs, doc, BOLD)

            index_content(bs, doc, index_data[BODY])

        parse_num += 1

    # calculate tf-idf

    for token in index_data[BODY]:
        idf = log(parse_num / (len(index_data[BODY][token])), 10)
        for doc in index_data[BODY][token]:
            index_data[BODY][token][doc] *=  idf
    index_data["number_of_doc"] = parse_num

    #sort the body index by tf-idf
    for token in index_data[BODY]:
        #sort body index by its tf-idf
        index_data[BODY][token] = sorted(index_data[BODY][token].items(), key=lambda x: -index_data[BODY][token][x[0]])
    with open("index_data.data", "wb") as f:
        pickle.dump(index_data, f)
    print("finish index")
    print("total files: {}, unique tokens: {}".format(parse_num, len(index_data[BODY])))


# build index for title, bold, h1, h2, h3
def index_sub(bs, doc, element):
    global index_data
    for node in bs.find_all(element):
        for token in text_to_tokens(node.text):
            if token not in index_data[element]:
                index_data[element][token] = {doc}
            else:
                index_data[element][token].add(doc)

# build index for content body
def index_content(bs, doc, index):
    content = bs.get_text()
    tokens = text_to_tokens(content)
    count = {} #count word frequency
    for token in tokens:
        if token not in count:
            count[token] = 1
        else:
            count[token] += 1

# build index for title, bold, h1, h2, h3
    for node in bs.find_all(STRONG):
        for token in text_to_tokens(node.text):
            if token not in count:
                count[token] = 1.5
            else:
                count[token] += 1.5

    for node in bs.find_all(BOLD):
        for token in text_to_tokens(node.text):
            if token not in count:
                count[token] = 1.5
            else:
                count[token] += 1.5

    for node in bs.find_all(TITLE):
        for token in text_to_tokens(node.text):
            if token not in count:
                count[token] = 2
            else:
                count[token] += 2

    for token in count:
        # edit tf for each token
        if token not in index:
            index[token] = {doc: log(count[token], 10) + 1}
        else:
            index[token][doc] = log(count[token], 10) + 1



if __name__ == '__main__':
    """
    if len(sys.argv) == 2:
        data_directory = sys.argv[1]
        build_index_file(data_directory)
    else:
        print("usage: python build_index.py path_of_data")
    """
    build_index_file(r'D:\UCI\Winter2022\CS121\Project3\CS121-Project3\WEBPAGES_RAW')

