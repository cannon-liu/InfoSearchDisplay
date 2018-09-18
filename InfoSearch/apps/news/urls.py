# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/17 11:55'

from django.urls import path
from django.views.generic import TemplateView

app_name = 'news'

urlpatterns = {
    path(r'', TemplateView.as_view(template_name='result.html'), name='news')


}
