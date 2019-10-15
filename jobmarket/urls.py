from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from jobmarket import views
from jobmarket import forms

urlpatterns = [
    path('jobs/', views.JobList.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name='job-detail'),
    path('htmljobs/', views.HTMLJobList.as_view(), name='jobslist'),
    path('htmljobs/<int:pk>/', views.HTMLJobDetail.as_view(), name='jobsdetail'),
    path('upload/', views.CSVUpload.as_view(), name='csvupload'),
    path('uploadform/', views.upload_file, name='csvuploadform'),
   # path('jobdescriptions/', views.JobDescriptionList.as_view(), name='jobdescription-list'),
  #  path('jobdescriptions/<int:pk>/', views.JobDescriptionDetail.as_view(), name='jobdescription-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('', views.api_root),
]


urlpatterns = format_suffix_patterns(urlpatterns)



