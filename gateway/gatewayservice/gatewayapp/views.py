# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
import json
import logging

log = logging.getLogger(__name__)

TEST_DOMAIN = "http://localhost:8081"
USER_DOMAIN = "http://localhost:8082"
BILLING_DOMAIN = "http://localhost:8083"
STATS_DOMAIN = "http://localhost:8084"
CREATIVE_TASKS_DOMAIN = "http://localhost:8085"

def get_tests(request):
	log.info("User "+str(request.user.username)+" got list of tests")
	r = requests.get(TEST_DOMAIN+request.get_full_path())
	context = {'d': r.json()}
	return render(request, 'gatewayapp/test_list.html', context)

@login_required
def get_test_by_id(request, test_id):
	log.info("User "+str(request.user.username)+" got tests " + str(test_id))
	r = requests.get(TEST_DOMAIN+request.get_full_path()).json()
	r["test_id"] = test_id
	context = {'d': r}
	return render(request, 'gatewayapp/test.html', context)

@login_required
def get_questions_by_test(request, test_id):
	log.info("User "+str(request.user.username)+" got list of questions in test" + str(test_id))
	rt = requests.get(TEST_DOMAIN+request.get_full_path()).json()
	log.info("User "+str(request.user.username)+" got questions")
	
	q_ids = []
	for q in rt["questions"]:
		q_ids.append(q["id"])
	q_ids = {"question": q_ids}
	
	rs = requests.get(STATS_DOMAIN + "/stats/get_stats/user/"+str(request.user.id)+"/", params = q_ids).json()
	questions = rt["questions"]
	replied = rs["replied"]
	for i in range(len(questions)):
		if (questions[i]["id"] in replied):
			questions[i]["replied"] = "+"
		else:
			questions[i]["replied"] = "-"
	rt["questions"] = questions
	log.info("User "+str(request.user.username)+" got replied questions")
	context = {'d': rt}
	return render(request, 'gatewayapp/question_list.html', context)

@login_required
def get_question_by_id(request, test_id, question_id):
	log.info("User "+str(request.user.username)+" got questions"+str(question_id) +" in test" + str(test_id))
	if (request.method == "GET"):
		r = requests.get(TEST_DOMAIN+request.get_full_path())
		context = {'q': r.json()}
		return render(request, 'gatewayapp/question.html', context)
	else:
		request.POST = request.POST.copy()
		request.POST["question"] = question_id
		request.POST["test"] = test_id
		request.POST["user"] = request.user.id
	 	if (request.POST["choice"] == requests.get(TEST_DOMAIN + "/tests/"+test_id+"/questions/"+str(question_id)+"/answer").content):
	 		request.POST["is_true"] = True
	 	else:
	 		request.POST["is_true"] = False
		r = requests.post(STATS_DOMAIN + "/stats/save_answer/", data = request.POST)
		return HttpResponse("Your answer is" + str(request.POST["is_true"]))

def get_users(request):
	r = requests.get(USER_DOMAIN+request.get_full_path())
	return HttpResponse(r)

def authenticate_user(request):
	log.info("User authnticating")
	user = authenticate(request, username="john", password="johnpassword")
	if user is not None:
		login(request, user)
		return HttpResponse("Authorized as john")
	else:
		return HttpResponse("User not found")

@login_required
def billing_user(request):
	if (request.method == "GET"):
		log.info("User "+str(request.user.username)+" visited payment page")
		context = {'q': []}
		return render(request, 'gatewayapp/billing.html', context)
	else:
		log.info("User "+str(request.user.username)+" created payment")
		request.POST = request.POST.copy()
		request.POST["u_id"] = request.user.id
		r = requests.post(BILLING_DOMAIN+"/billing/", data=request.POST)
		r = requests.post(USER_DOMAIN+"/users/alter_group/", data=request.POST)
		log.info("User "+str(request.user.username)+" group was changed")
		return HttpResponse("Pay please")

@login_required
def creative_tasks(request):
	if (request.method == "GET"):
		log.info("User "+str(request.user.username)+" visited creative task payment page")
		context = {'q': []}
		return render(request, 'gatewayapp/creative_task.html', context)
	else:
		request.POST = request.POST.copy()
		request.POST["user"] = request.user.id
		r = requests.post(CREATIVE_TASKS_DOMAIN+"/creative/add/", data=request.POST)
		log.info("User "+str(request.user.username)+" added creative task to creative service")
		request.POST["task"] = r.content
		r = requests.post(STATS_DOMAIN+"/stats/save_creative/", data=request.POST)
		log.info("User "+str(request.user.username)+" confirmed creative task")
		return HttpResponse("Writing from user" + str(request.POST["user"])+" added")