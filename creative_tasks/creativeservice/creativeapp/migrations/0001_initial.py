# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreativeTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('task_type', models.CharField(default='Writing', max_length=20)),
                ('answer', models.CharField(max_length=2500)),
            ],
        ),
    ]
