"""Examination URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from StudentExamination import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 考试系统
    path("register/", views.register),  # 注册页面
    path("index/", views.index),  # 考试页面
    path("api/gtimg/", views.gtimg),  # 验证码获取
    path("login/", views.login),  # 登录页面
    path("index/exit/", views.exit),  # 注销登录
    path("achievement/", views.achievement),  # 查询成绩
    path("TeacherIndex/", views.teacher_index),  # 教师管理主页面
    path("api/test/", views.main_register),  # 注册接口
    path("api/testlogin/", views.main_login),  # 登录接口
    path("api/getmain/", views.main_index),  # 获取商品详情
    path("api/getxx/", views.get_Logistic),  # 获取推送
    path("api/addkd/", views.add_Logistic),  # 添加快递
    path("api/addmain/",views.add_index),#添加商品详情
]
