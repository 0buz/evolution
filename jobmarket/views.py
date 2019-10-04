from rest_framework import generics
from .models import Job, JobDescription
from .serializers import JobSerializer, JobDescriptionSerializer

class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDescriptionList(generics.ListCreateAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer


class JobDescriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
