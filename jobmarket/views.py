from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Job
from .serializers import JobSerializer, UserSerializer

import csv, io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from .models import Job
from .serializers import JobSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

@api_view(['GET'])
def api_root(request, format=None):  # API root endpoint
    return Response({
        'Users': reverse('user-list', request=request, format=format),
        'Jobs': reverse('job-list', request=request, format=format),
    })


class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer): # new
        serializer.save(owner=self.request.user)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class JobDescriptionList(generics.ListCreateAPIView):
#     queryset = JobDescription.objects.all()
#     serializer_class = JobDescriptionSerializer
#
#
# class JobDescriptionDetail(generics.RetrieveAPIView):
#     queryset = JobDescription.objects.all()
#     serializer_class = JobDescriptionSerializer


# class JobHighlight(generics.GenericAPIView):
#     queryset = Job.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)
#     serializer_class = JobSerializer
#
#     def get(self,request,*args,**kwargs):
#         job = self.get_object()
#         return Response(job.highlighted)

#@permission_required("admin.can_add_log_entry")
# def job_upload(request):
#     template = "job_upload.html"
#     prompt = {
#         'order': 'Order should be Title, Type, Location, Duration, Start Date, Rate, Recruiter, Post Date'
#     }
#
#     if request.method =="GET":
#         return render(request, template, prompt)
#
#     csv_file = request.FILES['file']
#
#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, "This is not a csv file.")
#
#     data_set = csv_file.read().decode('UTF-8')
#     io_string = io.StringIO(data_set)
#     next(io_string)
#     for column in csv.reader(io_string, delimiter=',', quotechar="|"):
#         _, created = Job.objects.