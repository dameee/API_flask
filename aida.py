from flask import Flask, jsonify, request
import urllib.request
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import random
from parser import search

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

serviceUsername = "2abcc976-5f46-4e6b-9500-115955bec194-bluemix"
servicePassword = "3aa0704505b49cc78210b107a20202af14d94c98aed2ac4ece4b47789f311d44"
serviceURL = "https://2abcc976-5f46-4e6b-9500-115955bec194-bluemix:3aa0704505b49cc78210b107a20202af14d94c98aed2ac4ece4b47789f311d44@2abcc976-5f46-4e6b-9500-115955bec194-bluemix.cloudantnosqldb.appdomain.cloud"
databaseName = "aida"

@app.route('/')
def hello_world():
    output="hello"
    return jsonify(output)

@app.route('/makeroom', methods=['GET', 'POST'])
def makeroom():
    # 接続
    client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
    client.connect()
    myDatabase = client[databaseName]

    # 書き込み
    flag = True
    room_id = 0
    while flag:
        flag = False
        tmp = random.randrange(9999)
        print(tmp)
        for item in Result(myDatabase.all_docs, include_docs=True):
            if item["doc"]["room_id"]==tmp:
                flag = True
        if(flag==False):
            room_id = int('{0:04d}'.format(tmp))

    jsonDocument = {
        "room_id": room_id,
        "host_name": request.args.get('host_name'),
        "guest_name": None,
        "host_station": request.args.get('host_station'),
        "guest_station": None
    }
    newDocument = myDatabase.create_document(jsonDocument)
    if newDocument.exists():
        print("ルーム '{0}' が作成されました．".format(newDocument["room_id"]))

    output={
        "room_id": newDocument["room_id"]
    }

    return jsonify(output)

@app.route('/enter_room', methods=['GET', 'POST'])
def enter_room():
    # 接続
    client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
    client.connect()
    myDatabase = client[databaseName]

    #書き換え
    search_id = int(request.args.get('room_id'))
    guest_name = request.args.get('guest_name')
    guest_station = request.args.get('guest_station')
    result_collection = Result(myDatabase.all_docs, include_docs=True)
    for item in result_collection:
        if item["doc"]["room_id"]==search_id:
            target = myDatabase[item["doc"]["_id"]]
            target['guest_name'] = guest_name
            target['guest_station'] = guest_station
            target.save()

    output={
      "success":True
    }

    return jsonify(output)

@app.route('/room_info', methods=['GET', 'POST'])
def room_info():
    # 接続
    client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
    client.connect()
    myDatabase = client[databaseName]

    # 読み込み
    search_id = int(request.args.get('room_id'))
    result_collection = Result(myDatabase.all_docs, include_docs=True)
    output = {}
    for item in result_collection:
        if item["doc"]["room_id"]==search_id:
            output ={
                "users": [
                    {
                        "name": item["doc"]["host_name"],
                        "station": item["doc"]["host_station"]
                    },
                    {
                        "name": item["doc"]["guest_name"],
                        "station": item["doc"]["guest_station"]
                    }
                ]
            }
    return jsonify(output)

@app.route('/choose_station', methods=['GET', 'POST'])
def choose_station():
    my_station = request.args.get('from_station')
    friend_station = request.args.get('to_station')
    result = search(my_station, friend_station)
    data=result.stations
    off = len(data) // 2
    name=data[off]
    my_station_route=data[:off+1]
    friend_station_route=list(reversed(data[off:]))

    output={
        "station_match": {"name": name},
        "from_station_route": my_station_route,
        "to_station_route": friend_station_route
    }
    return jsonify(output)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
