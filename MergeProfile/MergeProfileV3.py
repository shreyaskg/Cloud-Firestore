
# Merging Profiles based on origin timestamp
import firebase_admin
import collections
import flask
# To avoid "importing from collections instead of collections.abc" warning
try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections
from firebase_admin import credentials
from flask import jsonify
from firebase_admin import firestore, auth

# cred = credentials.Certificate(r"C:\Users\shrey\PycharmProjects\Cloud_function_26\2\UpdateExistingTalent\AccountServiceKey.json")

# firebase_admin.initialize_app(cred)
# db = firestore.client()

def MergeDictionaries(d1,d2):
    d2.update(d1)
    return d2

# This function deleted all the documents within sub_collection and also finally deletes the document
def DeleteProfile(user_doc_id):
    
    # Get the document reference
    ref1 = db.collection('Profile').document(user_doc_id).get()
    
    sub_collection_1 = []
    sub_collection_1_data = {}
    
    # Get all the sub_collection names in the first for loop
    for sub_collection in ref1.reference.collections():
        sub_collection_1.append(sub_collection.id)
        
        # Get all the documents in the sub_collection
        data = db.collection('Profile').document(user_doc_id).collection(sub_collection.id).stream()
        
        # For each document in the sub_collection append the id of that particular document
        for d in data:
            # Use a hash map/ Dictionary to store in  sub_collection: [document1,document2] format
            if sub_collection.id not in sub_collection_1_data:
                sub_collection_1_data[sub_collection.id] = []
            sub_collection_1_data[sub_collection.id].append(d.id)

    # For each sub-collection 
    for sub_collection in sub_collection_1_data.keys():
        
        # For each document in sub_collection
        for id in sub_collection_1_data[sub_collection]:
            
            # Delete the document in that sub_collection
            db.collection('Profile').document(user_doc_id).collection(sub_collection).document(id).delete()
            
    # After all the sub_collections and associated documents are deleted, we can delete the document 
    db.collection('Profile').document(user_doc_id).delete()
    print("Profile Deleted")

# This function merges the fields in user_doc_id2 to user_doc_id1
def MergeProfile(user_doc_id1,user_doc_id2):
    print('Merge Called')
    ref1 = db.collection('Profile').document(user_doc_id1).get()
    ref2 = db.collection('Profile').document(user_doc_id2).get()

    data2 = ref2.to_dict()
    data1 = ref1.to_dict()

    temp_data1=data1
    temp_data2=data2

    

    # This is done to avoid any None errors
    if not data1 or not data2:
        print("Data doesn't exist")
        return 

    for data_1 in list(data1.keys()):
        
        if data1[data_1] in ['',0,'0','NA',None] or isinstance(data1[data_1],collections.Mapping) or isinstance(data1[data_1],list):
            
            # If the field exists within data 2 as well, we need to update the values
            if data_1 in list(data2.keys()):
                
                # If the field is a dictionary, then we will have to merge the values individually
                if isinstance(data1[data_1],collections.Mapping):
                   
                    for key in list(data1[data_1].keys()):
                        
                        # If the key exists within the data and the value in data2 is not null, then we have to replace the value
                        if key in list(data2[data_1].keys()):
                            if data1[data_1][key] in ['',0,'0','NA',None]:
                                # Replacing only the values that need to be replaced 
                                data1[data_1][key] = data2[data_1][key]        
                    data1[data_1] = MergeDictionaries(data1[data_1],data2[data_1])
 
                # If the field is not a dictionary we can replace the value directly
                elif isinstance(data1[data_1],list):
                    data1[data_1] += data2[data_1]
                    data1[data_1] = set(data1[data_1])
                    data1[data_1] = list(data_1)
                else:
                    data1[data_1] = data2[data_1]
                    del data2[data_1]
    
    for data_2 in list(data2.keys()):
        if data_2 not in list(data1.keys()):
            data1[data_2] = data2[data_2]        
                    
            # If the data exists and is not a garbage value we replace the value in the second document with the first
    db.collection('Profile').document(user_doc_id1).set(data1,merge = True)

    # Also we must update the sub-collections if it doesn't exist in the first document, replace it it exists
    sub_collection_1 = []
    sub_collection_1_data = {}
    sub_collection_2 = []

    # Getting all sub-collection names from user_doc_id1
    for sub_collection in ref1.reference.collections():
        
        # sub_collection_1 contains the names of all the sub_collections inside the document
        sub_collection_1.append(sub_collection.id)
        
        # Get all the documents in the particular sub_collection
        data = db.collection('Profile').document(user_doc_id1).collection(sub_collection.id).stream()
        
        # For each document in the sub_collection, convert it into dictionary
        for d in data:
            dt = d.to_dict()
            
            # Then use a hash table / dictionary to store the documents under their respective sub-collection ids
            if sub_collection.id not in sub_collection_1_data:
                sub_collection_1_data[sub_collection.id] = []
            sub_collection_1_data[sub_collection.id].append(dt)
    
    # Getting all sub-collection names from user_doc_id2
    for sub_collection in ref2.reference.collections():
        sub_collection_2.append(sub_collection.id)

    # Getting all the document under the sub-collections
    for sub_coll in sub_collection_2:
        if sub_coll not in ("App",'settings'):
            collection_data = db.collection('Profile').document(user_doc_id2).collection(sub_coll).stream()

            # If the sub collection doesn't exist within the user_doc_id1's sub_collections
            if sub_coll not in sub_collection_1:
                # Then we create the sub_collection and add the sub-collection data from user_doc_id2
                for doc in collection_data:
                    data = doc.to_dict()
                    if "user_doc_id" in data:
                        data['user_doc_id']=user_doc_id1
                    if "doc_id" in data:
                        data['doc_id']=user_doc_id1
                    db.collection('Profile').document(user_doc_id1).collection(sub_coll).document().set(data)

            # If the sub_collection name already exists,
            else:
                # Just copy the documents to the existing sub-collection
                for doc in collection_data:
                    
                    data = doc.to_dict()
                    if "user_doc_id" in data:
                        data['user_doc_id']=user_doc_id1
                    if "doc_id" in data:
                        data['doc_id']=user_doc_id1
                        
                    # Check if such a document already exists with the same fields, if it is not then we set the document of the document in sub-collection of user_doc_id1 to user_doc_id2
                    if data not in sub_collection_1_data[sub_coll]:
                        db.collection('Profile').document(user_doc_id1).collection(sub_coll).document().set(data,merge = True)


    if "author" in temp_data1:
        email=temp_data1['email']
        author=temp_data1['author']
        db.collection('Profile').document(ref1.id).set({'email':email,'author':author},merge=True)
    elif "author" in temp_data2:
        email=temp_data2['email']
        author=temp_data2['author']
        db.collection('Profile').document(ref1.id).set({'email':email,'author':author},merge=True)
    
    auth.set_custom_user_claims(author,{'user_doc_id':ref1.id})

    # Since we always merge data of user_doc_id2 to user_doc_id1, we will always delete the user_doc_id2 document 
    DeleteProfile(ref2.id)



# The MergeProfile function always merges user_doc_id2 to user_doc_id1, this function controls that as per timestamps
def hello_world(request):
    
    recdata = flask.request.json
    user_doc_id1 = recdata['doc_id_1']
    user_doc_id2 = recdata['doc_id_2']
    
    ref1 = db.collection('Profile').document(user_doc_id1).get()
    ref2 = db.collection('Profile').document(user_doc_id2).get()

    data2 = ref2.to_dict()
    data1 = ref1.to_dict()

    ret_data={}
    
    if not data1 or not data2:
        print("Data doesn't exist")
        return jsonify({'status': False,'message':'Data does not exist'})
    # If origin exits compare, and if we need we can swap user_doc_id1 and user_doc_id2
    time_stamp = 'time_stamps'
    
    # As per the timestamps, user_doc_ids are swapped or kept as it is and MergeProfile function is called
    if time_stamp in data2 and time_stamp not in data1:
        MergeProfile(user_doc_id2,user_doc_id1)
        ret_data={'status': True,'message':'Profiles merged'}

    elif time_stamp in data2 and time_stamp in data1:
        # Check for origin in both timestamps
        if 'origin' in data2[time_stamp] and 'origin' not in data1[time_stamp]:
            MergeProfile(user_doc_id2,user_doc_id1)
            ret_data = {'status': True,'message':'Profiles merged'}
            
        elif 'origin' in data2[time_stamp] and 'origin' in data1[time_stamp]:
            origin2 = data2[time_stamp]['origin']
            origin1 = data1[time_stamp]['origin']
            if origin2 < origin1:
                MergeProfile(user_doc_id2,user_doc_id1)
                ret_data = {'status': True,'message':'Profiles merged'}
            else:
 
                MergeProfile(user_doc_id1,user_doc_id2)
                ret_data={'status': True,'message':'Profiles merged'}
        else:
            # Default case merge to user_doc_id1
            MergeProfile(user_doc_id1,user_doc_id2)
            ret_data={'status': True,'message':'Profiles merged'}
    else:
        MergeProfile(user_doc_id1,user_doc_id2)
        ret_data ={'status': True,'message':'Profiles merged'}
    return jsonify(ret_data)

