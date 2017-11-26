# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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
	rate = models.IntegerField()
	remark = models.CharField(max_length =1500)

		
