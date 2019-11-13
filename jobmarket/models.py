from django.utils import timezone
from django.db import models
from enum import Enum, IntEnum




class Job(models.Model):
    # class TypeEnum(IntEnum):
    #     Any = 1
    #     Permanent = 2
    #     Contract = 3
    #     ContractPermanent = 4
    #     PartTimeTemporarySeasonal = 5

    title = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=30, default='')
    location = models.CharField(max_length=100, default='')
    duration = models.CharField(max_length=100, default='')
    start_date = models.CharField(max_length=100, default='')
    rate = models.CharField(max_length=100, default='')
    recruiter = models.CharField(max_length=100, default='')
    posted_date = models.DateTimeField()
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

# class File(models.Model):
#     file = models.FileField(blank=False, null=False)
#     def __str__(self):
#         return self.file.name

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
