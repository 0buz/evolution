# import io, csv
# from django import forms
# from .models import Job
# from django.contrib.auth.models import User
#
#
# class DataForm(forms.Form):
#     data_file = forms.FileField()
#
#     def process_date(self):
#         f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
#         csv_reader = csv.reader()
#         next(csv_reader)
#         for row in csv_reader:
#             Job.objects.create

from django import forms
from jobmarket.models import Job

class UploadFileForm(forms.Form):

    title = forms.CharField(max_length=50)
    file = forms.FileField()

    # class Meta:
    #     model = Job
    #     fields = ('name', 'email', 'phone', 'message')