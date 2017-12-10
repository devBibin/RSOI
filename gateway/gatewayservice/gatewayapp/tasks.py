import requests
import logging

from celery.decorators import task
from celery.registry import tasks
from celery.task import Task

class IssueTask(Task):
	def __init__(self):
		logging.info("My log")

	def run(self, url, method, urlData):
		try:
			if (method == "POST"):
				logging.info(url)
				logging.info("Here to POST!")
				r = requests.post("http://localhost:8000/creative/", data=urlData)
				logging.info(r.status_code)
			else:
				requests.get(url, data=urlData)
		except:
			logging.info("Something gone wrong")

tasks.register(IssueTask)