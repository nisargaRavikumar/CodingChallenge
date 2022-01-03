#!/usr/bin/env python
# coding: utf-8

# In[26]:


import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

urls_text_file_path = r"E:\noknok\urls.txt"
test_words_file_path = r"E:\noknok\words.txt"

f_ptr_url = open(urls_text_file_path,"r")
w_ptr_url = open(test_words_file_path,"r")
urls_data = f_ptr_url.readlines()
words = w_ptr_url.readlines()
words_data=[re.sub(r'\n', '', w) for w in words ]
print(words_data)
print(urls_data)


def remove_stop_words(sentence):
    # print("sentence ===",sentence)
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    return filtered_sentence

def parse_output(c_p_obj):
    word_list = []
    for x in c_p_obj:
        key = x
        value = c_p_obj[key]
        if len(key) > 5 and (bool(re.match('^[a-zA-Z0-9]*$', key)) == True):
            word_list.append(key)

    sentence = ' '.join(word for word in word_list)
    filtered_sentence = remove_stop_words(sentence)
    return Counter(filtered_sentence)

def read_and_process_url(url):

    print("URL ====> ",url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")

    text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))


    c_p_obj = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    c_p = parse_output(c_p_obj)


    # We get the words within divs
    text_div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
    
    c_div_obj = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
    c_div = parse_output(c_div_obj)
    # We sum the two counters and get a list with words count from most to less common
    total = c_div + c_p
    list_most_common_words = total.most_common() 

    #print(list_most_common_words)
    return list_most_common_words

def process_output(output_list):
    result_dict = {}
#     for word in words_data:
#         if word in output_list:
#             if word not in result_dict.keys():
#                 result_dict[word] = 1
#             else:
#                 result_dict[word] += 1
#     return result_dict
    

    for common_words in output_list:
        for x in common_words:
            word = x[0]
            value = x[1]

            if word in words_data:
                if word not in result_dict.keys():
                    result_dict[word] = value
                else:
                    result_dict[word] +=  value
    for word in words_data:
        if word not in result_dict:
            result_dict[word]=0
  

    return result_dict


def main():
    output_list = []
    for url in urls_data:
        common_words = read_and_process_url(url)
        output_list.append(common_words)
#         print(output_list)

    results = process_output(output_list)
    print("**********************************************************************************")
    print("Top three words are:")
    results=Counter(results)
    results.most_common()
    for k, v in results.most_common(3):
        print('%s- %i' % (k, v))
        
    print("**********************************************************************************")
    print("Total number of occurance of each word in the list ")
    for k, v in results.most_common():
        print('%s- %i' % (k, v))
main()


# In[ ]:





# In[ ]:





# In[ ]:




