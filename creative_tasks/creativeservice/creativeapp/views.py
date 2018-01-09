# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from models import *
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
from rest_framework_expiring_authtoken.authentication import (ExpiringTokenAuthentication,)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

@csrf_exempt 
@api_view(['POST'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_creative_task(request):
	ct = CreativeTask()
	ct.user_id = request.POST["user_id"]
	ct.answer = request.POST["creative_task"]

	ct.save()
	return HttpResponse(ct.pk)