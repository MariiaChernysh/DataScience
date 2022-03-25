import requests
import pandas as pd
import json

#start at date-1, 22:00 for the whole day. -2 hours
start="2022-03-24T22:00:00.000Z"
end="2022-03-25T10:00:00.000Z"

#kibana url
#put size=N to download the needed N of data-rows
url = "http://kibana.**********/_search?size=1000"
querystring = {"pretty":""}
#query for the request (created from postman on the basis of curl request)
payload = "{\"query\": {\r\n    \"bool\": {\r\n      \"must\": [],\r\n      \"filter\": [\r\n        " \
          "{\r\n          \"bool\": {\r\n            \"should\": [\r\n              {\r\n                " \
          "\"range\": {\r\n                  \"execution_time\": {\r\n                    \"gt\": \"30000\"\r\n " \
          "                 }\r\n                }\r\n              }\r\n            ],\r\n            " \
          "\"minimum_should_match\": 1\r\n          }\r\n        },\r\n        {\r\n          \"range\": " \
          "{\r\n            \"created_at\": {\r\n              \"format\": \"strict_date_optional_time\",\r\n " \
          "             \"gte\": \""+str(start)+"\",\r\n             " \
          " \"lte\": \""+str(end)+"\"\r\n            }\r\n          }\r\n        }\r\n     " \
          " ],\r\n      \"should\": [],\r\n      \"must_not\": []\r\n    }\r\n  }}"

#put auhorization and token here
headers = {
    'authorization': "*********************",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "*************************"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
data=response.text

#json is loaded with extra text in the beginning and end. delete it for further transformations
obj = json.loads(data)
hits=obj['hits']
hits=hits['hits']
hits=json.dumps(hits)

file=open("data.txt", "w", encoding="utf-8")
file.truncate(0)
file.write(hits)
file.close()
#######################################
#read data as json and transform as needed
df = pd.read_json('data.txt')
df=pd.json_normalize(df['_source'], max_level=0).sort_values('execution_time', ascending=False)
ttt=df.drop_duplicates(subset='click_id', keep='first')
#ttt=df.groupby('click_id').apply(lambda x: x.loc[x.execution_time.idxmax()])
final=ttt[[ 'p1', 'created_at', 'execution_time', 'click_id']].reset_index()
final.to_csv('fresh_click_ids.csv')