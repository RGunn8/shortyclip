# Generated by Django 2.1.7 on 2020-06-14 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortyclipsAPI', '0002_auto_20200613_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clip',
            name='likes',
        ),
    ]
