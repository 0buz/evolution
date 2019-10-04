from rest_framework import generics, renderers
from .models import Job, JobDescription
from .serializers import JobSerializer, JobDescriptionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


@api_view(['GET'])
def api_root(request, format=None):  # API root endpoint
    return Response({
        'Jobs': reverse('job-list', request=request, format=format),
        'Job Descriptions': reverse('jobdescription-list', request=request, format=format)
    })


class JobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDetail(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDescriptionList(generics.ListAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer


class JobDescriptionDetail(generics.RetrieveAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer


# class JobHighlight(generics.GenericAPIView):
#     queryset = Job.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)
#     serializer_class = JobSerializer
#
#     def get(self,request,*args,**kwargs):
#         job = self.get_object()
#         return Response(job.highlighted)

