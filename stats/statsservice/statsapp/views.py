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

@csrf_exempt
def save_answer_info(request):
	a = TestAnswer()
	a.test_id = request.POST["test"]
	a.question_id = request.POST["question"]
	a.choice_id = request.POST["choice"]
	a.user_id = request.POST["user_id"]
	a.is_true = request.POST["is_true"]
	a.save()
	return HttpResponse(requests.codes["ok"])

def get_stats_by_questions(request, user_id):
	q_list_ind = request.GET.getlist("question")
	stat = TestAnswer.objects.filter(question_id__in = q_list_ind)
	
	r = {}
	r["replied"] = []
	for s in stat:
		r["replied"].append(s.question_id)
	r["replied"] = list(set(r["replied"]))
	return JsonResponse(r)

@csrf_exempt
def save_creative_task_info(request):
	ct = CreativeTaskAnswer()
	ct.task_id = request.POST["task"]
	ct.user_id = request.POST["user_id"]
	ct.save()
	return HttpResponse(requests.codes["ok"])