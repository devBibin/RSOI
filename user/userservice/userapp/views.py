# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.contrib.auth.models import Permission, User, Group


def get_users(request):
	users = User.objects.all()
	response_data = {}
	response_data["users"] = []
	for u in users:
		item = {}
		item["username"] = u.username
		if (len(u.groups.values_list('name',flat=True)) == 0):
			item["groups"] = []
		else:
			item["groups"] = list(u.groups.values_list('name',flat=True))
		response_data["users"].append(item)
	return JsonResponse(response_data)

def set_group(request):
	pass
'''
def get_test_by_id(request, test_id):
	test = Test.objects.get(id=test_id)
	response_data = {}
	response_data["theme"] = test.test_theme
	response_data["intro"] = test.test_introduction
	response_data["author"] = str(test.test_to_author)
	return JsonResponse(response_data)'''