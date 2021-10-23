import requests
import firebase_admin
import json
import urllib
import flask
from flask import jsonify
from firebase_admin import credentials
from firebase_admin import firestore

firebase_admin.initialize_app()
db = firestore.client()

def hello_world(request):
    user_doc_id = requests.args.get('user_doc_id')
    data = db.collection('Profile').document(user_doc_id).get().to_dict()
    if 'education' in data:
        data = data['education']
        dictionary = {
            'branch': 'branch',
            'college': 'college_name',
            'highest_qualification':'degree',
            'graduated_from': 'college_name',
            'stream':'degree_type',
            'course_year':'year_of_completion'
        }
        new_data = {
                "degree_type": "",
                "college_name": "",
                "highest_qualification": True,
                "location": "",
                "score": 0,
                "university": "",
                "degree": "",
                "category": "",
                "year_of_completion": 0,
                "doc_id": "",
                "branch": "",
                "user_doc_id": user_doc_id
        }
        keys = dictionary.keys()
        for i in keys:
            if i in data:
                if data[i]:
                    new_data[dictionary[i]] = data[i]

        get = requests.post('https://us-central1-folk-bf69e.cloudfunctions.net/UpdateEducation',json = new_data)
        return jsonify(({'status': 'ok'}))


'''
{
        1"degree_type":"Graduation", Yes
        2"college_name":"DaulatRam College", Yes
        3"highest_qualification":True,  Yes
        4"location":"Delhi",  Yes
        5"score":90,  Yes
        6"university":"DU",  Yes
        7"degree":"",  Yes
        8"category":"",  Yes
        10"year_of_completion":2016,   Yes
        11"doc_id":"bAcjzMh8BxsnLQ1FHT7j",   Yes
        12"branch":"Statistics",   Yes
        13"user_doc_id":"000Test"   Yes
        14"course_year":1   Yes

}
'''