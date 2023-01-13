
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('userprofile', views.userprofile, name='userprofile'),
    path('mycourses', views.mycourses, name='mycourses'),
    path('mycourse_detail', views.mycourse_detail, name='mycourse_detail'),
    path('addunit', views.addunit, name='addunit'),
    path('administrator', views.administrator, name='administrator'),
    path('course_admin_delete', views.course_admin_delete, name='course_admin_delete'),
    path('category_admin_delete', views.category_admin_delete, name='category_admin_delete'),
    path('user_admin_delete', views.user_admin_delete, name='user_admin_delete'),
    path('grant_admin', views.grant_admin, name='grant_admin'),
    path('take_admin', views.take_admin, name='take_admin'),
    path('addmaterial', views.addmaterial, name='addmaterial'),
    path('textfile/<str:file_path>', views.view_text_file, name='textfile'),
    path('otherprofile', views.otherprofile, name='otherprofile'),
    path('editcourse', views.editcourse, name='editcourse'),
    path('saveedited', views.saveedited, name='saveedited'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)