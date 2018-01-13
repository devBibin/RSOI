# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.contrib.auth.models import Permission, User, Group
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
from oauth2_provider.decorators import protected_resource


def get_users(request):
	users = User.objects.all()
	if (len(users) == 0):
		return JsonResponse({'status':'false','message':'Users not found'}, status=204)
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
	u = User.objects.filter(pk =request.POST["user_id"])
	u_groups = User.groups.through.objects.get(user = u)
	u_groups.group = Group.objects.filter(name = "advanced user")[0]
	u_groups.save()
	return HttpResponse(status = 200)


def is_admin(user):
	return str(User.groups.through.objects.get(user = user).group) == "admin"



@protected_resource()
def rights_check(request):
	user = request.resource_owner
	return HttpResponse(user.pk, status=200)


@protected_resource()
def check_admin_rights(request):
	user = request.resource_owner
	if is_admin(user):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=403)