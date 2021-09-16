#!/usr/bin/env python
# encoding: utf-8
import json
import uuid
import pymongo
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)



@app.route('/')
def index():
    res = collection1.find({})
    all_user_data = []
    for user_data in res:
        all_user_data.append(user_data)
    return json.dumps(all_user_data)



@app.route('/loggedInUserList')
def getLoggedInUserList():
    res = collection2.find({})
    logged_in_users_list = []
    for user in res:
        logged_in_users_list.append(user)
    return json.dumps(logged_in_users_list, default=str)



@app.route('/user')
def getUserData():
    session_id = request.args.get('session_id')
    res = collection2.find_one({'_id': session_id})
    user_id = res["user_id"]
    user_data = collection1.find_one({'_id': user_id})
    return json.dumps(user_data["data"])



@app.route('/user/course')
def getCourseData():
    courseCode = request.args.get('courseCode')
    session_id = request.args.get('session_id')
    
    res = collection2.find_one({'_id': session_id})
    user_id = res["user_id"]

    user_data = collection1.find_one({'_id': user_id})

    response = {}
    for course in user_data["data"]:
        if course['courseCode'] == courseCode:
            response = course
            break
    return json.dumps(response)



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        #print(request.json['response']['googleId'])

        user_id = request.json['response']['googleId']

        res = collection1.find_one({'_id': user_id})
        if res == None:
            res = collection1.insert_one({'_id': user_id, 'data': []})

        session_id = uuid.uuid4()
        res = collection2.insert_one({'_id': str(session_id), 'user_id': user_id})

        #print(user_id, str(session_id))
        return json.dumps(str(session_id))



@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session_id = request.headers["Bunkalog-Session-Id"]
        res = collection2.delete_one({'_id': session_id})
    return 'logout request received'



@app.route('/add-class', methods=['POST'])
def addClass():
    if request.method == 'POST':
        print(request.json)
        request.json
        session_id = request.headers["Bunkalog-Session-Id"]

        res = collection2.find_one({'_id': session_id})
        user_id = res["user_id"]
        
        new_class_details = request.json
        
        # Perform validation
        new_class_details['classesAttended'] = int(new_class_details['classesAttended'])
        new_class_details['totalClasses'] = int(new_class_details['totalClasses'])

        res = collection1.find_one({'_id': user_id})
        res["data"].append(new_class_details)
        res = collection1.update_one({'_id': user_id}, {"$set": res})
        
        return 'success'



@app.route('/attend-class', methods=['POST'])
def attendClass():
    if request.method == 'POST':
        print(request.json)
        classVal = request.json['courseCode']
        session_id = request.headers["Bunkalog-Session-Id"]
        res = collection2.find_one({'_id': session_id})
        user_id = res["user_id"]

        res = collection1.find_one({'_id': user_id})

        for course in res["data"]:
            if course['courseCode'] == classVal:
                course['classesAttended'] = course['classesAttended'] + 1
                course['totalClasses'] = course['totalClasses'] + 1

        res = collection1.update_one({'_id': user_id}, {"$set": res})

        return 'success'



@app.route('/bunk-class', methods=['POST'])
def bunkClass():
    if request.method == 'POST':
        print(request.json)
        classVal = request.json['courseCode']
        session_id = request.headers["Bunkalog-Session-Id"]
        res = collection2.find_one({'_id': session_id})
        user_id = res["user_id"]

        res = collection1.find_one({'_id': user_id})

        for course in res["data"]:
            if course['courseCode'] == classVal:
                course['totalClasses'] = course['totalClasses'] + 1

        res = collection1.update_one({'_id': user_id}, {"$set": res})

        return 'success'



if __name__=='__main__':
    with open('.env') as f:
        password = f.readline()
        #print(password, len(password), bytes(password, 'utf-8'))
    client = pymongo.MongoClient("mongodb://csrp:" + password[:-1] + "@valhalla-shard-00-00.7f9jf.mongodb.net:27017,valhalla-shard-00-01.7f9jf.mongodb.net:27017,valhalla-shard-00-02.7f9jf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-13itpy-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.test

    global databases
    global collection1
    databases = client.bunkalog
    collection1 = databases.attendance_log
    collection2 = databases.session_log
    
    """#res = collection1.insert_one({'_id': '101', 'user_id': '100'})
    res = collection1.find({})
    for doc in res:
        print(doc)"""

    app.run(host="0.0.0.0")
