# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import *


class ViewTest(TestCase):
	def test_view_create_bill(self):
		response = self.client.post("/billing/",data={'u_id' : 1, 'type' : "type", 'amount': "1.1"})
		b = Billing.objects.filter(pk=1)[0]
		self.assertEqual(b.user_id,1)