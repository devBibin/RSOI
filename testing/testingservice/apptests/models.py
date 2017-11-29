# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models

class TestAuthor(models.Model):
    author_name = models.CharField(max_length=20)
    author_mail = models.EmailField(max_length=100)

    def __unicode__(self):
        return self.author_name

class TestType(models.Model):
    test_type_name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.test_type_name

class TestLanguage(models.Model):
    test_language_name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.test_language_name

class LanguageSection(models.Model):
    language_section_name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.language_section_name

class Test(models.Model):
    test_theme = models.CharField(max_length=500)
    test_introduction = models.CharField(max_length=5000)
    test_time_length = models.DurationField()
    test_to_author = models.ForeignKey(TestAuthor, on_delete=models.PROTECT)
    test_to_type = models.ForeignKey(TestType, on_delete=models.PROTECT)
    test_to_lang = models.ForeignKey(TestLanguage, on_delete=models.PROTECT)
    test_to_lang_section = models.ForeignKey(LanguageSection, null=True, 
        on_delete=models.PROTECT, default = None)

class QuestionBody(models.Model):
    question_text = models.CharField(max_length=1000)
    question_rating = models.PositiveSmallIntegerField(default = 1)
    question_to_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_to_lang_section = models.ForeignKey(LanguageSection, on_delete=models.PROTECT)
    question_annotation = models.CharField(max_length=1000, default="")

class QuestionIssues(models.Model):
    issue_text = models.CharField(max_length=1000)
    issue_author = models.CharField(max_length=1000)
    issue_to_question = models.ForeignKey(QuestionBody, on_delete = models.CASCADE)

    def __unicode__(self):
        return self.issue_text

class SimpleChoice(models.Model):
    choice_text = models.CharField(max_length=100)
    choice_right = models.BooleanField()
    choice_to_question = models.ForeignKey(QuestionBody, on_delete = models.CASCADE)
    


class TableTask(models.Model):
    task_text = models.CharField(max_length=100)
    task_to_question = models.ForeignKey(QuestionBody, on_delete = models.CASCADE)
    
    def __unicode__(self):
        return self.task_to_question.question_text

class TableChoice(models.Model):
    choice_text = models.CharField(max_length=100)
    choice_right = models.BooleanField()
    choice_to_task = models.ForeignKey(TableTask, on_delete = models.CASCADE)
    
    def __unicode__(self):
        return self.choice_text