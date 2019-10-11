from django.utils import timezone
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from datetime import datetime

# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Job(models.Model):
    title = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=20, default='')
    location = models.CharField(max_length=100, default='')
    duration = models.CharField(max_length=30, default='')
    start_date = models.CharField(max_length=30, default='')
    rate = models.CharField(max_length=30, default='')
    recruiter = models.CharField(max_length=50, default='')
    posted_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(default='')
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='jobs', on_delete=models.CASCADE)
    #highlighted = models.TextField(default='')
    # language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    # style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


# class JobDescription(models.Model):
#     job = models.ForeignKey(Job, related_name='desc2job', on_delete=models.CASCADE)
#     description = models.TextField(blank=False)
# #     created_date = models.DateTimeField(default=timezone.now)
# #    # highlighted = models.TextField(default='')
#
#     class Meta:
#         ordering = ['id']
#
#     def __str__(self):
#         return str(self.jobid)

