#!/usr/bin/env python
# encoding: utf-8
import json
import uuid
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

data = {}
loggedInUserList = {}


def redirectScript():
    return '<script>window.location.replace("http://localhost:3000/")</script>'




@app.route('/')
def index():
    print(data, loggedInUserList)
    print('DEBUG:', request.cookies)
    if 'bunkalog_session_id' in request.cookies:
        print(request.cookies.get('bunkalog_session_id'))
    return json.dumps(data) 



@app.route('/loggedInUserList')
def getLoggedInUserList():
    print(loggedInUserList)
    return json.dumps(loggedInUserList, default=str)



@app.route('/user')
def getUserData():
    session_id = request.args.get('session_id')
    user_id = loggedInUserList[session_id][0]
    return json.dumps(data[user_id])



@app.route('/user/course')
def getCourseData():
    courseCode = request.args.get('courseCode')
    session_id = request.args.get('session_id')
    user_id = loggedInUserList[session_id][0]
    response = {}
    for i in data[user_id]:
        if i['courseCode'] == courseCode:
            response = i
            break
    return json.dumps(response)



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        #print(request.json['response']['googleId'])

        user_id = request.json['response']['googleId']
        if user_id not in data:
            data[user_id] = []

        session_id = uuid.uuid4()
        loggedInUserList[str(session_id)] = [user_id, datetime.now()]

        print(user_id, str(session_id))

        return json.dumps(str(session_id))



@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session_id = request.headers["Bunkalog-Session-Id"]
        del loggedInUserList[session_id]
    return 'logout request received'



@app.route('/add-class', methods=['POST'])
def addClass():
    if request.method == 'POST':
        print(request.json)
        request.json
        session_id = request.headers["Bunkalog-Session-Id"]
        user_id = loggedInUserList[session_id][0]
        new_class_details = request.json
        # Perform validation
        new_class_details['classesAttended'] = int(new_class_details['classesAttended'])
        new_class_details['totalClasses'] = int(new_class_details['totalClasses'])
        data[user_id].append(new_class_details)
        return redirectScript()



@app.route('/attend-class', methods=['POST'])
def attendClass():
    if request.method == 'POST':
        print(request.json)
        classVal = request.json['courseCode']
        session_id = request.headers["Bunkalog-Session-Id"]
        user_id = loggedInUserList[session_id][0]
        for i in data[user_id]:
            if(i['courseCode']==classVal):
                i['classesAttended']=i['classesAttended']+1
                i['totalClasses']=i['totalClasses']+1
        return redirectScript()



@app.route('/bunk-class', methods=['POST'])
def bunkClass():
    if request.method == 'POST':
        print(request.json)
        classVal = request.json['courseCode']
        session_id = request.headers["Bunkalog-Session-Id"]
        user_id = loggedInUserList[session_id][0]
        for i in data[user_id]:
            if(i['courseCode']==classVal):
                i['totalClasses']=i['totalClasses']+1
        return redirectScript()



if __name__=='__main__':
        app.run(host="127.0.0.1")
