# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from models import *
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse

@csrf_exempt
def save_creative_task(request):
	ct = CreativeTask()
	ct.user_id = request.POST["user_id"]
	ct.answer = request.POST["creative_task"]

	ct.save()
	return HttpResponse(ct.pk)