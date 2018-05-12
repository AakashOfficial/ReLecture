# -*- coding: utf-8 -*-
import requests
import json
import codecs
import sys, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Add IBM Cloud credentials here
username = "2dc8e7bd-8219-42cc-9913-cea7af948071"
password = "TVNKFLoJjeOv"
headers = {'Content-Type' : "application/json"}

# Step 1: Create a custom model
# Change "name" and "description" to suit your own model
def create_custom_model(name, base_model_name, description):
	print("\nCreating custom mmodel...")
	data = {"name" : name, "base_model_name" : base_model_name, "description" : description}
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations"
	jsonObject = json.dumps(data).encode('utf-8')
	resp = requests.post(uri, auth=(username,password), verify=False, headers=headers, data=jsonObject)

	print("Model creation returns: ", resp.status_code)
	if resp.status_code != 201:
	   print("Failed to create model")
	   print(resp.text)
	   sys.exit(-1)

	respJson = resp.json()
	customID = respJson['customization_id']
	print("Model customization_id: ", customID)

	return customID

# Step 2: Add a corpus file (plain text file - ideally one sentence per line,
# but not necessary). In this example, we name it 'corpus1' - you can name
# it whatever you want (no spaces) - if adding more than one corpus, add
# them with different names
def add_corpus_file(customID, corpus_file, corpus_name):
	print("\nAdding corpus file...")
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/"+customID+"/corpora/"+corpus_name
	with open(corpus_file, 'rb') as f:
	   r = requests.post(uri, auth=(username,password), verify=False, headers=headers, data=f)

	print("Adding corpus file returns: ", r.status_code)
	if r.status_code != 201:
	   print("Failed to add corpus file")
	   print(r.text)
	   sys.exit(-1)

# Step 3: Get status of corpus file just added.
# After corpus is uploaded, there is some analysis done to extract OOVs.
# One cannot upload a new corpus or words while this analysis is on-going so
# we need to loop until the status becomes 'analyzed' for this corpus.
def get_corpus_file_status(customID, corpus_name):
	print("Checking status of corpus analysis...")
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/"+customID+"/corpora/"+corpus_name
	r = requests.get(uri, auth=(username,password), verify=False, headers=headers)
	respJson = r.json()
	status = respJson['status']
	time_to_run = 10
	while (status != 'analyzed'):
	    time.sleep(10)
	    r = requests.get(uri, auth=(username,password), verify=False, headers=headers)
	    respJson = r.json()
	    status = respJson['status']
	    print("status: ", status, "(", time_to_run, ")")
	    time_to_run += 10

	print("Corpus analysis done!")

# Get status of model - only continue to training if 'ready'
def get_model_status(customID):
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/"+customID
	r = requests.get(uri, auth=(username,password), verify=False, headers=headers)
	respJson = r.json()
	status = respJson['status']
	print("Checking status of model for multiple words...")
	time_to_run = 10
	while (status != 'ready'):
	    time.sleep(10)
	    r = requests.get(uri, auth=(username,password), verify=False, headers=headers)
	    respJson = r.json()
	    status = respJson['status']
	    print("status: ", status, "(", time_to_run, ")")
	    time_to_run += 10

	print("Multiple words added!")

# Step 5: Start training the model
# After starting this step, need to check its status and wait until the
# status becomes 'available'.
def start_training_model(customID):
	print("\nTraining custom model...")
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/"+customID+"/train"
	data = {}
	jsonObject = json.dumps(data).encode('utf-8')
	r = requests.post(uri, auth=(username,password), verify=False, data=jsonObject)

	print("Training request returns: ", r.status_code)
	if r.status_code != 200:
	   print("Training failed to start - exiting!")
	   sys.exit(-1)

# Get status of training and loop until done
def get_training_status(customID):
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/"+customID
	r = requests.get(uri, auth=(username,password), verify=False, headers=headers)
	respJson = r.json()
	status = respJson['status']
	time_to_run = 10
	while (status != 'available'):
	    time.sleep(10)
	    r = requests.get(uri, auth=(username,password), verify=False, headers=headers)
	    respJson = r.json()
	    status = respJson['status']
	    print("status: ", status, "(", time_to_run, ")")
	    time_to_run += 10

	print("Training complete!")

	print("\nGetting custom models...")
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations"
	r = requests.get(uri, auth=(username,password), verify=False, headers=headers)

	print("Get models returns: ", r.status_code)
	print(r.text)

# STEP 6 (OPTIONAL): TO DELETE THE CUSTOM MODEL:
def delete_custom_model(customID):
	print("\nDeleting custom model...")
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/"+customID
	r = requests.delete(uri, auth=(username,password), verify=False, headers=headers)
	respJson = r.json()
	print("Model deletion returns: ", r.status_code)

# STEP 7 (OPTIONAL): TO LIST THE CUSTOM MODEL:
def list_custom_model():
	print("\nGetting custom models...")
	uri = "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations"
	r = requests.get(uri, auth=(username,password), verify=False, headers=headers)
	print("Get models returns: ", r.status_code)
	print(r.text)

def dictionary_customization(name, base_model_name, description, corpus_file, corpus_name):
	customID = create_custom_model(name, base_model_name, description)
	add_corpus_file(customID, corpus_file, corpus_name)
	get_corpus_file_status(customID, corpus_name)
	get_model_status(customID)
	start_training_model(customID)
	get_training_status(customID)
	list_custom_model()

if __name__ == '__main__':
    dictionary_customization("test custom model","en-US_BroadbandModel","test model","test_corpus.txt","test_corpus")

