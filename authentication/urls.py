
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
    path('user_profile_save', views.user_profile_save, name='user_profile_save'),
    path('course', views.course, name="course"),
    path('addcourse', views.addcourse, name="addcourse"),
    path('enroll_course', views.enroll_course, name='enroll_course'),
    path('deroll_course', views.deroll_course, name='deroll_course'),
    path('course_details', views.course_details, name='course_details'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('addcomment', views.addcomment, name='addcomment'),
    path('payment', views.payment, name='payment'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('mycourses', views.mycourses, name='mycourses'),
    path('mycourse_detail', views.mycourse_detail, name='mycourse_detail'),
    path('addunit', views.addunit, name='addunit'),
]