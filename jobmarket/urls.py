from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from jobmarket import views

urlpatterns = [
    path('jobmarket/', views.JobList.as_view()),
    path('jobmarket/<int:pk>/', views.JobDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)