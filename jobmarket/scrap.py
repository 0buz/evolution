from jobmarket.models import Job
from .serializers import JobSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


test1 = Job(title="Title CLI")
test1.save()