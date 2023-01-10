from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth import get_user_model
from authentication.models import User, Category, FavCategories, UserProfile, Course, CourseEnrolled, TeachingUnit,TUMaterials, CourseGrade, UserPayment, CourseOwner
from django.core import serializers
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def home(request):

    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        # check if username exists in the database
        username1 = request.POST.get('username')
        username_exists_in_database = User.objects.filter(username=username1).exists()
        email1 = request.POST.get('email')
        email_exists_in_database = User.objects.filter(email=email1).exists()
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1==pass2:
            passwords_match = False
        else:
            passwords_match = True
            
        
        if (username_exists_in_database or email_exists_in_database or passwords_match):
            context = {
                 'username_exists': username_exists_in_database,
                 'email_exists': email_exists_in_database,
                 'passwords_matching': passwords_match,
                }
            return render(request, 'authentication/signup.html', context)

        else:
            name1 = request.POST.get('name1')
            name2 = request.POST.get('name2')
            gender1 = request.POST.get('gender')
            newuser = User()
            newuser.username = username1
            newuser.name = name1
            newuser.surname = name2
            newuser.set_password(pass1)
            newuser.gender = gender1
            newuser.email = email1
            newuser.save()
            return redirect("signin")
    else:
        return render(request, "authentication/signup.html")


def signin(request):
    logout(request)
    
    if request.method == "POST":
        username = request.POST['username'] 
        password = request.POST['pass1']  
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    #print("TRYING")
                    user_data_extra = UserProfile.objects.get(user_id=request.user.user_id)
                    request.session['user_data_extra'] = {
                    'description': user_data_extra.description,
                    'picture': user_data_extra.picture.url
                    }
                except:
                    try:
                        user_data_extra = UserProfile.objects.get(user_id=request.user.user_id)
                        request.session['user_data_extra'] = {
                            'description': user_data_extra.description,
                            'picture': None
                        }
                    except:
                        request.session['user_data_extra'] = {
                        'description': " ",
                        'picture': None 
                        }

                return render(request, "authentication/index.html")
            else:
                return render(request,"authentication/signin.html", {'bad_login':True})
        except User.DoesNotExist:  # User does not exist
            return render(request,"authentication/signin.html", {'bad_login':True})
    else:
        return render(request,"authentication/signin.html")
    
    
    
def signout(request):
    logout(request)
    request.session.clear()
    return redirect('home')

def favcategories(request):
    # code for getting the favorite categories
    enrolled_categories = FavCategories.objects.filter(user_id=request.user.user_id).values_list('id_category', flat=True)
    return render(request, 'authentication/favcategories.html',{'all_categories':Category.objects.all(),
                                                                'enrolled_categories': enrolled_categories
                                                                })
    
def enroll_fav_category(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        category_id = request.POST['id_category']
        #print(category_id)
        user = User.objects.get(user_id=user_id)
        category = Category.objects.get(id_category=category_id)
        
        new_fav = FavCategories()
        new_fav.user_id = user
        new_fav.id_category = category
        new_fav.save()
        return redirect('favcategories')
    else:
        return redirect('home')
    
def delete_fav_category(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        id_category = request.POST.get('id_category')
        obj = FavCategories.objects.get(user_id=user_id, id_category=id_category)
        obj.delete()
        from_profile = request.POST.get('from_profile')
        if from_profile:
            return redirect('userprofile')
        else:
            return redirect('favcategories')



def user_profile_save(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(user_id=user_id)
        userprofile, created = UserProfile.objects.get_or_create(user_id=user)
        try:
            userprofile.picture = request.FILES.get('picture')
        except MultiValueDictKeyError:
            if created:
                userprofile.picture = None
            else:
                userprofile.picture = userprofile.picture or None
        userprofile.description = request.POST.get('description')
        userprofile.save()
        request.session['user_data_extra'] = {
                 'description': userprofile.description,
                  'picture': userprofile.picture.url if userprofile.picture else None
                    }
        return redirect('userprofile')
    else:
        return redirect('userprofile')
    
    
def course(request):
    all_courses = Course.objects.all()
    courses_with_category_names = []
    for course in all_courses:
        category_name = Category.objects.get(pk=course.ID_CATEGORY_id).name
        courses_with_category_names.append({
            'ID_COURSE': course.ID_COURSE,
            'ID_CATEGORY': course.ID_CATEGORY_id,
            'NAME': course.NAME,
            'DESCRIPTION': course.DESCRIPTION,
            'LOGO': course.LOGO,
            'PRICE': course.PRICE,
            'DURATION': course.DURATION,
            'CATEGORY_NAME': category_name
        })
    enrolled_courses = CourseEnrolled.objects.filter(user_id=request.user.user_id).values_list('ID_COURSE', flat=True)
    return render(request, 'authentication/course.html', {'course': courses_with_category_names,
                                                          'enrolled_courses': enrolled_courses})


def addcourse(request):
    if request.method == "POST":
        newcourse = Course()
        newcourse.NAME = request.POST.get('name')
        category_id = request.POST['id_category']
        category = Category.objects.get(id_category=category_id)
        newcourse.ID_CATEGORY = category 
        newcourse.DESCRIPTION = request.POST.get('description')
        newcourse.PRICE = request.POST.get('price')
        newcourse.DURATION = request.POST.get('duration')
        newcourse.save()

        newowner = CourseOwner()
        newowner.ID_COURSE = newcourse
        user_id = request.POST.get('user_id')
        user = User.objects.get(user_id = user_id)
        newowner.user_id = user
        newowner.save()

        return redirect('home')
    else:
        return render(request, 'authentication/addcourse.html', {'categories':Category.objects.all()})

    
def enroll_course(request):
    if request.method == 'POST':
        id_course = request.POST.get('ID_COURSE')
        course = Course.objects.get(ID_COURSE=id_course)
        CourseEnrolled.objects.create(user_id=request.user, ID_COURSE=course)
        return redirect('course')
    else:
        return redirect('home')
    
 
def deroll_course(request):
    if request.method == 'POST':
        id_course = request.POST.get('ID_COURSE')
        obj = CourseEnrolled.objects.get(user_id=request.user, ID_COURSE=id_course)
        obj.delete()
        return redirect('course')
    
def course_details(request):
    if request.method == 'POST':
        id_course = request.POST.get('ID_COURSE')
        spec_course = Course.objects.get(ID_COURSE=id_course)
        category_name = spec_course.ID_CATEGORY.name
        is_enrolled = CourseEnrolled.objects.filter(user_id=request.user, ID_COURSE=id_course).exists()
        course_grades = CourseGrade.objects.filter(ID_COURSE=id_course)
        course_grades = course_grades.select_related('user_id')
        return render(request, 'authentication/detailedcourse.html', {'course': spec_course,'enrolled_courses': is_enrolled, 'category_name': category_name, 'comments':course_grades})
        
def addcategory(request):
    if request.method == "POST":
        Category.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('favcategories')
    else:
        return render(request, 'authentication/addcategory.html')
    
def addcomment(request):
    if request.method == "POST":
        user = User.objects.get(user_id=request.POST.get('user_id'))
        rate, comment = request.POST.get('rate'), request.POST.get('comment')
        course = Course.objects.get(ID_COURSE=request.POST.get('ID_COURSE'))
        CourseGrade.objects.create(
            RATE=rate,
            COMMENT=comment,
            user_id=user,
            ID_COURSE=course
        )
        return redirect('course')

def payment(request):
    return ()

def userprofile(request):
    if request.user.is_authenticated:
        enrolled_categories = FavCategories.objects.filter(user_id=request.user.user_id).prefetch_related('id_category')
        return render(request, 'authentication/userprofile.html', {'enrolled_categories': enrolled_categories})
    else:
        return redirect('home')

def mycourses(request):
    owned = CourseOwner.objects.filter(user_id=request.user).values_list('ID_COURSE', flat=True)
    courses = []
    for course in owned:
        print("-----course")
        print(course)
        courses.append(Course.objects.get(ID_COURSE=course))
    print("------courses")
    print(courses)
    return render(request, 'authentication/mycourses.html', {'courses': courses})

