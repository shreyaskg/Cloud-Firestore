import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate('AccountServiceKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def UpdateTalent(user_doc_id):
    # Step 0, Create a reference to the document and get the document fields
    doc_ref = db.collection('Profile').document(user_doc_id)
    doc = doc_ref.to_dict()

    # Step 1, check if "talent" field exists within the document fields, to avoid any key error
    if "Talent" in doc:
        doc = doc['Talent']
        # Step 2 : Check the flags which are true if flag exists within the document
        if "Flag" in doc:  # type(Flag) =  Dictionary
            flags = doc["Flag"]
            for flag in flags:
                # Only proceed if flag is true
                if flag:  # flag = true/false
                    # If flag is true, then check if the "key" value [cooking,dance_talent.....] exsists within the document



UpdateTalent('000Test')