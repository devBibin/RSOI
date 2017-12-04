# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from models import *
import json
from django.core.paginator import Paginator


def get_tests(request):
	if (not request.GET.get("page")) or (not request.GET.get("size")):
		page = 1
		size = 10
	else:
		page = int(request.GET.get("page"))
		size = int(request.GET.get("size"))

	tests = Test.objects.all()
	p = Paginator(tests, size)
	response_data = {}
	if (page > max(p.page_range)):
		page = max(p.page_range)
	response_data['pages_count'] = p.num_pages
	response_data["data"] = []
	for el in p.page(page).object_list:
		item = {}
		item["theme"] = el.test_theme
		item["id"] = el.pk
		response_data['data'].append(item)
	return JsonResponse(response_data)


def get_test_by_id(request, test_id):
	test = Test.objects.get(id=test_id)
	response_data = {}
	response_data["id"] = test.pk
	response_data["theme"] = test.test_theme
	response_data["intro"] = test.test_introduction
	response_data["author"] = str(test.test_to_author)
	return JsonResponse(response_data)

def get_questions_by_test(request, test_id):
	questions = QuestionBody.objects.filter(question_to_test = test_id)
	response_data = {}
	i = 0
	response_data["id"] = test_id
	response_data["questions"] = []
	for q in questions:
		item = {}
		item["id"] = q.id
		item["question_text"] = q.question_text
		item["question_rating"] = q.question_rating
		item["question_annotation"] = q.question_annotation
		schoices = SimpleChoice.objects.filter(choice_to_question = q.pk)
		item["simple_choices"] = []
		for c in schoices:
			c_item = {}
			c_item["id"] = c.id
			c_item["text"] = c.choice_text
			c_item["is_right"] = c.choice_right
			item["simple_choices"].append(c_item)
		response_data["questions"].append(item)		
	return JsonResponse(response_data)

def get_question_by_id(request, test_id, question_id):
	q = QuestionBody.objects.filter(pk = question_id)[0]
	response_data = {}
	response_data["test_id"] = test_id
	response_data["id"] = q.id
	response_data["question_text"] = q.question_text
	response_data["question_rating"] = q.question_rating
	response_data["question_annotation"] = q.question_annotation
	schoices = SimpleChoice.objects.filter(choice_to_question = q.pk)
	response_data["simple_choices"] = []
	for c in schoices:
		c_item = {}
		c_item["id"] = c.id
		c_item["text"] = c.choice_text
		c_item["is_right"] = c.choice_right
		response_data["simple_choices"].append(c_item)	
	return JsonResponse(response_data)

def get_correct_answer(request, test_id, question_id):
	q = QuestionBody.objects.filter(pk = question_id)[0]
	a = SimpleChoice.objects.filter(choice_to_question = q.pk, choice_right = True)[0].pk
	return HttpResponse(a)

