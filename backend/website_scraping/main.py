# -*- coding: utf-8 -*-
# Master script for the plagiarism-checker
# Coded by: Shashank S Rao

# import other modules
from cosineSim import cosineSim
from htmlstrip import strip_tags
from extractdocx import docxExtract

# import required modules
import codecs
import traceback
import sys
import operator
import urllib.parse
import urllib.request
import json
import re
import time

# Given a text string, remove all non-alphanumeric
# characters (using Unicode definition of alphanumeric).
def getQueries(text, n):
    sentenceEnders = re.compile(r'[.!?]')
    sentenceList = sentenceEnders.split(text)
    sentencesplits = []
    for sentence in sentenceList:
        x = re.compile(r'\W+', re.UNICODE).split(sentence)
        x = [ele for ele in x if ele != '']
        sentencesplits.append(x)
    finalq = []
    for sentence in sentencesplits:
        l = len(sentence)
        l = l // n
        index = 0
        for i in range(0, l):
            finalq.append(sentence[index:index + n])
            index = index + n - 1
        if index != len(sentence):
            finalq.append(sentence[len(sentence) - index:len(sentence)])
    return finalq

# Search the web for the plagiarised text
# Calculate the cosineSimilarity of the given query vs matched content on google
# This is returned as 2 dictionaries
def searchWeb(text, output, c):
    try:
        query = urllib.parse.quote_plus(text)
        if len(query) > 60:
            return output, c

        # using googleapis for searching web
        base_url = 'https://www.googleapis.com/customsearch/v1?'
        params = {
            'key': 'AIzaSyBiihlzs7zIUJeXoe3N9fBDlNAGB9l_Cow',
            'cx': '067ffae8ffb6443ee',
            'q': query
        }
        url = base_url + urllib.parse.urlencode(params)
        request = urllib.request.Request(url, headers={'Referer': 'Python'})

        while True:
            try:
                response = urllib.request.urlopen(request)
                results = json.load(response)
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"HTTP Error 429: Too Many Requests. Retrying after 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"HTTP Error: {e.code} - {e.reason}")
                    return output, c
            except urllib.error.URLError as e:
                print(f"URL Error: {e.reason}")
                return output, c

        try:
            if 'items' in results:
                for item in results['items']:
                    content = item.get('snippet', '')
                    link = item.get('link', '')
                    if link in output:
                        output[link] += 1
                        c[link] = (c[link] * (output[link] - 1) + cosineSim(text, strip_tags(content))) / output[link]
                    else:
                        output[link] = 1
                        c[link] = cosineSim(text, strip_tags(content))
        except Exception as e:
            print(f"Error processing search results: {e}")
            return output, c
    except Exception as e:
        print(f"Error in searchWeb: {e}")
    return output, c

# Use the main function to scrutinize a file for plagiarism
def main():
    # n-grams N VALUE SET HERE
    n = 9
    if len(sys.argv) < 3:
        print("Usage: python main.py <input-filename>.txt <output-filename>.txt")
        sys.exit()
    if sys.argv[1].endswith(".docx"):
        t = docxExtract(sys.argv[1])
    else:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                t = f.read()
        except:
            print("Invalid Filename")
            print("Usage: python main.py <input-filename>.txt <output-filename>.txt")
            sys.exit()
    queries = getQueries(t, n)
    q = [' '.join(d) for d in queries]
    found = []
    # using 2 dictionaries: c and output
    # output is used to store the url as key and number of occurrences of that url in different searches as value
    # c is used to store url as key and sum of all the cosine similarities of all matches as value
    output = {}
    c = {}
    i = 1
    count = len(q)
    if count > 100:
        count = 100
    for s in q[:100]:
        output, c = searchWeb(s, output, c)
        msg = "\r" + str(i) + "/" + str(count) + " completed..."
        sys.stdout.write(msg)
        sys.stdout.flush()
        i = i + 1
        time.sleep(1)  # Delay to avoid rate limiting
    with open(sys.argv[2], "w", encoding='utf-8') as f:
        for ele in sorted(c.items(), key=operator.itemgetter(1), reverse=True):
            f.write(str(ele[0]) + " " + str(ele[1] * 100.00))
            f.write("\n")
    print("\nDone!")

if __name__ == "__main__":
    try:
        main()
    except:
        # writing the error to stdout for better error detection
        error = traceback.format_exc()
        print("\nUh Oh!\n" + "Plagiarism-Checker encountered an error!:\n" + error)
