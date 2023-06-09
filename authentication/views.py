from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth import get_user_model
from authentication.models import User, Category, FavCategories, UserProfile, Course, CourseEnrolled, TeachingUnit,TUMaterials, CourseGrade, UserPayment, CourseOwner, TeachingUnit
from authentication.models import User, Category, FavCategories, UserProfile, Course, CourseEnrolled, TeachingUnit,TUMaterials, CourseGrade, UserPayment, CourseOwner, Administrator, OnlineChat
from django.core import serializers
from django.utils.datastructures import MultiValueDictKeyError
from mimetypes import guess_type

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
                    print("TRYING")
                    user_data_extra = UserProfile.objects.get(user_id=request.user.user_id)
                    request.session['description'] = user_data_extra.description
                    request.session['picture'] = user_data_extra.picture.url

                except:
                    print("Failed Trying")
                    try:
                        print("Trying to grab description and setting pic to none")
                        user_data_extra = UserProfile.objects.get(user_id=request.user.user_id)
                        request.session['description'] = user_data_extra.description
                        request.session['picture'] = None
                    except:
                        print("Failed to grab description and setting pic to none")
                        request.session['description'] = " "
                        request.session['picture'] = None
                administrator = Administrator.objects.filter(user_id=request.user.user_id).exists()
                #checking if user is an administrator :)))
                if administrator:
                    request.session['user_data_extra'] = { 'administrator': True }
                else:
                    request.session['user_data_extra'] = { 'administrator': False }
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
        request.session['description'] = userprofile.description
        request.session['picture'] = userprofile.picture.url if userprofile.picture else None
        return redirect('userprofile')
    else:
        return redirect('userprofile')
    
#Function to get courses with category name if category was deleted course category =  Empty Category
def get_courses_with_category_names():
    all_courses = Course.objects.all()
    courses_with_category_names = []
    for course in all_courses:
        category_name = ''
        if course.ID_CATEGORY_id:
            category_name = Category.objects.get(pk=course.ID_CATEGORY_id).name
        else:
            category_name = "Empty Category"
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
    return courses_with_category_names
#Display courses that someone is enrolled into
def course(request):
    courses_with_category_names = get_courses_with_category_names()
    if request.user.is_authenticated:
        enrolled_courses = CourseEnrolled.objects.filter(user_id=request.user.user_id).values_list('ID_COURSE', flat=True)
        return render(request, 'authentication/course.html', {'course': courses_with_category_names,
                                                            'enrolled_courses': enrolled_courses})
    else:
        enrolled_courses = []
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
        try:
            category_name = spec_course.ID_CATEGORY.name
        except:
            category_name = "Category Deleted"
        course_grades = CourseGrade.objects.filter(ID_COURSE=id_course)
        teaching_units = TeachingUnit.objects.filter(ID_COURSE=id_course)
        materials = TUMaterials.objects.filter(ID_TEACHINGUNIT__in=teaching_units.values_list('ID_TEACHINGUNIT', flat=True))
        for material in materials:
            material.file_type, encoding = guess_type(material.MATERIAL.url)
        if request.user.is_authenticated:
            is_enrolled = CourseEnrolled.objects.filter(user_id=request.user, ID_COURSE=id_course).exists()
            course_grades = course_grades.select_related('user_id')
            try:
                online_chat = OnlineChat.objects.get(ID_COURSE=spec_course)

            except:
                online_chat = OnlineChat()
                online_chat.date = None
                online_chat.link = "Not set"
            return render(request, 'authentication/detailedcourse.html', {'course': spec_course,'enrolled_courses': is_enrolled, 'category_name': category_name, 'comments':course_grades,
                                                                    'teaching_units': teaching_units,
                                                                    'materials': materials,
                                                                    'online_chat': online_chat})
        else:
            is_enrolled = False
            return render(request, 'authentication/detailedcourse.html', {'course': spec_course,'enrolled_courses': is_enrolled, 'category_name': category_name, 'comments':course_grades,
                                                                    'teaching_units': teaching_units,
                                                                    'materials': materials})
            
        
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

def userprofile(request):
    if request.user.is_authenticated:
        enrolled_categories = FavCategories.objects.filter(user_id=request.user.user_id).prefetch_related('id_category')
        return render(request, 'authentication/userprofile.html', {'enrolled_categories': enrolled_categories})
    else:
        return redirect('home')

def mycourses(request):
    owned = CourseOwner.objects.filter(user_id=request.user).values_list('ID_COURSE', flat=True)
    online_chat = OnlineChat.objects.all()
    courses = []
    for course in owned:
        courses.append(Course.objects.get(ID_COURSE=course))
    return render(request, 'authentication/mycourses.html', {'courses': courses, 'online_chats': online_chat}) 

def mycourse_detail(request):
    if request.method == 'POST':
        id_course = request.POST.get('ID_COURSE')
        request.session['id_course'] = id_course
    else:
        id_course = request.session.get('id_course')
    spec_course = Course.objects.get(ID_COURSE=id_course)
    try:
        category_name = spec_course.ID_CATEGORY.name
    except:
        category_name = "Category Deleted"
    
    

    course_grades = CourseGrade.objects.filter(ID_COURSE=id_course)
    course_grades = course_grades.select_related('user_id')
    teaching_units = TeachingUnit.objects.filter(ID_COURSE=id_course)
    materials = TUMaterials.objects.filter(ID_TEACHINGUNIT__in=teaching_units.values_list('ID_TEACHINGUNIT', flat=True))
    for material in materials:
        material.file_type, encoding = guess_type(material.MATERIAL.url)
    return render(request, 'authentication/mycourse_detail.html', {'course': spec_course,
                                                                    'category_name': category_name,
                                                                    'comments': course_grades,
                                                                    'teaching_units': teaching_units,
                                                                    'materials': materials})


def addunit(request):
    if request.method == 'POST':
        id_course = request.session.get('id_course')
        #id_course = request.POST.get('ID_COURSE')
        newunit = TeachingUnit()
        course = Course.objects.get(ID_COURSE=id_course)
        newunit.ID_COURSE = course
        name = request.POST.get('name')
        desc = request.POST.get('description')
        request.session['id_course'] = id_course
        if name and desc:
            newunit.NAME = name
            newunit.DESCRIPTION = desc
            newunit.save()
            return redirect('mycourse_detail')
    return render(request, 'authentication/addunit.html', {'id_course': id_course})

def administrator(request):
    if request.session['user_data_extra'] != { 'administrator': True }:
        return redirect('home')
    else:
        courses_with_category_names = get_courses_with_category_names()
        administrators =  Administrator.objects.all().values_list('user_id',flat=True)
        return render( request, 'authentication/administrator.html', {'course': courses_with_category_names,'all_categories':Category.objects.all(), 'all_users': User.objects.all(), 'admins' : administrators})

def course_admin_delete(request):
    if request.method == "POST":
        id_course = request.POST.get('ID_COURSE')
        obj = Course.objects.get(ID_COURSE=id_course)
        obj.delete()
        return redirect('administrator')
    
def category_admin_delete(request):
    if request.method == "POST":
        id_category = request.POST.get('id_category')
        obj = Category.objects.get(id_category=id_category)
        obj.delete()
        return redirect('administrator')
    
def user_admin_delete(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        obj = User.objects.get(user_id=user_id)
        obj.delete()
        return redirect('administrator')

def grant_admin(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        obj = Administrator()
        obj.user_id_id = user_id
        obj.save()
        return redirect('administrator')

def take_admin(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        obj = Administrator.objects.get(user_id=user_id)
        obj.delete()
        return redirect('administrator')

def addmaterial(request):
    if request.method == "POST":
        id_unit = request.POST.get('id_unit')
        if id_unit:
            request.session['id_unit'] = id_unit
        else:
            id_unit = request.session.get('id_unit')

        newmaterial = TUMaterials()
        newmaterial.ID_TEACHINGUNIT = TeachingUnit.objects.get(ID_TEACHINGUNIT=id_unit)
        material = request.FILES.get('material')
        explanation = request.POST.get('explanation')
        print(material, explanation)
        if material and explanation:
            newmaterial.MATERIAL = material
            newmaterial.EXPLANATION = explanation
            newmaterial.save()
            return redirect('mycourse_detail')
        else:
            return render(request, 'authentication/addmaterial.html', {'id_unit': id_unit})

def view_text_file(request, file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/plain')

    
def otherprofile(request):
    if request.method == "POST":
        user_information = User.objects.get(user_id=request.POST.get('user_id'))
        try:
            user_profile_information = UserProfile.objects.get(user_id = user_information)
            if not user_profile_information.picture:
                user_profile_information.picture = " "
        except:
            user_profile_information = UserProfile()
            user_profile_information.picture = " "
            user_profile_information.description = " "
        return render( request, 'authentication/otherprofile.html', {'user_information': user_information,'user_profile_information':user_profile_information})

def editcourse(request):
    if request.method == "POST":
        id_course = request.POST.get('ID_COURSE')
        from_mycourses = request.POST.get('from_mycourses')
        return render(request, 'authentication/editcourse.html', {'categories':Category.objects.all(), 'course':Course.objects.get(ID_COURSE=id_course), 'from_mycourses': from_mycourses})
    
def saveedited(request):
    if request.method == "POST":
        id_course = request.POST.get('ID_COURSE')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        category = request.POST.get('category')

        course = Course.objects.get(ID_COURSE=id_course)
        course.NAME = name
        course.DESCRIPTION = description
        course.PRICE = price
        course.DURATION = duration
        course.ID_CATEGORY_id = category
        course.save()
        from_mycourses = request.POST.get('from_mycourses')
        if from_mycourses:
            return redirect('mycourses')
        else:
            return redirect('administrator')
    
def addchat(request):
    if request.method == "POST":
        return render( request, 'authentication/addchat.html', {'id_course': request.POST.get('ID_COURSE')})
    else:
        return redirect('home')
    
def savechat(request):
    if request.method == "POST":
        ID_COURSE = request.POST.get('ID_COURSE', '')
        date = request.POST.get('date', '')
        link = request.POST.get('link', '')

        online_chat = OnlineChat.objects.filter(ID_COURSE=Course.objects.get(ID_COURSE=ID_COURSE)).first()
        if online_chat:
            online_chat.date = date
            online_chat.link = link
            online_chat.save()
        else:
            online_chat = OnlineChat(ID_COURSE=Course.objects.get(ID_COURSE=ID_COURSE), date=date, link=link)
            online_chat.save()

        return redirect('mycourses')
    else:
        return redirect('home')
    
def deletechat(request):
    if request.method == "POST":
        ID_COURSE = request.POST.get('ID_COURSE', '')
        online_chat = OnlineChat.objects.filter(ID_COURSE=Course.objects.get(ID_COURSE=ID_COURSE)).first()
        if online_chat:
            online_chat.delete()
        return redirect('mycourses')
    else:
        return redirect('mycourses')