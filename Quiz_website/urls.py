"""Quiz_website URL Configuration

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
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/",views.index),
    path("reg/",views.reg),
    path("",views.login),
    path("user_home/",views.user_home),
    path("creator_home/",views.creator_home),
    path("admin_home/",views.admin_home),
    path("quiz_creator/",views.quiz_creator),
    path("adm_view_users/",views.adm_view_users),
    path("adm_view_creators/",views.adm_view_creators),
    path("add_question/",views.add_question),
    path("creator_view_quiz/",views.creator_view_quiz),
    path("user_view_quiz/",views.user_view_quiz),
    path("answe_to_question/",views.answe_to_question),
    path("add_question_category/",views.add_question_category),
    path("user_view_quiz_category/",views.user_view_quiz_category),
    path("delete_question/",views.delete_question),
    path("score/",views.score),
    path("view_answers/",views.view_answers),
    path("udp/",views.udp),
    path("delete_creator/",views.delete_creator),
    path("delete_answer/",views.delete_answer),
    path("approve_edu/",views.approve_edu),
    
    
]
