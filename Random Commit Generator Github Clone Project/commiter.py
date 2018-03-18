import requests
import time
import json
import requests
import pandas as pd
headers = {'Content-Type':'Application/json'}
root = 'http://88.169.46.187:9200'
database = root + '/github'

def sendPost(jsonData)  :
#     global target
#     xdate = date.today()
#     xdate = date.today().strftime("%Y-%m-%d %H:%M:%S.%f")
#     xdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")     
    print(jsonData)
    response = requests.request("POST",'http://34.215.22.13:5000/xpost', json=jsonData)
    print(response.content)

def searchMatch():
    xreq=requests.get(database + '/_search?',headers=headers, data=json.dumps(
    {
      "query": {
        "function_score": {
          "query": {
            "match_all": {}
          },
          "functions": [
            {
              "random_score": {}
            }
          ]
        }
      }

        ,"size":1000    ,"_source":["type","created_at","id","repo.id","repo.name","actor.id","payload.comment.commit_id","payload.commits.message" ]    
    })).json() 
    return xreq
xres=searchMatch()        
xcount = len(xres['hits']['hits'])
        
while xcount>0 :
    xdix = pd.io.json.json_normalize(xres['hits']['hits'])
    xdix=xdix.fillna('')
    xdix['_source.payload.commits']=xdix['_source.payload.commits'].apply(lambda x : ','.join([v['message'] for v in x]))
    
#     for xid in xdix.rows:
    for index, xid in xdix.iterrows():
        xindex = xid._id
        print (' *** Processing id=%s *** ' % xindex)
        try:
	        sendPost(  {'repo':xid['_source.repo.name'],'data':'ID : %s => MSG : %s ' % (xid._id,xid['_source.payload.commits'] if xid['_source.payload.commits']!='' else 'VIDE') , 'event': xid['_source.type']})
        except:
                print('**** post impossible, verifier serveur')
                pass
        finally:
                print('*** sendpost done')
        
        time.sleep(3.0)
        
    xres=searchMatch()
    xcount = len(xres['hits']['hits'])
    print ( '-- count de restant : %s --' % xcount)

def xtimer():
    global t
    print(sendPost())
    t = threading.Timer(3.0, xtimer)
    t.start()


