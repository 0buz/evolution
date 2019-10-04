from django.contrib import admin
from .models import Job, JobDescription

admin.site.register(Job)
admin.site.register(JobDescription)