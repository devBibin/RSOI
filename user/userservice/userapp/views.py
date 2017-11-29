# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.contrib.auth.models import Permission, User, Group
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse


def get_users(request):
	print "JOPA"
	users = User.objects.all()
	response_data = {}
	response_data["users"] = []
	for u in users:
		item = {}
		item["id"] = u.pk
		item["username"] = u.username
		if (len(u.groups.values_list('name',flat=True)) == 0):
			item["groups"] = []
		else:
			item["groups"] = list(u.groups.values_list('name',flat=True))
		response_data["users"].append(item)
	return JsonResponse(response_data)

@csrf_exempt
def alter_user_group(request):
	u = User.objects.filter(pk =request.POST["u_id"])
	u_groups = User.groups.through.objects.get(user = u)
	u_groups.group = Group.objects.filter(name = "advanced user")[0]
	u_groups.save()
	return HttpResponse(requests.codes["ok"])