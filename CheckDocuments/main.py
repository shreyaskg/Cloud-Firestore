# function to verify the document

import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("AccountServiceKey.json")
# Initializing the app
firebase_admin.initialize_app(cred)
db = firestore.client()

data = {'verified_by':'',
        'user_doc_id':'cGHgvv85qrbe16RDohXk',
        'doc_id':'',
        'approval':'',
        'verification_status':'verified'}

def Verify_Document(data):
    doc_ref = db.collection('Profile').document(data['user_doc_id']).collection('Documents').document(data['doc_id'])
    docs_ref =db.collection('Profile').document(data['user_doc_id'])
    get_doc_type = ''
    if data['verification_status'] == 'verified':
        doc_ref.set({'verification_status':'verified'})
        docs_ref.set(data,merge = True)
        get_doc_type = doc_ref.get().to_dict()['doc_type']
        if get_doc_type in ['photo','id_proof']:
            flag = 1

        if flag == 1:
            if get_doc_type == 'photo':
                docs_ref.set({'photo_verification_status':'verified'},merge = True)
            elif get_doc_type == 'id_proof':
                docs_ref.set({'id_proof_verification_status': 'verified'}, merge=True)