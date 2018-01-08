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

def index(request):
	return render(request, 'renderapp/index.html', {})

def get_tests(request):
	r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/test_list.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)

def get_test_by_id(request, test_id):
	r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/test.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)
		


def get_questions_by_test(request, test_id):
	r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/question_list.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)



def get_question_by_id(request, test_id, question_id):
	if (request.method == "GET"):
		r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	elif (request.method == "POST"):
		r = requests.post(GATEWAY_DOMAIN+request.get_full_path())

	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/question.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)


def billing_user(request):
	if (request.method == "GET"):
		r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	elif (request.method == "POST"):
		r = requests.post(GATEWAY_DOMAIN+request.get_full_path())
	
	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/question.html', context)
	elif (r.status == 202):
		return render(request, 'renderapp/notification_page.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)


def creative_tasks(request):
	if (request.method == "GET"):
		r = requests.get(GATEWAY_DOMAIN+request.get_full_path())
	elif (request.method == "POST"):
		r = requests.post(GATEWAY_DOMAIN+request.get_full_path())
	
	context = r.json()
	if (r.status_code == 200):
		return render(request, 'renderapp/question.html', context)
	elif (r.status == 202):
		return render(request, 'renderapp/notification_page.html', context)
	else:
		return render(request, 'renderapp/error_page.html', context)


def authenticate_user(request):
	return HttpResponseRedirect(GATEWAY_DOMAIN +request.get_full_path())

def authenticate_complete(request):
	red = HttpResponseRedirect("http://localhost:8000")
	return red