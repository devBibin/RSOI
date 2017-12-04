# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import *
import json

class ViewTest(TestCase):
	def setUp(self):
		for i in range(10):
			TestAnswer.objects.create(test_id= 1, question_id =i, choice_id = 3, user_id = 1, is_true = True)

	def test_view_save_answer_info(self):
		response = self.client.post("/stats/save_answer/",data={'test' : 1, 'question' : 1, 'choice': 3, 'user': 1, 'is_true':True})
		a = TestAnswer.objects.filter(question_id=1)[0]
		self.assertEqual(a.choice_id,3)

	def test_view_save_creative_task_info(self):
		response = self.client.post("/stats/save_creative/",data={'task' : 3, 'user' : 1})
		ct = CreativeTaskAnswer.objects.filter(task_id=3)[0]
		self.assertEqual(ct.task_id,3)

	def test_view_get_stats_by_question(self):
		response = self.client.get("/stats/get_stats/user/1/?question=1&question=2&question=111")
		json_data = json.loads(response.content)
		self.assertEqual(len(json_data["replied"]), 2)