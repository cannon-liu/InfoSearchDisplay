"""new_elasticsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.views.static import serve
from InfoSearch.settings import MEDIA_ROOT
from apps.news.views import SearchSuggest

urlpatterns = [
    path('admin/', admin.site.urls),
    #首页
    path(r'', TemplateView.as_view(template_name='index.html'), name='index'),
    #建议
    path(r'suggest/<suggest_info>', TemplateView.as_view(template_name='result.html'), name="suggest"),
    # 读取上传图片
    # path(r'media/<path>', serve, {"document_root": MEDIA_ROOT}),
    path(r'media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # path('static/<path>', serve, {'document_root': STATIC_ROOT}),
    # path('static/<path:path>', serve, {'document_root': STATIC_ROOT}),
    # 新闻信息配置
    path(r'news/', include(('apps.news.urls', 'news'), namespace='news')),
]
