# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

admin.site.register(Test)
admin.site.register(QuestionBody)
admin.site.register(SimpleChoice)
admin.site.register(TableTask)
admin.site.register(TableChoice)
# Register your models here.