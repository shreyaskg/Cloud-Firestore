# function to create a Document sub-collection if it doesn't exist and set the 'docs' field of the document

import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("AccountServiceKey.json")
# Initializing the app
firebase_admin.initialize_app(cred)
db = firestore.client()

def doc_type_set(data,l_data):

	# getting the user_doc_id
	doc_ref = data['user_doc_id']

	# setting the timestamp
	ts = int(time.time())
	data['timestamp'] = ts

	# Set the default value of approver to folk_guide, from the profile section
	if data['approver'] == '':
		print('fuck')
		doc_folk_guide = db.collection('Profile').document(doc_ref).get().to_dict()['folk_guide']
		data['approver'] = doc_folk_guide

	#getting the doctype
	doc_type = data['doc_type']

	# Set default verification_status to pending
	if data['verification_status'] != '':
		data['verification_status'] = 'pending'

	doc = 0
	doc_ = db.collection('Profile').document(doc_ref).collection('Documents').stream()
	for i in doc_:
		doc += 1

	docs_ref = db.collection('Profile').document(doc_ref)
	if True:
		# create a reference to the docs section
		if (doc == 1):
			# First document so set the left side docs to the required format
			docs_ref.set({'docs': l_data}, merge=True)
		else:
			# get the verification status of the docs document
			ref_doc = docs_ref.get().to_dict()
			verify_status=''
			if 'docs' in ref_doc:
				if status in ref_doc['docs']:
					verify_status = ref_doc['docs'][status]
					verify_status = verify_status.lower()


			flag = 0
			if verify_status=='':
				flag=1
			if verify_status == 'pending' and data['verification_status'] == 'pending':
				flag = 1
			elif verify_status == 'pending' and data['verification_status'] == 'verified':
				flag = 1
			elif verify_status == 'verified' and data['verification_status'] == 'verified':
				flag = 1
			elif verify_status not in ['pending', 'verified']:
				flag = 1
			if flag == 1:

				if doc_type=='photo':
					docs_ref.set({'docs': {'photo_url': l_data['photo_url'],'last_timestamp':int(time.time()),
										   'photo_url_last_submission': l_data['photo_url_last_submission'],
										   'photo_verification_status': l_data['photo_verification_status']}},
								 merge=True)
				elif doc_type == 'id_proof':
					docs_ref.set({'docs': {'id_proof_url': l_data['id_proof_url'],'last_timestamp':int(time.time()),
										   'id_proof_last_submission': l_data[
											   'id_proof_last_submission'],
										   'id_proof_verification_status': l_data[
											   'id_proof_verification_status']}}, merge=True)



data = {'uploaded_by':'008jYwyjRDJDqLZwDcrJ',
        'doc_type':'certificate',
        'doc_link' : 'https://firebases//',
        'reference_file_name' :'Ahmedabad.jpg',
        'file_type':'jpg',
        'user_doc_id':'cGHgvv85qrbe16RDohXk',
        'verification_status':'verified',
        'doc_details':'Ration Card',
        'approver':'',
        'remarks':'verified'
        }
l_data = {
		# approver is common to all document types
		'approver': data['approver'],
		'documents_verification_status': '',
		'id_proof_last_submission': 0,
		'id_proof_url': '',
		'id_proof_verification_status': '',
		'last_submission': 0,
		'photo_url': '',
		'photo_url_last_submission': 0,
		'photo_verification_status': ''
	}

doc_type_set(data,l_data)