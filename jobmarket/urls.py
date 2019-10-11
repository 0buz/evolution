from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from jobmarket import views

urlpatterns = [
    path('jobs/', views.JobList.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name='job-detail'),
   # path('jobdescriptions/', views.JobDescriptionList.as_view(), name='jobdescription-list'),
  #  path('jobdescriptions/<int:pk>/', views.JobDescriptionDetail.as_view(), name='jobdescription-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('', views.api_root),
]


urlpatterns = format_suffix_patterns(urlpatterns)



