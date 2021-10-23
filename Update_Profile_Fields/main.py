# Update Fields in profile
import requests
import firebase_admin
import flask
from firebase_admin import credentials , firestore ,auth
from flask import jsonify

# cred = credentials.Certificate(r"C:\Users\shrey\PycharmProjects\Cloud_function_26\2\UpdateExistingTalent\AccountServiceKey.json")

# firebase_admin.initialize_app(cred)
# db = firestore.client()

def hello_world(request):
#     recdata = request.flask.json
    data = {}
    recdata = request
    status = {"status":False}
    if 'city' in recdata:
        data['city'] = recdata['city']
    if 'state' in recdata:
        data['state'] = recdata['state']
    if 'nationality' in recdata:
        data['nationality'] = recdata['nationality']
    if 'user_doc_id' in recdata:
        user_doc_id = recdata['user_doc_id']
        db.collection('Profile').document(user_doc_id).set(data,merge = True)
        status["status"] = True
#     return (jsonify(status))
hello_world({'user_doc_id':'00abc','city':'Bru','state':'Karnataka','nationality':'Indian'})
    
