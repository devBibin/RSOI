import requests
import logging

from celery.decorators import task
from celery.registry import tasks
from celery.task import Task


@task
def create_issue(url, method, urlData):
	try:
		if (method == "POST"):
			requests.post(url, data=urlData)
		else:
			requests.get(url, data=urlData)
	except:
		return