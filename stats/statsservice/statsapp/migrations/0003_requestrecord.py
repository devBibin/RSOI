# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-12 09:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsapp', '0002_auto_20171128_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(max_length=32)),
                ('method', models.CharField(max_length=10)),
                ('uri', models.CharField(max_length=100)),
                ('params', models.CharField(max_length=4000)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('status', models.IntegerField(default=200)),
                ('errors', models.CharField(default='{}', max_length=4000)),
            ],
        ),
    ]
