from django.contrib import admin
from jobmarket.models import Job

# this is to control readonly fields on creation
# class JobAdmin(admin.ModelAdmin):
#     readonly_fields = ('description',)

#admin.site.register(Job, JobAdmin)
admin.site.register(Job)