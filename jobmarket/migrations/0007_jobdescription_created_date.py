# Generated by Django 2.2.6 on 2019-10-04 13:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobmarket', '0006_auto_20191004_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdescription',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]