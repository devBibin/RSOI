# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

class TestAnswer(models.Model):
	test_id = models.IntegerField()
	question_id = models.IntegerField()
	choice_id = models.IntegerField()
	user_id = models.IntegerField()
	is_true = models.BooleanField()

class CreativeTaskAnswer(models.Model):
	user_id = models.IntegerField()
	task_id = models.IntegerField()
	status = models.CharField(max_length=20, default ="processing")
	rate = models.IntegerField(default=0)
	remark = models.CharField(max_length =1500)

class RequestInfo(models.Model):
    guid = models.CharField(max_length=32)
    method = models.CharField(max_length=10)
    uri = models.CharField(max_length=256)
    params = models.CharField(max_length=2500)
    timestamp = models.DateTimeField(default=datetime.utcnow)
    status = models.IntegerField(default=200)
    errors = models.CharField(max_length=2500, default='{}')

		
