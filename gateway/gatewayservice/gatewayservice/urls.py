"""gatewayservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from gatewayapp import views as gv
from gatewayapp import urls


include('gatewayapp.urls', namespace="gatewayapp")
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tests/(?P<test_id>[0-9]+)/questions/(?P<question_id>[0-9]+)/$', gv.get_question_by_id),
    url(r'^tests/(?P<test_id>[0-9]+)/questions/$', gv.get_questions_by_test),
    url(r'^tests/(?P<test_id>[0-9]+)/$', gv.get_test_by_id),
    url(r'^tests/$', gv.get_tests),
    url(r'^users/auth/$', gv.redirect_auth),
    url(r'^accounts/login/$', gv.redirect_auth),
    url(r'^users/auth2/$', gv.auth),
    url(r'^users/billing/$', gv.billing_user),
    url(r'^creative/$', gv.creative_tasks),
]
