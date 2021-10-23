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
    # data in new format
    user_doc_id = requests.args.get('user_doc_id')
    data = db.collection('Profile').document(user_doc_id).get().to_dict()
    if 'tertiary_data' in data:
        tertiary_data = data['tertiary_data']

        father_dictionary = {
            'fathers_name': 'Name',
            'fathers_title':'title',
            'fathers_age_group':'age_group'
        }
        mother_dictionary = {
            'mothers_name':'Name',
            'mothers_title':'title',
            'mothers_age_group':'age_group'
        }
        father_data = {
            'relation_type': '',
            'comments': '',
            'current_nominee': True,
            'emergency_contact': True,
            'connect_to_org': True,
            'contact': '',
            'email': '',
            'age_group': '',
            'title': '',
            'location': '',
            'doc_id': '',
            'Name': '',
            'user_doc_id': user_doc_id
        }
        mother_data = father_data

        # setting
        flag_f = 0
        keys = father_dictionary.keys()
        for key in keys:
            if key in tertiary_data:
                if tertiary_data[key]:
                    father_data[father_dictionary[key]] = tertiary_data[key]
                    flag_f = 1

        flag_m = 0
        keys = mother_dictionary.keys()
        for key in keys:
            if key in tertiary_data:
                if tertiary_data[key]:
                    mother_data[mother_dictionary[key]] = tertiary_data[key]
                    flag_m = 1

        if flag_f == 1:
            # set father_data
            father_data['relation_type'] = 'Father'
            get = requests.post("https://us-central1-folk-bf69e.cloudfunctions.net/UpdateRelation", json=father_data)
        if flag_m == 1:
            # set mother_data
            mother_data['relation_type'] = 'Mother'
            get = requests.post("https://us-central1-folk-bf69e.cloudfunctions.net/UpdateRelation", json=mother_data)
        return jsonify(({'status': 'ok'}))