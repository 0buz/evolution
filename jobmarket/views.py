import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')

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
from jobmarket.models import Job
from jobmarket.serializers import JobSerializer, UserSerializer
from jobmarket.permissions import IsOwnerOrReadOnly
from evolution.utils import csvrecords
from django.http import HttpResponseRedirect
from jobmarket.forms import UploadFileForm
from rest_framework_csv import renderers as csvrend

"""
def upload_file(request):
    template = "csvupload.html"
    prompt = {
        'order': 'Order should be Title, Type, Location, Duration, Start Date, Rate, Recruiter, Post Date'
    }
    if request.method == "GET":
        return render(request, "csvupload.html", prompt) #render(request, template, prompt)

    csv_file = request.FILES['csv_file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a csv file.")

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     # handle_uploaded_file(request.FILES['file'])
        #     return HttpResponseRedirect('/success/url/')

        for chunk in csv_file.chunks():
            data=chunk.decode('UTF-8')
            csvdata=csv.DictReader(data)
            for c in csvdata:
                print(c)
            print("\n",csvdata)
            print(type(csvdata))
            #Job.objects.create()


    else:
        form = UploadFileForm()
    return render(request, 'csvupload.html', {'form': form})
"""



class CSVUpload(APIView):
    renderer_classes = [TemplateHTMLRenderer, csvrend.CSVRenderer,]
    #renderer_classes = [TemplateHTMLRenderer]
    template_name = 'csvupload.html'
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    parser_classes = (MultiPartParser, FormParser)
    #serializer_class = JobSerializer

    def get(self, request):
        queryset = Job.objects.all()
        return Response({'jobs': queryset})

    # def get_renderer_context(self):
    #     context = super().get_renderer_context()
    #     context['header'] = (self.request.GET['fields'].split(",")
    #                          if 'fields' in self.request.GET else None)
    #     return context

    def post(self, request):
        my_file = request.FILES['csv_file']
        # csv_source = csvrecords(my_file)
        # io_string = io.StringIO(csv_source)
        # my_file = open("/home/adrian/all/evolution/evolution/data/preprocessed/preprocessed20191007_test.csv")
        # data_set = io.StringIO(my_file.read().decode('UTF-8'))
        data_set = io.TextIOWrapper(my_file)
        print("\nDATA SET >>>>>>>", data_set)
        # csv_source = csvrecords(my_file)
        # print("\nCSV SOURCE >>>>>>>",next(csv_source))
        # data_set = my_file.read()
        # io_string = io.StringIO(csv_source)
        # next(io_string)
        count = 0
        rdr = csv.DictReader(data_set)
        print("\nRequest DAta KKKKKKKKKKKKKKKK",request.data)
        #rdr = csvrecords(data_set)
       # print("XXXXXXXXXXXXXXXXXXXX", next(rdr))
        for item in rdr:
            print("\n", count, item)
            serializer = JobSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            #print(serializer.data)
            serializer.save(owner=self.request.user)
            # #serializer.create(validated_data=item)
            #
            count += 1
        print("Count column:", count)

        # job = get_object_or_404(Job, pk=pk)
        # serializer = JobSerializer(job, data=request.data)
        # if not serializer.is_valid():
        #     return Response({'serializer': serializer, 'job': job})
        # serializer.save()
        # return redirect('jobslist')

        csv_source = csvrecords(my_file)  # .read().decode("UTF-8"))
        #  print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", type(my_file))
        # print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", type(csv_source))
        # print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", type(record))

        return render(request, self.template_name)


#     my_saved_file = open(filename)  # there you go


# @permission_required("admin.can_add_log_entry")
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

    def get(self, request):
        queryset = Job.objects.all()
        return Response({'jobs': queryset})


class HTMLJobDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobsdetail.html'

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        serializer = JobSerializer(job, context={'request': request})
        return Response({'serializer': serializer, 'job': job})

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        serializer = JobSerializer(job, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'job': job})
        serializer.save()
        return redirect('jobslist')


@api_view(['GET'])
def api_root(request, format=None):  # API root endpoint
    return Response({
        'Users': reverse('user-list', request=request, format=format),
        'Jobs': reverse('job-list', request=request, format=format),
        'HTML Jobs': reverse('jobslist', request=request, format=format),
        'Upload': reverse('csvupload', request=request, format=format),
        # 'Upload Form': reverse('csvuploadform', request=request, format=format),
    })


class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
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
