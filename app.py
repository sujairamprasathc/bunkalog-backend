#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request

app = Flask(__name__)

data = [
                {'courseName': 'Game Theory',
                'courseCode': '15XT81',
                'classesAttended': 21,
                'totalClasses': 24},
                {'courseName': 'Parallel & Distributed Computing',
                'courseCode': '15XT82',
                'classesAttended': 13,
                'totalClasses': 14},
                {'courseName': 'Mathematical Modelling',
                'courseCode': '15XT83',
                'classesAttended': 20,
                'totalClasses': 28},
                {'courseName': 'ADBMS',
                'courseCode': '15XTE1',
                'classesAttended': 14,
                'totalClasses': 18},
                {'courseName': 'DV',
                'courseCode': '15XTOK',
                'classesAttended': 22,
                'totalClasses': 22}
        ]

@app.route('/')
def index():
    return json.dumps(data) 

@app.route('/add-class', methods=['GET'])
def addClass():
        name = request.args.get('courseName')
        idval = request.args.get('courseCode')
        attend = int(request.args.get('classesAttended'))
        total = int(request.args.get('totalClasses'))
        newdict = {'courseName' : name,
                                'courseCode' : idval,
                                'classesAttended' : attend,
                                'totalClasses' : total}
        data.append(newdict) 
        return '<script>window.location.replace("http://192.168.86.129:3000/")</script>'

@app.route('/attend-class', methods=['GET'])
def attendClass():
        classVal = request.args.get('courseCode')
        for i in data:
                if(i['courseCode']==classVal):
                        i['classesAttended']=i['classesAttended']+1
                        i['totalClasses']=i['totalClasses']+1
        return '<script>window.location.replace("http://192.168.86.129:3000/")</script>'

@app.route('/bunk-class', methods=['GET'])
def bunkClass():
        classVal = request.args.get('courseCode')
        for i in data:
                if(i['courseCode']==classVal):
                        i['totalClasses']=i['totalClasses']+1
        return '<script>window.location.replace("http://192.168.86.129:3000/")</script>'

if __name__=='__main__':
        app.run(host="192.168.86.129")
