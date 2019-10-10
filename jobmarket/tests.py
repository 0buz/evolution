from django.test import TestCase
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')
from rest_framework.test import RequestsClient
from rest_framework.test import APIRequestFactory


# print(os.getcwd())
# os.chdir("/home/adrian/all/evolution/evolution")
client = RequestsClient()
response = client.get('http://testserver/jobs')

assert response.status_code == 200

response = client.get('http://testserver/jobdescriptions')

assert response.status_code == 200



# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/jobs/', {'title': 'test title', 'type':'Contract'})
request = factory.get('127.0.0.1:8000/jobs/')

testreq = factory.options('/jobs/')
request = factory.post('/jobs/', json.dumps({'title': 'json.dumps'}), content_type='application/json')



from rest_framework.test import APIClient

client = APIClient()
client.post('/jobs/', {'title': 'with client.APIClient with server off'}, format='json')
client.options('/jobs/')

client.post('/jobdescriptions/', {'jobid':'6','description': 'dummy desc'}, format='json')

type(client.head)