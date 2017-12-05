from django.test import TestCase, Client
import json
from django.core.urlresolvers import reverse
import requests_mock
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission, User, Group


csrf_client = Client(enforce_csrf_checks=True)
'''
    url(r'^tests/(?P<test_id>[0-9]+)/questions/(?P<question_id>[0-9]+)$', gv.get_question_by_id),
    url(r'^tests/(?P<test_id>[0-9]+)/questions$', gv.get_questions_by_test),
    url(r'^tests/(?P<test_id>[0-9]+)/$', gv.get_test_by_id),
    url(r'^users/billing/$', gv.billing_user),
    url(r'^creative/$', gv.creative_tasks)
'''
class ViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username= "Valentin", password="123")

	def test_views_get_tests(self):
		response = self.client.get("/tests/")
		self.assertEqual(response.status_code, 200)

	def test_views_get_test_by_id(self):
		self.client.login(username="Valentin", password="123")
		response = self.client.get("/tests/1/")
		self.assertEqual(response.status_code, 200)

	def test_views_get_questions_by_test(self):
		self.client.login(username="Valentin", password="123")
		response = self.client.get("/tests/1/questions/")
		self.assertEqual(response.status_code, 200)

	def test_views_get_users(self):
		response = self.client.get("/users/")
		self.assertEqual(response.status_code, 200)

	
	def test_views_billing_user(self):
		data = {'u_id':'1'}
		c = Client() #above, from django.test import TestCase,Client
		c.login(username="Valentin", password="123")
		#optional, but may be necessary for your configuration: c.login("username","password")
		response = c.post('/users/billing/',params=data)
		self.assertEqual(response.status_code, 200)
	

	def test_views_creative_tasks(self):
		data = {'user':'1', 'task':'2'}
		c = Client() #above, from django.test import TestCase,Client
		c.login(username="Valentin", password="123")
		#optional, but may be necessary for your configuration: c.login("username","password")
		response = c.post('/creative/',params=data)
		self.assertEqual(response.status_code, 200)