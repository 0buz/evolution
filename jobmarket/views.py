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


import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jobmarket.models import Job
from jobmarket.serializers import JobSerializer, UserSerializer
from jobmarket.permissions import IsOwnerOrReadOnly
from evolution.utils import csvrecords
import logging

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
    renderer_classes = [TemplateHTMLRenderer,]
    template_name = 'csvupload.html'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)
    #serializer_class = JobSerializer

    def get(self, request):
        queryset = Job.objects.all()
        return Response({'jobs': queryset})

    def post(self, request):
        source_file = request.FILES['csv_file']
        #import pdb; pdb.set_trace()
        data_set = io.TextIOWrapper(source_file)
        count = 0
        reader = csvrecords(data_set)   # yield csv row by row to mitigate potential issues with very large files
        #rdr = csv.DictReader(data_set)
        logging.getLogger("info_logger").info(f"{source_file} uploading...")
        for item in reader:
            serializer = JobSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=self.request.user)
            count += 1
        logging.getLogger("info_logger").info(f"{count} records uploaded.")
        return render(request, self.template_name)


class HTMLJobList(APIView):
    model = Job
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobslist.html'
    context_object_name = 'jobs'
    pagination_by = 10

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




def index(request):
    user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'core/user_list.html', { 'users': users })
