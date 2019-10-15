from rest_framework import serializers
from jobmarket.models import Job
from django.contrib.auth.models import User


# JobSerializer class uses the model and outputs the table fields
class JobSerializer(serializers.HyperlinkedModelSerializer):  # updated from serializers.ModelSerializer
    owner = serializers.ReadOnlyField(source='owner.username')

    # highlight = serializers.HyperlinkedIdentityField(view_name='job-detail', format='html')
    # jobs_description = serializers.PrimaryKeyRelatedField(source="desc2job", many=False, read_only=True)

    class Meta:
        model = Job
        fields = (
            'url', 'id', 'title', 'type', 'location', 'duration', 'start_date', 'rate', 'recruiter', 'posted_date',
            'description',
            'created_date', 'owner')  # added 'url', 'owner' fields

    def create(self, validated_data):
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.type)
        instance.location = validated_data.get('location', instance.location)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.recruiter = validated_data.get('recruiter', instance.recruiter)
        instance.posted_date = validated_data.get('posted_date', instance.posted_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


# class JobDescriptionSerializer(serializers.HyperlinkedModelSerializer):
#     # id = serializers.IntegerField(read_only=True)
#     # highlight = serializers.HyperlinkedIdentityField(view_name='jobdescription-detail', format='html')
#     class Meta:
#         model = JobDescription
#         fields = ('url', 'id', 'job', 'description', 'created_date')  # added 'url' fields

class UserSerializer(serializers.HyperlinkedModelSerializer):  # updated from serializers.ModelSerializer
    jobs = serializers.HyperlinkedRelatedField(many=True, view_name='job-detail',
                                               read_only=True)  # this is "related_name" defined in models!!!

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'jobs')  # added 'url', 'jobs' fields


# class CSVUploadSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = File
#             fields = "__all__"
