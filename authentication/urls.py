
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('favcategories', views.favcategories, name="favcategories"),
    path('enroll_fav_category', views.enroll_fav_category, name='enroll_fav_category'),
    path('delete_fav_category', views.delete_fav_category, name='delete_fav_category'),
]