# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 13:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_annotation', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_type_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LanguageSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_section_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=1000)),
                ('question_rating', models.PositiveSmallIntegerField(default=1)),
                ('question_answer_count', models.PositiveIntegerField(default=0, editable=False)),
                ('question_right_answer_count', models.PositiveIntegerField(default=0, editable=False)),
                ('question_to_answer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apptests.AnswerBody')),
                ('question_to_lang_section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apptests.LanguageSection')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionIssues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_text', models.CharField(max_length=1000)),
                ('issue_author', models.CharField(max_length=1000)),
                ('issue_to_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apptests.QuestionBody')),
            ],
        ),
        migrations.CreateModel(
            name='SimpleChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=100)),
                ('choice_right', models.BooleanField()),
                ('choice_to_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apptests.AnswerBody')),
            ],
        ),
        migrations.CreateModel(
            name='TableChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=100)),
                ('choice_right', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TableTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_text', models.CharField(max_length=100)),
                ('task_to_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apptests.AnswerBody')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_theme', models.CharField(max_length=500)),
                ('test_introduction', models.CharField(max_length=5000)),
                ('test_time_length', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='TestAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=20)),
                ('author_mail', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TestLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_language_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='test_to_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apptests.TestAuthor'),
        ),
        migrations.AddField(
            model_name='test',
            name='test_to_lang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apptests.TestLanguage'),
        ),
        migrations.AddField(
            model_name='test',
            name='test_to_lang_section',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='apptests.LanguageSection'),
        ),
        migrations.AddField(
            model_name='test',
            name='test_to_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apptests.TestType'),
        ),
        migrations.AddField(
            model_name='tablechoice',
            name='choice_to_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apptests.TableTask'),
        ),
        migrations.AddField(
            model_name='questionbody',
            name='question_to_test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apptests.Test'),
        ),
        migrations.AddField(
            model_name='answerbody',
            name='answer_to_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='apptests.AnswerType'),
        ),
    ]
