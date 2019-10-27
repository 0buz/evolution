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
from rest_framework.renderers import JSONRenderer

import io
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User


from jobmarket.models import Job
from jobmarket.serializers import JobSerializer, UserSerializer
from jobmarket.permissions import IsOwnerOrReadOnly
from evolution.utils import csvrecords
import logging


class CSVUpload(APIView):
    renderer_classes = [TemplateHTMLRenderer,]
    template_name = 'csvupload.html'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)
    #serializer_class = JobSerializer


    def get(self, request):

        return render(request, self.template_name)

    def post(self, request):
        latest_id = Job.objects.latest('id').id   # get latest table id before upload starts
        source_file = request.FILES['csv_file']
        #import pdb; pdb.set_trace()
        data_set = io.TextIOWrapper(source_file)

        count = 0
        reader = csvrecords(data_set)   # yield csv row by row to mitigate potential issues with very large files
        #rdr = csv.DictReader(data_set)
        logging.getLogger("info_logger").info(f"Uploading {source_file}...")
        success = True
        for item in reader:
            serializer = JobSerializer(data=item)
            try:
                serializer.is_valid()
                serializer.save(owner=self.request.user)
            except Exception as err:
                #if Exception, then rollback upload
                success = False
                current_latest_id=Job.objects.latest('id').id   # get what is now the latest ID
                logging.getLogger("error_logger").error(f"{err}. Occurred at record {serializer}.")
                items=Job.objects.filter(id__in=[id for id in range(latest_id+1,current_latest_id+1)])   # get all the successfully uploaded records and delete them
                for item in items:
                    item.delete()
                    #logging.getLogger("error_logger").error(f"{item} record deleted.")
                logging.getLogger("error_logger").error(f"Upload rolled back! {len(items)} records deleted.")
                break
            count += 1
        if success:
            messages.success(request, f"Upload completed successfully for file \"{source_file}\" - {count} records uploaded.")
            logging.getLogger("info_logger").info(f"Upload completed successfully - {count} records uploaded.")
        else:
            messages.error(request, f"Upload failed for file {source_file}! No new records added.")
        #return render(request, self.template_name, )
        return HttpResponseRedirect(self.request.path_info)   #path_info stores current url i.e. refresh the page; this is to avoid resubmitting the same file for upload on manual refresh

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
   # renderer_classes = [JSONRenderer]

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


class HTMLJobList(APIView):
    """Whilst Django REST Framework aim is on buidling web APIs, this class is simply an experiment on using HTML templates."""
    model = Job
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobslist.html'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request):
        queryset = Job.objects.all()
        return Response({'jobs': queryset})


class HTMLJobDetail(APIView):
    """Whilst Django REST Framework aim is on buidling web APIs, this class is simply an experiment on using HTML templates."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobsdetail.html'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

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
