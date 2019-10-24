import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')

from csv import DictReader

def csvrecords(file):
    """Function to yield one row at a time. This will be used to when uploading csv data via REST API."""
    for item in DictReader(file):
        yield item