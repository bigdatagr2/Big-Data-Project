from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)
es = Elasticsearch('http://192.168.99.100', port=9201)

@app.route('/')
def home():
    return render_template('search.html')

def countLanguages(res):
    xsplit = {}
    for item in res['aggregations']['count']['buckets']:
        dictItem = dict(item)
        x = dictItem['key']
        y = dictItem['doc_count']
        for z in x.split(","):
            if z not in xsplit:
                xsplit[z] = y
            else:
                xsplit[z] += y
           
    dictxSplit = dict(xsplit)
    xjoin = ''            
    for key, value in dictxSplit.items(): 
        xjoin = "%s  %s(%s)" % (xjoin,key,value) 
    return xjoin
    
@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    target = request.form["targettable"]
    res=""
    xjoin =''
    search_term = request.form["input"]
    if target == "Commits":
        res = es.search(
            index="engine-recherche",
            body={ "size":250,
                    "query": {
                        "bool": {
                            "should": [
                                {"wildcard":{"committer_name": "*" + search_term + "*"}},
                                {"wildcard":{"committer_date": "*" + search_term + "*"}},
                                {"wildcard":{"subject": "*" + search_term + "*"}},
                                {"wildcard":{"message": "*" + search_term + "*"}},
                                {"wildcard":{"repo_name": "*" + search_term + "*"}},
                                {"wildcard":{"language_name": "*" + search_term + "*"}},
                                { 
                                     "bool": {
                                        "should": [
                                           {"match_phrase": {"committer_name": search_term}},
                                           {"match_phrase": {"committer_date": search_term}},
                                           {"match_phrase": {"subject": search_term}},
                                           {"match_phrase": {"message": search_term}},
                                           {"match_phrase": {"repo_name":  search_term}},
                                           {"match_phrase": {"language_name":  search_term}}
                                        ] 
                                    }
                                }
                            ]
                        }                                                                  
                    },
                    "sort": [
                            { "_score": { "order": "desc" }}                  
                    ],
                    "aggs": {
                        "count": {
                            "terms" : {"field": "language_name"}
                        }
                    }
                }
            
        )
    else:
        if target == "Contents":
            res = es.search(
                index="contents", 
                #size=0, 
                body={"size":250,
                    "query": {
                        "bool": {
                            "should": [
                                {"wildcard":{"id": "*" + search_term + "*"}},
                                {"wildcard":{"content": "*" + search_term + "*"}},
                                {"wildcard":{"repo_name": "*" + search_term + "*"}},
                                {"wildcard":{"language_name": "*" + search_term + "*"}},
                                { 
                                    "bool": {
                                        "should": [
                                            {"match_phrase": {"id": search_term}},
                                            {"match_phrase": {"content": search_term}},
                                            {"match_phrase": {"repo_name": search_term}},
                                            {"match_phrase": {"language_name": search_term}}
                                        ] 
                                    }
                                }
                            ]
                        }                                                                  
                    },
                    "sort": [
                        { "_score": { "order": "desc" }}                  
                    ],
                    "aggs": {
                        "count": {
                            "terms" : {"field": "language_name"}
                        }
                    }
                }
            )
    xjoin = countLanguages(res)
    return render_template('results.html', res=res, target=target, xjoin=xjoin_ , searchTerm=search_term)
   
    
if __name__ == '__main__':
        app.secret_key = 'mysecret'
        app.run(host='0.0.0.0',port=5000)