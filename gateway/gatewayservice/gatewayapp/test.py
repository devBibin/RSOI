from django.test import TestCase
import json
from django.core.urlresolvers import reverse
import requests_mock

'''
@login_required
def get_questions_by_test(request, test_id):
	log.info("User "+str(request.user.username)+" got list of questions in test" + str(test_id))
	rt = requests.get(TEST_DOMAIN+request.get_full_path()).json()
	
	q_ids = []
	for q in rt["questions"]:
		q_ids.append(q["id"])
	q_ids = {"question": q_ids}
	
	rs = requests.get(STATS_DOMAIN + "/stats/get_stats/user/"+str(request.user.id)+"/", params = q_ids).json()
	questions = rt["questions"]
	replied = rs["replied"]
	for i in range(len(questions)):
		if (questions[i]["id"] in replied):
			questions[i]["replied"] = "+"
		else:
			questions[i]["replied"] = "-"
	rt["questions"] = questions
	context = {'d': rt}
	return render(request, 'gatewayapp/question_list.html', context)

@login_required
def get_question_by_id(request, test_id, question_id):
	log.info("User "+str(request.user.username)+" got questions"+str(question_id) +" in test" + str(test_id))
	if (request.method == "GET"):
		r = requests.get(TEST_DOMAIN+request.get_full_path())
		context = {'q': r.json()}
		return render(request, 'gatewayapp/question.html', context)
	else:
		request.POST = request.POST.copy()
		request.POST["question"] = question_id
		request.POST["test"] = test_id
		request.POST["user"] = request.user.id
	 	if (request.POST["choice"] == requests.get(TEST_DOMAIN + "/tests/"+test_id+"/questions/"+str(question_id)+"/answer").content):
	 		request.POST["is_true"] = True
	 	else:
	 		request.POST["is_true"] = False
		r = requests.post(STATS_DOMAIN + "/stats/save_answer/", data = request.POST)
		return HttpResponse("Your answer is" + str(request.POST["is_true"]))



@login_required
def billing_user(request):
	if (request.method == "GET"):
		log.info("User "+str(request.user.username)+" visited payment page")
		context = {'q': []}
		return render(request, 'gatewayapp/billing.html', context)
	else:
		log.info("User "+str(request.user.username)+" created payment")
		request.POST = request.POST.copy()
		request.POST["u_id"] = request.user.id
		r = requests.post(BILLING_DOMAIN+"/billing/", data=request.POST)
		r = requests.post(USER_DOMAIN+"/users/alter_group/", data=request.POST)
		return HttpResponse("Pay please")

@login_required
def creative_tasks(request):
	if (request.method == "GET"):
		context = {'q': []}
		return render(request, 'gatewayapp/creative_task.html', context)
	else:
		request.POST = request.POST.copy()
		request.POST["user"] = request.user.id
		r = requests.post(CREATIVE_TASKS_DOMAIN+"/creative/add/", data=request.POST)
		request.POST["task"] = r.content
		r = requests.post(STATS_DOMAIN+"/stats/save_creative/", data=request.POST)
		return HttpResponse("Writing from user" + str(request.POST["user"])+" added")


    url(r'^tests/(?P<test_id>[0-9]+)/questions/(?P<question_id>[0-9]+)$', gv.get_question_by_id),
    url(r'^tests/(?P<test_id>[0-9]+)/questions$', gv.get_questions_by_test),
    url(r'^tests/(?P<test_id>[0-9]+)/$', gv.get_test_by_id),
    url(r'^users/billing/$', gv.billing_user),
    url(r'^creative/$', gv.creative_tasks)
'''
'''
class ViewTest(TestCase):
	def test_views_get_tests(self):
		response = self.client.get("/tests/")
		self.assertEqual(response.response_code, 200)

	def test_views_get_test_by_id(self):
		response = self.client.get("/tests/1/")
		self.assertEqual(response.body, "404")
'''