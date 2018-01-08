# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
import json
import logging
from tasks import *
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy


log = logging.getLogger(__name__)

TEST_DOMAIN = "http://localhost:8081"
USER_DOMAIN = "http://localhost:8082"
BILLING_DOMAIN = "http://localhost:8083"
STATS_DOMAIN = "http://localhost:8084"
CREATIVE_TASKS_DOMAIN = "http://localhost:8085"
RENDER_DOMAIN = "http://localhost:8000"

APPLICATION_AUTH = "b21oWnVNY1JzelN0T1ZuZjk3WUhDUEVzOThEdjNESWJzVzFwTHJyVToxbWhzUkxXQzhHN1hkS2dmdkk3TDQ5RWR6ZVdmbnJqb1F3elQ1QXpCd3RnSXd6RnZjNDQxbDd3aUxFd3B4WUdHdzhXVTRXV1M4aE05QUZuRnlWUzkzM1c4cnJCMTN3eVFydW51NFJhM0l5dllKMWdrMmJaRHNlMjNEdUI3UFJLUA=="

def get_tests(request):
	try:
		r = requests.get(TEST_DOMAIN+request.get_full_path())
		log.info("User "+str(request.user.username)+" got list of tests")
		context = {'data': r.json()}
		if (r.status_code != 200):
			context = r.json()
		return JsonResponse(context, status = r.status_code)
	except Exception as e:
		log.error("Service testing failed")
		context = {'data': "", "message": "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
		return JsonResponse(context, status = 503)

def get_test_by_id(request, test_id):
	try:
		r = requests.get(TEST_DOMAIN+request.get_full_path()).json()
		log.info("User "+str(request.user.username)+" got test " + str(test_id))
		r["test_id"] = test_id
		context = {'data': r}
		return JsonResponse(context, status = 200)
	except Exception as e:
		log.error("Service testing failed")
		context = {'data': "", "message": "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
		return JsonResponse(context, status = 503)


@login_required
def get_questions_by_test(request, test_id):
	try:
		rt = requests.get(TEST_DOMAIN+request.get_full_path()).json()
		log.info("User "+str(request.user.username)+" got questions")
	except Exception as e:
		context = {"message" : "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
		return JsonResponse(context, status = 503)
	
	q_ids = []
	for q in rt["questions"]:
		q_ids.append(q["id"])
	q_ids = {"question": q_ids}
	
	try:
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
	except Exception as e:
		log.error("Degradation of functionality because of failing stats service")
	
	context = {'data': rt}
	return JsonResponse(context, status = 200)

@csrf_exempt
@login_required 
def get_question_by_id(request, test_id, question_id):
	log.info("User "+str(request.user.username)+" got questions"+str(question_id) +" in test" + str(test_id))
	if (request.method == "GET"):
		try:
			r = requests.get(TEST_DOMAIN+request.get_full_path())
		except Exception as e:
			context = {"message" : "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
			return JsonResponse(context, status = 503)
		d = r.json()
		d["is_true"] = ""
		context = {'data': d}
		return JsonResponse(context, status = 200)
	else:
		request.POST = request.POST.copy()
		request.POST["question"] = question_id
		request.POST["test"] = test_id
		request.POST["user"] = request.user.id
	 	if (request.POST.get("choice") == requests.get(TEST_DOMAIN + "/tests/"+test_id+"/questions/"+str(question_id)+"/answer").content):
	 		request.POST["is_true"] = True
	 	else:
	 		request.POST["is_true"] = False

	 	try:
			r = requests.post(STATS_DOMAIN + "/stats/save_answer/", data = request.POST)
			r = requests.get(TEST_DOMAIN+request.get_full_path())
			d = r.json()
			d["is_true"] = request.POST["is_true"]
			context = {'data': d}
			return JsonResponse(context, status = 200)
		except Exception as e:
			context = {"message" : "К сожалению сервис статистики не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
			return JsonResponse(context, status = 503)

@csrf_exempt
@login_required 
def billing_user(request):
	if (request.method == "GET"):
		log.info("User "+str(request.user.username)+" visited payment page")
		context = {'data': []}
		return JsonResponse(context, status = 200)
	if (request.method == "POST"):
		log.info("User "+str(request.user.username)+" created payment")
		request.POST = request.POST.copy()
		request.POST["u_id"] = request.user.id 
		
		try:
			r = requests.post(BILLING_DOMAIN+"/billing/", data=request.POST)
		except Exception as e:
			log.error("Billing domain failed")
			context = {"message" : "К сожалению сервис платежи не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
			return JsonResponse(context, status = 503)
		
		try:
			r = requests.post(USER_DOMAIN+"/users/alter_group/", data=request.POST)
		except Exception as e:
			log.error("User domain failed")
			r = requests.delete(BILLING_DOMAIN+"/billing/", params =request.POST)
			log.error("Cancel payment operation")
			context = {"message" : "К сожалению сервис пользователи не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
			return JsonResponse(context, status = 503)

		log.info("User's "+str(request.user.username)+" group was changed")
		context = {"message" : "Пожалуйста оплатите счет для получения расширенных прав доступа"}
		return JsonResponse(context, status = 202)

@csrf_exempt
@login_required 
def creative_tasks(request):
	log.info("User "+str(request.user.username)+" went to creative task")
	if (request.method == "GET"):
		log.info("User "+str(request.user.username)+" visited creative task page")
		context = {'data': []}
		return JsonResponse(context, status = 200)
	else:
		request.POST = request.POST.copy()
		request.POST["user"] = 2
		try:
			r = requests.post(CREATIVE_TASKS_DOMAIN+"/creative/add/", data=request.POST)
			request.POST["task"] = r.content
			log.info("User "+str(request.user.username)+" added creative task to creative service")
		except Exception as e:
			IssueTask.delay("http://localhost:8000/creative/", "POST", request.POST)
			log.error("Creative tasks domain failed. Queing request!")
			context = {"message" : "Спасибо! Ваша работа будет проверена в кратчайшие сроки."}
			return JsonResponse(context, status = 202)

		try:
			r = requests.post(STATS_DOMAIN+"/stats/save_creative/", data=request.POST)
		except Exception as e:
			IssueTask.delay("http://localhost:8000/creative/", "POST", request.POST)
			log.error("Stats domain failed. Queing request!")
		
		log.info("User "+str(request.user.username)+" confirmed creative task")
		context = {"message" : "Спасибо! Ваша работа будет проверена в кратчайшие сроки."}
		return JsonResponse(context, status = 202)


def redirect_auth(request):
	log.info("Try to redirect to user service")
	return HttpResponseRedirect(
		'http://localhost:8082/o/authorize/?response_type=code&client_id=omhZuMcRszStOVnf97YHCPEs98Dv3DIbsW1pLrrU&state=random_state_string')

def auth(request):
    log.info("Try to get tokens")
    header = {
        'Authorization': 'Basic ' + APPLICATION_AUTH}
    data = {'code': request.GET['code'], 'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:8001/users/auth2/'}
    target = 'http://localhost:8082/o/token/'
    resp = requests.post(target, data=data, headers=header)
    if resp.status_code == 200:
        content = json.loads(resp.content)
        print content
        r2 = HttpResponseRedirect(
            RENDER_DOMAIN + '/users/auth_succsess/?token=' + content['access_token'] + '&refresh=' + content['refresh_token'])
        return r2
    return resp

def reauth(request):
    log.info("Reauth user")
    header = {
        'Authorization': 'Basic ' + APP_AUTH}
    data = {'refresh_token': str(request.POST.get('code')), 'grant_type': 'refresh_token'}
    target = 'http://127.0.0.1:8005/o/token/'
    resp = requests.post(target, data=data, headers=header)
    if resp.status_code == 200:
        content = json.loads(resp.content)
        ret_data = {'token': content['access_token'], 'refresh': content['refresh_token']}
        return HttpResponse(status=200, content=json.dumps(ret_data))
    return resp

def has_access(request):
    header = {'Authorization': str(request.META.get('HTTP_AUTHORIZATION'))}
    resp = requests.get(USER_DOMAIN + '/users/check_rights/', headers=header)
    if resp.status_code == 200:
        return True
    else:
        return False


def has_admin_access(request):
    header = {'Authorization': str(request.META.get('HTTP_AUTHORIZATION'))}
    resp = requests.get(USER_DOMAIN + '/users/check_admin_rights/', headers=header)
    if resp.status_code == 200:
        return True
    else:
        return False


def is_auth(request):
    if has_access(request):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)