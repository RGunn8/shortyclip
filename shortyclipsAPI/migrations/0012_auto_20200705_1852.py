# Generated by Django 3.0.7 on 2020-07-05 18:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortyclipsAPI', '0011_auto_20200623_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='clip',
            name='followTags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='clip',
            name='shared',
            field=models.IntegerField(default=0),
        ),
    ]
