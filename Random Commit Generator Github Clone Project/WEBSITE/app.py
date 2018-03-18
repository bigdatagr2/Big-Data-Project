
# A very simple Flask Hello World app for you to get started with...
from datetime import date, datetime
from flask import Flask, flash, redirect, render_template, \
     request, url_for, get_template_attribute
import json
import requests
import paho.mqtt.publish as publish
import datacode as dbHandler
from flask_socketio import SocketIO
from elasticsearch import Elasticsearch
from django.utils.safestring import mark_safe

es = Elasticsearch('http://88.169.46.187', port=9200, timeout=60)

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

jsonData = {'data','Just started ....'}
startTime = date.today()
startCounter = 0



@app.route('/')
def index():
    global jsonData, startTime, startCounter
    return render_template('index.html', data=jsonData,start=startTime,counter=startCounter)

@app.route('/_getLast',methods=['GET', 'POST'])
def get_last():
    print "getlast triggered here ...."
    xres = dbHandler.retrieveLast()
    print ("lastrow is : " , xres)
    return  jsonify(xres)

@app.route('/xpost', methods=['GET', 'POST'])
def xpost():
    global jsonData, startTime, startCounter
    if request.method == 'POST':

        jsonData = json.loads(request.get_data().decode('utf-8'))
#         print('type : %s, data = %s ' % (type(jsonData),jsonData))
        #to MQTT
        # MqttMessage
        publish.single( jsonData['event'] + "/" + jsonData['repo'], jsonData['data'] , hostname="18.188.23.129",port=1883)
        # publish.single("test/Events", json.dumps(xparse) , hostname="18.188.23.129")

        startCounter = startCounter + 1
#         print('this is the jsonData %s \n' % jsonData)
        # if jsonData :
        #     print ('*** before flash ***')
        flash(jsonData)
        
        socketio.emit("message",{'repo': jsonData['repo'],'data':jsonData['data'],'start':'{0:%d/%m/%Y %H:%M:%S}'.format(datetime.now()), 'counter': startCounter , 'event':jsonData['event'] })

        #dbHandler.insertData(jsonData,startTime,startCounter)
        #dbHandler.retrieveData()

        return "xpost realised avec : %s \n %s \n %s" % (jsonData['data'],jsonData['event'],jsonData['repo']) 

    else:

        return render_template('index.html', data=jsonData,start=startTime,counter=startCounter)


#from websocket import (
#      handle_client_connect_event,
#)

@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))


@socketio.on('message')
def handle_message_event(letext):
    print('Message recu: {0}'.format(letext))
    
    
@app.route('/search')
def home():
    return render_template('search.html')

@app.route('/test')
def test():
    return render_template('test.html')

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
#         xjoin += "%s(%s) ,  " % (key,value) 
        xjoin = "%s  %s(%s)" % (xjoin,key,value) 
#     print ("%s\n%s\n%s" % ("="*60,xjoin,"="*60))
    return xjoin
    
@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    target = request.form["targettable"]
    res=""
    xjoin_ =''
    search_term = request.form["input"]
    if target == "Commits":
        res = es.search(
            index="engine-recherche",
            #size=0, 
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
    xjoin_ = countLanguages(res)
    return render_template('results.html', res=res, target=target, xjoin=xjoin_ , searchTerm=search_term)