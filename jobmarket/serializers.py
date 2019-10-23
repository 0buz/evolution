from rest_framework import serializers
from jobmarket.models import Job
from django.contrib.auth.models import User
from rest_framework.pagination import BasePagination

# JobSerializer class uses the model and outputs the table fields
class JobSerializer(serializers.HyperlinkedModelSerializer):  # updated from serializers.ModelSerializer
    owner = serializers.ReadOnlyField(source='owner.username')
    location = serializers.CharField(allow_blank=True)
    duration = serializers.CharField(allow_blank=True)
    start_date = serializers.CharField(allow_blank=True)
    rate = serializers.CharField(allow_blank=True)
    posted_date = serializers.DateTimeField(input_formats=[("%d/%m/%Y %H:%M:%S")])

    #duration = CharField(max_length=20, validators=[ < UniqueValidator(queryset=CustomerReportRecord.objects.all()) >])

    # def validate_duration(self,value):
    #     if not value:
    #         raise serializers.ValidationError("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa.")

    # def to_internal_value(self, data):
    #     if data.get('duration') == '':
    #         print("THESE ARE THE DURATION VALUES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ", data.get('duration'))
    #         data.pop('duration')
    #
    #     return super(JobSerializer, self).to_internal_value(data)

    class Meta:
        model = Job
        fields = (
            'url', 'id', 'title', 'type', 'location', 'duration', 'start_date', 'rate', 'recruiter', 'posted_date',
            'description', 'created_date', 'owner')  # added 'url', 'owner' fields

    def create(self, validated_data):
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.type)
        instance.location = validated_data.get('location', instance.location)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.start_date = validated_data.get('start date', instance.start_date)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.recruiter = validated_data.get('recruiter', instance.recruiter)
        instance.posted_date = validated_data.get('posted_date', instance.posted_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):  # updated from serializers.ModelSerializer
    jobs = serializers.HyperlinkedRelatedField(many=True, view_name='job-detail',
                                               read_only=True)  # this is "related_name" defined in models!!!

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'jobs')  # added 'url', 'jobs' fields
