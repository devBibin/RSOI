from django.test import TestCase
from models import *

class ViewTest(TestCase):
	def test_view_create_bill(self):
		response = self.client.post("/creative/add/",data={'user' : 1, 'creative_task' : "Test answer"})
		ct = CreativeTask.objects.filter(pk=1)[0]
		self.assertEqual(ct.user_id,1)