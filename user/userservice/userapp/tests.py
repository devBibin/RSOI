from django.test import TestCase
import json
from django.core.urlresolvers import reverse
from models import *
from django.contrib.auth.models import Permission, User, Group


class ViewTest(TestCase):
	def setUp(self):
		User.objects.create(username= "Valentin", password="123")
		u = User.objects.all()[0]
		Group.objects.create(name='simple user') 
		g = Group.objects.all()[0]
		g.user_set.add(u)
		Group.objects.create(name='advanced user') 


	def test_view_get_users(self):
		response = self.client.get("/users/")
		json_data = json.loads(response.content)
		self.assertEqual(len(json_data["users"]),1)

	def test_view_alter_user_group(self):
		response = self.client.get("/users/")
		json_data = json.loads(response.content)
		print json_data
		response = self.client.post("/users/alter_group/",data={'u_id' : 1})
		u = User.objects.filter(username = "Valentin")[0]
		u_groups = list(u.groups.values_list('name',flat=True))
		self.assertEqual(u_groups[0], "advanced user")