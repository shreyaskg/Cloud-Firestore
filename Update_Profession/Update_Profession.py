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
    if 'occupation_details' in data:
        data = data['occupation_details']
        format_1 = {
            'designation':'designation',
            'working_with':'company_name'
        }
        format_2 = {
            'business_nature':'company_nature',
            'business_rols':'designation'
        }
        format_1_data = {
            "company_location": "",
            "company_name": "",
            "designation": "",
            "company_nature": "",
            "start_date": "",
            "end_date": "",
            "status": "",
            "current_major_occupation": True,

            "doc_id": "",

            "user_doc_id": user_doc_id
        }
        f1_flag = 0
        f2_flag = 0
        format_2_data = format_1_data
        keys = format_1.keys()
        for key in keys:
            if key in data:
                if data[key]:
                    format_1_data[format_1[key]] = data[key]
                    f1_flag = 1
        keys = format_2.keys()
        for key in keys:
            if key in data:
                if data[key]:
                    format_2_data[format_2[key]] = data[key]
                    f2_flag = 1
        if f1_flag:
            get = requests.post('https://us-central1-folk-bf69e.cloudfunctions.net/UpdateProfession',
                                json = format_1_data)
        if f2_flag:
            get = requests.post('https://us-central1-folk-bf69e.cloudfunctions.net/UpdateProfession',
                                json=format_2_data)
        return jsonify(({'status':'ok'}))

