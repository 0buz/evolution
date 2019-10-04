from django.db import models

# Create your models here.


# snippets/models.py
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

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
    posted_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    # language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    # style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class JobDescription(models.Model):
    jobid = models.ForeignKey(Job, related_name='jobspec', on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.jobid)
