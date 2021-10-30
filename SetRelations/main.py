import firebase_admin
import time
import requests
import urllib
import json
import pygeohash as pgh
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("AccountServiceKey.json")
# Initializing the app
firebase_admin.initialize_app(cred)
db = firestore.client()

def relation_set(input_data):

   doc_ref = input_data['user_docid']

   base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
   AUTH_KEY = ""

   # If current nominee is true then all other fields must be false

   parameters = {

      "address": input_data['location']  + ' ' + input_data['city'] + ' ' + input_data['state'] + ' ' +
                 input_data['country'] ,
      "key": AUTH_KEY}

   r = json.loads(requests.get(f"{base_url}{urllib.parse.urlencode(parameters)}").text)

   lat = r['results'][0]['geometry']['location']['lat']
   lng = r['results'][0]['geometry']['location']['lng']
   input_data['geopoint'] = firestore.GeoPoint(lat, lng)
   input_data['formatted_location'] = r['results'][0]['formatted_address']
   input_data['geohash'] = pgh.encode(lat, lng)

   doc_ = db.collection('Profile').document(doc_ref).collection('Relations').stream()
   # doc_id : relation
   doc_references_relations = {}
   doc_nominee = {}

   # counting the number of documents in the sub-collection '
   doc = 0
   relation = input_data['relation_type']
   for i in doc_:
      id = i.id
      doc += 1
      i = i.to_dict()
      doc_references_relations[i['relation_type']] = id
      doc_nominee[i['current_nominee']] = id
   print(doc_references_relations)
   print(doc_nominee)
   if input_data['current_nominee'] == True:
      if True in doc_nominee:
         print('AYe')
         db.collection('Profile').document(doc_ref).collection('Relations').document(doc_nominee[i['current_nominee']]).set({'current_nominee':False},merge = True)

   # if it is the first document then create new document
   flag = 0
   if doc == 0:
      db.collection('Profile').document(doc_ref).collection('Relations').document().set(input_data)
      flag = 1
      print('1')

   else:
      # If the present relation already exists then replace the document with the current one
      if relation in doc_references_relations and relation in ['Father','Mother']:
         replace_doc_ref = doc_references_relations[relation]
         db.collection('Profile').document(doc_ref).collection('Relations').document(replace_doc_ref).set(input_data,merge = True)
         if (relation == 'Father'):
            flag = 1
            print('2')
         elif (relation == 'Mother'):
            flag = 1
            print('3')

      elif input_data['relation_type'] not in doc_references_relations:
           db.collection('Profile').document(doc_ref).collection('Relations').document().set(input_data)
           print('4')
   if flag == 1:
      if relation == 'Father':
         db.collection('Profile').document(doc_ref).set({'tertiary_data': {'fathers_age_group': input_data['age_group'],
                                                                              'fathers_name': input_data['Name'],


                                                                              'fathers_title': input_data['title']}},
                                                           merge=True)
      elif relation == 'Mother':
         db.collection('Profile').document(doc_ref).set({'tertiary_data': {'mothers_age_group': input_data['age_group'],
                                                                              'mothers_name': input_data['Name'],
                                                                              'mothers_title': input_data['title']}},
                                                           merge=True)


input_data = {
   'relation_type':'Father',
   'timestamp':1599195847,
   'comments':'rejected because of data',
   'current_nominee':True,
   'emergency_contact':True,
   'connect_to_org':True,
   'contact':9886665344,
   'email':'asd@gmail.com',
   'age_group'	:'34-50',
   'title':'late',
   'location':	'MG Road',
   'birth_year':	1973,
   'state':'Karnataka',
   'city':	'Bangalore',
   'country':'India',
   'Name':	'Yamete',
   'user_docid': 'XzCMuNysyOjImr9ctKqX'
}
relation_set(input_data)
