from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

import csv, io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from .models import Job
from .serializers import JobSerializer, UserSerializer, CSVUploadSerializer
from .permissions import IsOwnerOrReadOnly


class CSVUpload(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'csvupload.html'
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    permission_classes = (permissions.AllowAny)


    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        my_file = request.FILES['file_field_name']
        filename = ''
        with open(filename, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)

        my_saved_file = open(filename)  # there you go


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

class HTMLJobList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobslist.html'

    def get(self,request):
        queryset = Job.objects.all()
        return Response({'jobs': queryset})


class HTMLJobDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobsdetail.html'

    def get(self,request, pk):
        job = get_object_or_404(Job, pk=pk)
        serializer = JobSerializer(job, context={'request': request})
        return Response({'serializer':serializer, 'job':job})

    def post(self,request, pk):
        job = get_object_or_404(Job, pk=pk)
        serializer = JobSerializer(job, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer':serializer, 'job':job})
        serializer.save()
        return redirect('jobslist')


@api_view(['GET'])
def api_root(request, format=None):  # API root endpoint
    return Response({
        'Users': reverse('user-list', request=request, format=format),
        'Jobs': reverse('job-list', request=request, format=format),
        'HTML Jobs': reverse('jobslist', request=request, format=format),
        'Upload': reverse('csvupload', request=request, format=format),
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

