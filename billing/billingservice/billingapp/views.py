from __future__ import unicode_literals

from django.http import JsonResponse
from models import *
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse

@csrf_exempt 
def create_bill(request):
	if (request.method == "GET"):
		context = {'q': []}
		return HttpResponse(requests.codes["method_not_allowed"])
	else:
		b = Billing()
		b.user_id = request.POST["u_id"]
		b.payment_for_type = request.POST["type"]
		b.transaction_amount = request.POST["amount"]
		b.transaction_date = datetime.datetime.now()

		b.save()
		return HttpResponse(requests.codes["ok"])