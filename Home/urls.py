"""Codenvy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from Home import views

urlpatterns = [
    path("",views.start, name="start"),
    path("signin",views.signin,name="signin"),
    path("home/",views.start, name="home"),
    path("home/<str:user_name>",views.home, name="home_user"),
    path("signup",views.signup,name="signup"),
    path("leaderboard/",views.leaderboard, name="leaderboard"),
    path("problems/", views.problems, name="problems"),  # Add this line for /problems/ endpoint
    path("problems/<str:user_name>/", views.problems, name="problems_user"),  # Update this line as per your requirement
    path("problem_search/<str:user_name>",views.problem_search,name="search_problem"),
    path("problems/<str:user_name>/type/<str:type>",views.problems_typeSpecific,name="type_specific_problems"),
    path("problems/<str:user_name>/difficuilty/<str:difficuilty>",views.problems_difficuiltySpecific,name="difficuilty_specific_problems"),
   path("problem_desc/<str:user_name>/<int:id>", views.problem_description, name="problem_description"),

    path("submit_code/<str:user_name>/<int:id>",views.submit,name="problem_description"),
    path("submissions/<str:user_name>",views.submissions,name="my_submissions"),
]
