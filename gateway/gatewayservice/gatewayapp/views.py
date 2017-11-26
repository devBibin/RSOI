# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests

TEST_DOMAIN = "http://localhost:8081"
USER_DOMAIN = "http://localhost:8082"

@login_required
def get_tests(request):
	r = requests.get(TEST_DOMAIN+request.get_full_path())
	context = {'d': r.json()}
	return render(request, 'gatewayapp/test_list.html', context)

@login_required
def get_test_by_id(request, test_id):
	res = requests.get(TEST_DOMAIN+request.get_full_path())
	return HttpResponse(res)

@login_required
def get_questions_by_test(request, test_id):
	r = requests.get(TEST_DOMAIN+request.get_full_path())
	context = {'d': r.json()}
	return render(request, 'gatewayapp/question_list.html', context)

@login_required
def get_question_by_id(request, test_id, question_id):
	if (request.method == "GET"):
		r = requests.get(TEST_DOMAIN+request.get_full_path())
		context = {'q': r.json()}
		#return HttpResponse(r)
		return render(request, 'gatewayapp/question.html', context)
	else:
		print (request.POST)
		return HttpResponse(request.POST["choice"])

def get_users(request):
	r = requests.get(USER_DOMAIN+request.get_full_path())
	return HttpResponse(r)

def authenticate_user(request):
	user = authenticate(request, username="john", password="johnpassword")
	if user is not None:
		login(request, user)
		return HttpResponse("Authorized as john")
	else:
		return HttpResponse("B")
	#context = {'d': r.json()}
	#return render(request, 'gatewayapp/test_list.html', context)