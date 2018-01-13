# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from models import *
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
import urlparse
from rest_framework_expiring_authtoken.authentication import (ExpiringTokenAuthentication,)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import statsapp.writer
from django.db.models import Count
from django.core import serializers
import time


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_answer_info(request):
	a = TestAnswer()
	a.test_id = request.POST["test"]
	a.question_id = request.POST["question"]
	a.choice_id = request.POST["choice"]
	a.user_id = request.POST["user_id"]
	a.is_true = request.POST["is_true"]
	a.save()
	return HttpResponse(requests.codes["ok"])

@api_view(['GET'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_stats_by_questions(request, user_id):
	q_list_ind = request.GET.getlist("question")
	stat = TestAnswer.objects.filter(question_id__in = q_list_ind, user_id = user_id)
	
	r = {}
	r["replied"] = []
	for s in stat:
		r["replied"].append(s.question_id)
	r["replied"] = list(set(r["replied"]))
	return JsonResponse(r)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_creative_task_info(request):
	ct = CreativeTaskAnswer()
	ct.task_id = request.POST["task"]
	ct.user_id = request.POST["user_id"]
	ct.save()
	return HttpResponse(requests.codes["ok"])

@csrf_exempt
@api_view(['GET'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_auth_stats(request):
	content = {}
	content["auth_tries"] = RequestInfo.objects.filter(uri = "/users/auth/").count()
	content["auth_completed"] = RequestInfo.objects.filter(uri__startswith = "/users/auth2/").count()
	return JsonResponse(content)

@csrf_exempt
@api_view(['GET'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_requests_stats(request):
	content = {}
	content["uri_array"] =  list(RequestInfo.objects.all().values('uri').annotate(total=Count('uri')).order_by('total'))
	content["total"] = RequestInfo.objects.count()
	return JsonResponse(content)

def get_requests_distrubution(request):
	content = {}
	cur_time = datetime.datetime.now()
	print "Current time is ", cur_time
	cur_time = cur_time.replace(minute=0, second=0, microsecond=0)
	finish_timestamp = time.mktime(cur_time.timetuple()) + 60*60
	start_timestamp = finish_timestamp - 24*60*60
	
	dist_lst = []
	i = 0
	for t in range(int(start_timestamp), int(finish_timestamp), 60*60):
		dist_lst.append({i : 
			RequestInfo.objects.filter(
			timestamp__range=[str(datetime.datetime.fromtimestamp(t)), str(datetime.datetime.fromtimestamp(t+60*60))]).count()})
		i = i + 1
	content["distribution"] = dist_lst
	content["period"] = str(datetime.datetime.fromtimestamp(start_timestamp + 3*60*60)) +" -- " +str(datetime.datetime.fromtimestamp(finish_timestamp+ 3*60*60))
	return JsonResponse(content)