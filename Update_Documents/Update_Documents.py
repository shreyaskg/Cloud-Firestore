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
    # Getting docs section of the document if it exists
    info = db.collection('Profile').document(user_doc_id).get().to_dict()
    if 'docs' in info:
        docs = info['docs']

        photo_proof_dict = {
            'approver':'approver',
            'photo_url':'doc_link',
            'photo_verification_status':'verification_status',
        }
        id_proof_dict =  {
            'approver': 'approver',
            'id_proof_url': 'doc_link',
            'id_proof_verification_status': 'verification_status',
        }

        photo_proof_data = {"uploaded_by":"",
            "doc_type":"",
            "doc_link" : "",
            "reference_file_name" :"",
            "file_type":"",
            "user_doc_id":user_doc_id,
            "verification_status":"",
            "doc_details":"",
            "approver":"",
            "remarks":""
            }
        id_proof_data = photo_proof_data

        id_flag = 0
        photo_flag = 0

        keys = photo_proof_dict.keys()
        for key in keys:
            if key in docs:
                if docs[key]:
                    photo_proof_data[photo_proof_dict[key]] = docs[key]
                    photo_flag = 1
        keys = id_proof_dict.keys()
        for key in keys:
            if key in docs:
                if docs[key]:
                    id_proof_data[id_proof_dict[key]] = docs[key]
                    id_flag = 1
        if photo_flag:
            photo_proof_data['doc_type'] = 'photo'
            get = requests.post('https://us-central1-folk-bf69e.cloudfunctions.net/UpdateDocuments', json=photo_proof_data)

        if id_flag:
            id_proof_data['doc_type'] = 'id_proof'
            get = requests.post('https://us-central1-folk-bf69e.cloudfunctions.net/UpdateDocuments', json=id_proof_data)

        return jsonify(({'status': 'ok'}))
