# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
import json
from django.views.decorators.csrf import csrf_exempt



GATEWAY_DOMAIN = "http://localhost:8001"
SELF = "http://localhost:8000"

def index(request):
	return render(request, 'renderapp/index.html', {})

# open method
def get_tests(request):
	r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/test_list.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)

# open method
def get_test_by_id(request, test_id):
	r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/test.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)
		
 
def get_questions_by_test(request, test_id):
	auth_data = check_and_reauth(request)
	if (auth_data is not None):
		try:
			int(auth_data)
		except:
			resp = HttpResponseRedirect(SELF+request.get_full_path())
			resp.set_cookie('access', auth_data['token'])
			resp.set_cookie('refresh', auth_data['refresh'])
			return resp

		r = requests.get(GATEWAY_DOMAIN+request.get_full_path(), params = {"user_id" : str(auth_data)})
		context = r.json()
		
		if (r.status_code == 200):
			return render(request, 'renderapp/question_list.html', context)
		else:
			return render(request, 'renderapp/error_page.html', context)
	
	else:
		return HttpResponseRedirect(SELF + "/users/auth/")

 
def get_question_by_id(request, test_id, question_id):
	auth_data = check_and_reauth(request)
	if (auth_data is not None):

		try:
			int(auth_data)
		except:
			resp = HttpResponseRedirect(SELF+request.get_full_path())
			resp.set_cookie('access', auth_data['token'])
			resp.set_cookie('refresh', auth_data['refresh'])
			return resp
		
		if (request.method == "GET"):
			r = requests.get(GATEWAY_DOMAIN+request.get_full_path(), params = {"user_id" : str(auth_data)})
		elif (request.method == "POST"):
			r = requests.post(GATEWAY_DOMAIN+request.get_full_path(), data = {"user_id" : str(auth_data), 
				"choice" : str(request.POST.get("choice"))})

		context = r.json()
		if (r.status_code == 200):
			return render(request, 'renderapp/question.html', context)
		else:
			return render(request, 'renderapp/error_page.html', context)
	else:
		return HttpResponseRedirect(SELF + "/users/auth/")

 
def billing_user(request):
	auth_data = check_and_reauth(request)
	if (auth_data is not None):

		try:
			int(auth_data)
		except:
			resp = HttpResponseRedirect(SELF+request.get_full_path())
			resp.set_cookie('access', auth_data['token'])
			resp.set_cookie('refresh', auth_data['refresh'])
			return resp
		
		if (request.method == "GET"):
			r = requests.get(GATEWAY_DOMAIN+request.get_full_path(), params = {"user_id" : str(auth_data)})
		elif (request.method == "POST"):
			r = requests.post(GATEWAY_DOMAIN+request.get_full_path(), data = {"user_id" : str(auth_data),
				"type" : str(request.POST.get("type")),
				"amount" : str(request.POST.get("amount"))})
		
		context = r.json()
		if (r.status_code == 200):
			return render(request, 'renderapp/billing.html', context)
		elif (r.status_code == 202):
			return render(request, 'renderapp/notification_page.html', context)
		else:
			return render(request, 'renderapp/error_page.html', context)

	else:
		return HttpResponseRedirect(SELF + "/users/auth/")


def creative_tasks(request):
	auth_data = check_and_reauth(request)
	if (auth_data is not None):

		try:
			int(auth_data)
		except:
			resp = HttpResponseRedirect(SELF+request.get_full_path())
			resp.set_cookie('access', auth_data['token'])
			resp.set_cookie('refresh', auth_data['refresh'])
			return resp

		if (request.method == "GET"):
			r = requests.get(GATEWAY_DOMAIN+request.get_full_path(), params = {"user_id" : str(auth_data)})
		elif (request.method == "POST"):
			r = requests.post(GATEWAY_DOMAIN+request.get_full_path(), data = {"user_id" : str(auth_data),
				"creative_task" : str(request.POST.get("creative_task"))})
		
		context = r.json()
		if (r.status_code == 200):
			return render(request, 'renderapp/creative_task.html', context)
		elif (r.status_code == 202):
			return render(request, 'renderapp/notification_page.html', context)
		else:
			return render(request, 'renderapp/error_page.html', context)
	else:
		return HttpResponseRedirect(SELF + "/users/auth/")


def authenticate_user(request):
	return HttpResponseRedirect(GATEWAY_DOMAIN +request.get_full_path())


def authenticate_complete(request):
	red = HttpResponseRedirect("http://localhost:8000")
	red.set_cookie('access', request.GET['token'])
	red.set_cookie('refresh', request.GET['refresh'])
	return red

 
def reauth(request):
	resp = requests.post(GATEWAY_DOMAIN + '/users/reauth/', data={'code': str(request.COOKIES.get('refresh'))})
	if resp.status_code != 200:
		return None
	else:
		data = json.loads(resp.content)
		return data


def check_and_reauth(request):
	header = {'Authorization': 'Bearer ' + str(request.COOKIES.get('access'))}
	resp = requests.get(GATEWAY_DOMAIN + '/users/is_auth/', headers=header)
	if resp.status_code == 200:
		return resp.content
	else:
		return reauth(request)