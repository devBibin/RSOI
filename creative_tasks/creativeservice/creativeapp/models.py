# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class CreativeTask(models.Model):
	user_id = models.IntegerField()
	task_type = models.CharField(max_length = 20, default = "Writing")
	answer = models.CharField(max_length = 2500)