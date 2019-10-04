from rest_framework import serializers
from .models import Job, JobDescription
from django.contrib.auth.models import User


#AprestSerializer class uses our model and outputs the table fields
class JobSerializer(serializers.HyperlinkedModelSerializer):    #updated from serializers.ModelSerializer
   # id = serializers.IntegerField(read_only=True)
    # owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='job-detail', format='html')

    class Meta:
        model = Job
        fields = ('url', 'id', 'title', 'type', 'location','duration', 'start_date', 'rate', 'recruiter', 'posted_date',
                  'created_date', 'highlight')   #added 'url', 'highlight' fields


class JobDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    highlight = serializers.HyperlinkedIdentityField(view_name='jobdescription-detail', format='html')
    class Meta:
        model = JobDescription
        fields = ('url', 'id', 'jobid', 'description', 'created_date', 'highlight')   #added 'url', 'highlight' fields





# class UserSerializer(serializers.HyperlinkedModelSerializer):     #updated from serializers.ModelSerializer
#
#     #aprests = serializers.PrimaryKeyRelatedField(many=True, queryset=Aprest.objects.all())
#     aprests = serializers.HyperlinkedRelatedField(many=True, view_name='aprest-detail', read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('url','id','username','aprests')   #added 'url' field






