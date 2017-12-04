from django.test import TestCase
import json
from django.core.urlresolvers import reverse
from models import *


class ViewTest(TestCase):
	def setUp(self):
		TestAuthor.objects.create(author_name="Valentin",author_mail="mail")
		TestLanguage.objects.create(test_language_name ="English")
		TestType.objects.create(test_type_name="short")
		LanguageSection.objects.create(language_section_name="grammar")

		a = TestAuthor.objects.all()[0]
		l = TestLanguage.objects.all()[0]
		t = TestType.objects.all()[0]
		s = LanguageSection.objects.all()[0] 

		for i in range(10):
			Test.objects.create(test_theme = str(i)+"Theme", test_introduction = str(i)+"Intro",
			test_time_length="00:00:01",test_to_author=a,test_to_lang=l,test_to_type=t,test_to_lang_section=s)

		test = Test.objects.all()[0]
		for i in range(10):
			QuestionBody.objects.create(question_text=str(i)+"text",question_annotation=str(i)+"annotation",
				question_rating=3,question_to_test=test,question_to_lang_section=s)
		question = QuestionBody.objects.all()[0]
		for i in range(4):
			if (i == 0):
				SimpleChoice.objects.create(choice_text=str(i)+"choice",choice_right=True,choice_to_question=question)
			else:
				SimpleChoice.objects.create(choice_text=str(i)+"choice",choice_right=False,choice_to_question=question)

	def test_view_get_correct_answer(self):
		response = self.client.get("/tests/1/questions/1/answer/")
		data = int(response.content)
		self.assertEqual(data,1)

	def test_view_tests_simple(self):
		response = self.client.get("/tests/")
		json_data = json.loads(response.content)
		self.assertEqual(len(json_data["data"]),10)

	def test_view_tests_page(self):
		response = self.client.get("/tests/?page=3&size=1")
		json_data = json.loads(response.content)
		self.assertEqual(json_data["data"][0]["theme"],"2Theme")

	def test_view_tests_size(self):
		response = self.client.get("/tests/?page=1&size=5")
		json_data = json.loads(response.content)
		self.assertEqual(len(json_data["data"]),5)
		self.assertEqual(json_data["data"][4]["theme"],"4Theme")

	def test_view_tests_wild(self):
		response = self.client.get("/tests/?page=111&size=111")
		json_data = json.loads(response.content)
		self.assertEqual(len(json_data["data"]),10)
		self.assertEqual(json_data["data"][9]["theme"],"9Theme")

	def test_view_get_tests_by_id(self):
		response = self.client.get("/tests/31/")
		json_data = json.loads(response.content)
		self.assertEqual(json_data["theme"],"0Theme")

	def test_view_get_questions_by_test(self):
		response = self.client.get("/tests/21/questions/")
		json_data = json.loads(response.content)
		self.assertEqual(len(json_data["questions"]),10)

	def test_view_get_question_by_id(self):	
		response = self.client.get("/tests/11/questions/11/")
		json_data = json.loads(response.content)
		self.assertEqual(json_data["question_text"],"0text")
		self.assertEqual(len(json_data["simple_choices"]),4)
