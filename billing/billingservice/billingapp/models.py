# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Billing(models.Model):
	user_id = models.IntegerField()
	payment_for_type = models.CharField(max_length=100, default = "Creative tasks")
	transaction_amount = models.FloatField()
	transaction_date = models.DateTimeField()
	transaction_status = models.CharField(max_length = 30, default = "Not paid")
