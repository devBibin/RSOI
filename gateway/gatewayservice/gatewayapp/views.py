# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
import json
import logging
from tasks import *
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
import gatewayapp.writer
from gatewayapp.writer import get_request_log


log = logging.getLogger(__name__)
log.propagate = False

GATEWAY_DOMAIN = "http://localhost:8001"
TEST_DOMAIN = "http://localhost:8081"
USER_DOMAIN = "http://localhost:8082"
BILLING_DOMAIN = "http://localhost:8083"
STATS_DOMAIN = "http://localhost:8084"
CREATIVE_TASKS_DOMAIN = "http://localhost:8085"
RENDER_DOMAIN = "http://localhost:8000"

APPLICATION_AUTH = "b21oWnVNY1JzelN0T1ZuZjk3WUhDUEVzOThEdjNESWJzVzFwTHJyVToxbWhzUkxXQzhHN1hkS2dmdkk3TDQ5RWR6ZVdmbnJqb1F3elQ1QXpCd3RnSXd6RnZjNDQxbDd3aUxFd3B4WUdHdzhXVTRXV1M4aE05QUZuRnlWUzkzM1c4cnJCMTN3eVFydW51NFJhM0l5dllKMWdrMmJaRHNlMjNEdUI3UFJLUA=="

service_tokens = {'tests': '',
				  'billings': '',
				  'stats': '',
				  'creative_tasks': '',}
service_locations = {'tests': TEST_DOMAIN, 'billings': BILLING_DOMAIN, 'stats': STATS_DOMAIN, 
'creative_tasks': CREATIVE_TASKS_DOMAIN}


def wrap_request(method, domain, uri, service, data = None):
	if (method == "GET"):
		r = requests.get(domain+uri, headers = create_header(service))
		if (r.status_code == 401):
			log.warning("Service "+service+" token expired")
			login_service(service)
			r = requests.get(domain+uri, headers = create_header(service))
	elif (method == "POST"):
		r = requests.post(domain+uri, data = data, headers = create_header(service))
		if (r.status_code == 401):
			log.warning("Service "+service+" token expired")
			login_service(service)
			r = requests.post(domain+uri, data = data, headers = create_header(service))
	return r

def get_tests(request):
	try:
		errors = {}
		r = wrap_request("GET", TEST_DOMAIN, request.get_full_path(), "tests")
		log.info("User "+str(request.user.username)+" got list of tests")
		context = {'data': r.json()}
		if (r.status_code != 200):
			context = r.json()
			errors = context

		get_request_log(request, r.status_code, errors)
		
		return JsonResponse(context, status = r.status_code)
	except Exception as e:
		log.error("Service testing failed " +str(e) )
		context = {'data': "", "message": "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
		redirect_auth(request)

def get_test_by_id(request, test_id):
	try:
		r = wrap_request("GET", TEST_DOMAIN, request.get_full_path(), "tests")
		log.info("User "+str(request.user.username)+" got test " + str(test_id))
		r = r.json()
		r["test_id"] = test_id
		context = {'data': r}

		get_request_log(request)
		
		return JsonResponse(context, status = 200)
	except Exception as e:
		log.error("Service testing failed")
		context = {'data': "", "message": "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
		return JsonResponse(context, status = 503)


def get_questions_by_test(request, test_id):
	if (has_access(request)):
		user_id = request.GET.get("user_id")
		try:
			rt = wrap_request("GET", TEST_DOMAIN, request.get_full_path(), "tests")
			log.info("User "+str(user_id)+" got questions")
		except Exception as e:
			context = {"message" : "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
			return JsonResponse(context, status = 503)
		
		q_ids = []
		rt = rt.json()
		for q in rt["questions"]:
			q_ids.append(q["id"])
		q_ids = {"question": q_ids}
		
		try:
			rs = requests.get(STATS_DOMAIN + "/stats/get_stats/user/"+str(user_id)+"/", params = q_ids, headers =create_header('stats'))
			if (rs.status_code == 401):
				log.info("Stats service token expired")
				login_service("stats")
				rs = requests.get(STATS_DOMAIN + "/stats/get_stats/user/"+str(user_id)+"/", params = q_ids, headers =create_header('stats')) 

			rs = rs.json()
			questions = rt["questions"]
			replied = rs["replied"]
			for i in range(len(questions)):
				if (questions[i]["id"] in replied):
					questions[i]["replied"] = "+"
				else:
					questions[i]["replied"] = "-"
			rt["questions"] = questions
			log.info("User "+str(user_id)+" got replied questions")
		except Exception as e:
			log.error("Degradation of functionality because of failing stats service " + str(e))
		
		context = {'data': rt}
		get_request_log(request)
		return JsonResponse(context, status = 200)
	else:
		log.warning("Anuthorized request to private API")
		return HttpResponse(status = 403)

@csrf_exempt
def get_question_by_id(request, test_id, question_id):
	if (has_access(request)):
		if (request.method == "GET"):
			user_id = request.GET.get("user_id")
			log.info("User "+str(user_id)+" got questions"+str(question_id) +" in test" + str(test_id))
			try:
				r = wrap_request("GET", TEST_DOMAIN, request.get_full_path(), "tests")
			except Exception as e:
				context = {"message" : "К сожалению сервис тестирование не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
				return JsonResponse(context, status = 503)
			d = r.json()
			d["is_true"] = ""
			context = {'data': d}
			get_request_log(request)
			return JsonResponse(context, status = 200)
		elif (request.method == "POST"):
			request.POST = request.POST.copy()
			request.POST["question"] = question_id
			request.POST["test"] = test_id

			r = wrap_request("GET", TEST_DOMAIN, "/tests/"+test_id+"/questions/"+str(question_id)+"/answer", "tests")
		 	right_answer = r.content
		 	
		 	if (request.POST.get("choice") == right_answer):
		 		log.info("User " + str(request.POST.get("user_id")) + " gave CORRECT answer")
		 		request.POST["is_true"] = True
		 	else:
		 		log.info("User " + str(request.POST.get("user_id")) + " gave WRONG answer")
		 		request.POST["is_true"] = False

		 	try:
		 		log.info("Saving answer")
		 		r = wrap_request("POST", STATS_DOMAIN, "/stats/save_answer/", "stats", request.POST)
				log.info("Answer saved")
				
				r = wrap_request("GET", TEST_DOMAIN, request.get_full_path(), "tests")

				d = r.json()
				d["is_true"] = request.POST["is_true"]
				context = {'data': d}
				
				get_request_log(request)
				return JsonResponse(context, status = 200)
			except Exception as e:
				log.error("Service stats FAILED")
				context = {"message" : "К сожалению сервис статистики не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
				return JsonResponse(context, status = 503)
	else:
		return HttpResponse(status = 403)

@csrf_exempt
def billing_user(request):
	if (has_access(request)):
		if (request.method == "GET"):
			user_id = request.GET.get("user_id")
			log.info("User "+str(user_id)+" visited payment page")
			context = {'data': []}
			get_request_log(request)
			return JsonResponse(context, status = 200)
		elif (request.method == "POST"):
			try:
				log.info("User "+str(request.POST.get("user_id"))+" creating payment")
				r = wrap_request("POST", BILLING_DOMAIN, "/billing/", "billings", request.POST)
			except Exception as e:
				log.error("Billing domain failed " + str(e))
				context = {"message" : "К сожалению сервис платежи не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
				return JsonResponse(context, status = 503)
			
			try:
				r = requests.post(USER_DOMAIN+"/users/alter_group/", data=request.POST)
			except Exception as e:
				log.error("User domain failed" + str(e))
				r = requests.delete(BILLING_DOMAIN+"/billing/", params =request.POST)
				log.error("Cancel payment operation")
				context = {"message" : "К сожалению сервис пользователи не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
				return JsonResponse(context, status = 503)

			log.info("User's "+str(request.user.username)+" group was changed")
			context = {"message" : "Пожалуйста оплатите счет для получения расширенных прав доступа"}
			get_request_log(request)
			return JsonResponse(context, status = 202)
	else:
		return HttpResponse(status = 403)

@csrf_exempt
def creative_tasks(request):
	if (has_access(request)):
		if (request.method == "GET"):
			user_id = request.GET.get("user_id")
			log.info("User "+str(user_id)+" visited creative task page")
			context = {'data': []}
			get_request_log(request)
			return JsonResponse(context, status = 200)
		else:
			request.POST = request.POST.copy()
			try:
				r = requests.post(CREATIVE_TASKS_DOMAIN+"/creative/add/", data=request.POST,headers = create_header("creative_tasks"))
				if (r.status_code == 401):
					log.warning("Service creative token expired")
					login_service("creative_tasks")
					r = requests.post(CREATIVE_TASKS_DOMAIN+"/creative/add/", data=request.POST,headers = create_header("creative_tasks"))
				request.POST["task"] = r.content
				log.info("User "+str(request.POST.get("user_id"))+" added creative task to creative service")
			except Exception as e:
				IssueTask.delay("http://localhost:8000/creative/", "POST", request.POST)
				log.error("Creative tasks domain failed. Queing request!")
				context = {"message" : "Спасибо! Ваша работа будет проверена в кратчайшие сроки."}
				return JsonResponse(context, status = 202)

			try:
				r = requests.post(STATS_DOMAIN+"/stats/save_creative/", data=request.POST, headers = create_header("stats"))
				if (r.status_code == 401):
					log.warning("Service stats token expired")
					login_service("stats")
					r = requests.post(STATS_DOMAIN+"/stats/save_creative/", data=request.POST, headers = create_header("stats"))
			
			except Exception as e:
				IssueTask.delay("http://localhost:8000/creative/", "POST", request.POST)
				log.error("Stats domain failed. Queing request!")
			
			log.info("User "+str(request.user.username)+" confirmed creative task")
			context = {"message" : "Спасибо! Ваша работа будет проверена в кратчайшие сроки."}
			get_request_log(request)
			return JsonResponse(context, status = 202)
	else:
		HttpResponse(status = 403)

def redirect_auth(request):
	log.info("Try to redirect to user service")
	get_request_log(request)
	return HttpResponseRedirect(
		'http://localhost:8082/o/authorize/?response_type=code&client_id=omhZuMcRszStOVnf97YHCPEs98Dv3DIbsW1pLrrU&state=random_state_string')

@csrf_exempt
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
		get_request_log(request)
		r2 = HttpResponseRedirect(
			RENDER_DOMAIN + '/users/auth_succsess/?token=' + content['access_token'] + '&refresh=' + content['refresh_token'])
		return r2
	return resp

@csrf_exempt
def reauth(request):
	d =  request.POST
	log.info("Reauth user with refresh token: " + d["code"])
	header = {
		'Authorization': 'Basic ' + APPLICATION_AUTH}
	data = {'refresh_token': str(d["code"]), 'grant_type': 'refresh_token'}
	target = 'http://localhost:8082/o/token/'
	resp = requests.post(target, data=data, headers=header)
	if resp.status_code == 200:
		content = json.loads(resp.content)
		ret_data = {'token': content['access_token'], 'refresh': content['refresh_token']}
		get_request_log(request)
		return HttpResponse(status=200, content=json.dumps(ret_data))
	get_request_log(request, resp.status_code)
	return resp

@csrf_exempt
def has_access(request):
	log.info("Checking if user has rights with: " + str(request.META.get('HTTP_AUTHORIZATION')))
	header = {'Authorization': str(request.META.get('HTTP_AUTHORIZATION'))}
	resp = requests.get(USER_DOMAIN + '/users/check_rights/', headers=header)
	if resp.status_code == 200:
		return resp.content
	else:
		return False

@csrf_exempt
def has_admin_access(request):
	log.info("Checking if user has admin rights with: " + str(request.META.get('HTTP_AUTHORIZATION')))
	header = {'Authorization': str(request.META.get('HTTP_AUTHORIZATION'))}
	resp = requests.get(USER_DOMAIN + '/users/check_admin_rights/', headers=header)
	if resp.status_code == 200:
		return HttpResponse(status = 200)
	else:
		context = {"message" : "Необходимы права администратора."}
		return JsonResponse(context, status = 403)

@csrf_exempt
def is_auth(request):
	log.info("Checking if user is authenthicated")
	if has_access(request):
		user_id = has_access(request)
		return HttpResponse(user_id, status=200)
	else:
		return HttpResponse(status=401)

def login_service(service):
	log.info("Try to log in to service " + service)
	payload = {'username': 'john', 'password': 'johnpassword'}
	try:
		resp = requests.post(service_locations[service] + '/get_auth_token/', data=payload)
		service_tokens[service] = json.loads(resp.content)['token']
	except Exception as e: 
		log.error("Service "+service+" failed " + str(e))
		context = {'data': "", "message": "К сожалению сервис не доступен. Мы уже спешим и скоро все починим. Приносим свои извинения."}
		return False

def create_header(service):
	log.info("Create authorization header")
	return {'Authorization': 'Token ' + service_tokens[service]}

def get_auth_stats(request):
	resp = wrap_request("GET", STATS_DOMAIN, request.get_full_path(), "stats")
	return JsonResponse(resp.json())

def get_requests_stats(request):
	resp = wrap_request("GET", STATS_DOMAIN, request.get_full_path(), "stats")
	return JsonResponse(resp.json())

def get_requests_distrubution(request):
	resp = wrap_request("GET", STATS_DOMAIN, request.get_full_path(), "stats")
	return JsonResponse(resp.json())
