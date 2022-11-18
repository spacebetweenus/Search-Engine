import pickle
import json
import os
from numpy import dot
from numpy.linalg import norm
from math import log


from build_index import is_valid_token, BODY


with open("index_data.data", "rb") as f:
    index = pickle.load(f)

with open(os.path.join(r'E:\UCI\2022 Winter\COMPSCI 121\P3\webpages\WEBPAGES_RAW', "bookkeeping.json")) as f:
    bookkeeping = json.load(f)

def searchGUI(s):
    returnstr = ''
    term = s
    if term.isspace() or term == "":
        return "Invalid Input"
    body_index = index[BODY]
    term_list = term.split()
    if len(term_list) == 1:
        token = is_valid_token(term.lower())
        if token:
            if token in body_index:
                docs = body_index[token]
                # print("found {} results, list 20".format(len(docs)))
                #sorted_docs = sorted(docs.keys(), key=lambda x: -docs[x])[:20]
                for id, doc in enumerate(docs):
                    # print("{}: {} ({})".format(id + 1, bookkeeping[doc[0]], doc[0]))
                    returnstr += "{}: {} ({})\n".format(id + 1, bookkeeping[doc[0]], doc[0])
                    # print("{}: {} ({})".format(id + 1, bookkeeping[doc[0]], doc[0]))
            else:
                return "No result found!"
        else:
            return "Invalid token!"
    else:
        term_dict = {}
        for x in term_list:
            x = is_valid_token(x.lower())
            if x in body_index:
                term_dict[x] = log(index["number_of_doc"] / len(body_index[x]), 10)
            else:
                term_dict[x] = 0
        sort_order = sorted(term_dict.keys(), key=lambda t: -term_dict[t])
        #build champion list
        champion_list = []
        for term in sort_order:
            if term in body_index:
                champion_list += [x[0] for x in body_index[term][:200]]
                if len(champion_list) >= 200:
                    break
        if not champion_list:
            return "Invalid or wrong token!"
        else:
            query_frenquency = [term_dict[x] for x in sort_order] #for calculate id-idf
            champion_list = set(champion_list)
            champion_list_freqency = {x: [] for x in champion_list}
            for frequncy_count, single_term in enumerate(sort_order, 1):
                #if single_term in the body_index we update each doc in the champion_list_freqency
                if single_term in body_index:
                    for single_pair in body_index[single_term]:
                        if single_pair[0] in champion_list_freqency:
                            champion_list_freqency[single_pair[0]].append(single_pair[1])
                #champion_list_freqency update if not have that term
                for doc in champion_list_freqency:
                    if len(champion_list_freqency[doc]) != frequncy_count:
                        champion_list_freqency[doc].append(0)
            cosine_res = [(x, dot(champion_list_freqency[x], query_frenquency)/norm(champion_list_freqency[x]))
                          for x in champion_list_freqency]
            '''
            print(champion_list)
            print(len(champion_list))
            for x in champion_list_freqency:
                print(x + " ")
                print(champion_list_freqency[x])
            print("\n"+"result")
            print(cosine_res)
            '''
            
            #print(sorted(cosine_res, key=lambda t: -t[1])[:20])
            #top 20 result
            for id, doc in enumerate(sorted(cosine_res, key=lambda t: -t[1])):
                returnstr += "{}: {} ({})\n".format(id + 1, bookkeeping[doc[0]], doc[0])
                # print("{}: {} ({})".format(id + 1, bookkeeping[doc[0]], doc[0]))
    return returnstr





def search():
    while True:
        term = ""
        while term.isspace() or term == "":
            term = input("input search term: ")
        body_index = index[BODY]
        term_list = term.split()
        if len(term_list) == 1:
            token = is_valid_token(term.lower())
            if token:
                if token in body_index:
                    docs = body_index[token]
                    print("found {} results, list 20".format(len(docs)))
                    #sorted_docs = sorted(docs.keys(), key=lambda x: -docs[x])[:20]
                    for id, doc in enumerate(docs[:20]):
                        print("{}: {} ({})".format(id + 1, bookkeeping[doc[0]], doc[0]))
                else:
                    print("No result found!")
            else:
                print("invalid token!")
        else:
            term_dict = {}
            for x in term_list:
                x = is_valid_token(x.lower())
                if x in body_index:
                    term_dict[x] = log(index["number_of_doc"] / len(body_index[x]), 10)
                else:
                    term_dict[x] = 0
            sort_order = sorted(term_dict.keys(), key=lambda t: -term_dict[t])
            #build champion list
            champion_list = []
            for term in sort_order:
                if term in body_index:
                    champion_list += [x[0] for x in body_index[term][:200]]
                    if len(champion_list) >= 200:
                        break
            if not champion_list:
                print("invalid or wrong token!")
            else:
                query_frenquency = [term_dict[x] for x in sort_order] #for calculate id-idf
                champion_list = set(champion_list)
                champion_list_freqency = {x: [] for x in champion_list}
                for frequncy_count, single_term in enumerate(sort_order, 1):
                    #if single_term in the body_index we update each doc in the champion_list_freqency
                    if single_term in body_index:
                        for single_pair in body_index[single_term]:
                            if single_pair[0] in champion_list_freqency:
                                champion_list_freqency[single_pair[0]].append(single_pair[1])
                    #champion_list_freqency update if not have that term
                    for doc in champion_list_freqency:
                        if len(champion_list_freqency[doc]) != frequncy_count:
                            champion_list_freqency[doc].append(0)
                cosine_res = [(x, dot(champion_list_freqency[x], query_frenquency)/norm(champion_list_freqency[x]))
                              for x in champion_list_freqency]
                '''
                print(champion_list)
                print(len(champion_list))
                for x in champion_list_freqency:
                    print(x + " ")
                    print(champion_list_freqency[x])
                print("\n"+"result")
                print(cosine_res)
                '''
                
                #print(sorted(cosine_res, key=lambda t: -t[1])[:20])
                #top 20 result
                for id, doc in enumerate(sorted(cosine_res, key=lambda t: -t[1])[:20]):
                    print("{}: {} ({})".format(id + 1, bookkeeping[doc[0]], doc[0]))



if __name__ == '__main__':
    # with open("index_data.data", "rb") as f:
    #     index = pickle.load(f)

    # with open(os.path.join(r'D:\UCI\Winter2022\CS121\Project3\CS121-Project3\WEBPAGES_RAW', "bookkeeping.json")) as f:
    #     bookkeeping = json.load(f)
    search()
