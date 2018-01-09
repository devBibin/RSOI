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
@api_view(['GET', 'POST'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_bill(request):
	if (request.method == "GET"):
		context = {'q': []}
		return HttpResponse(requests.codes["method_not_allowed"])
	elif (request.method == "POST"):
		b = Billing()
		b.user_id = request.POST["user_id"]
		b.payment_for_type = request.POST["type"]
		b.transaction_amount = request.POST["amount"]
		b.transaction_date = datetime.datetime.now()

		b.save()
		return HttpResponse(requests.codes["ok"])
	elif (request.method == "DELETE"):
		b = Billing.objects.filter(user_id = request.GET["user_id"])
		b = b[len(b)-1]
		b.delete()
		return HttpResponse(requests.codes["ok"])