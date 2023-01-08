from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser):
    #REQUIRED_FIELDS = ('email', 'name', 'surname', 'password', 'gender')
    USERNAME_FIELD = 'username'
    
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True, blank=False) 
    username = models.CharField(max_length=255, unique=True,blank=False)
    name = models.CharField(max_length=255,blank=False)
    surname = models.CharField(max_length=255,blank=False)
    password = models.CharField(max_length=255,blank=False)
    gender = models.CharField(max_length=255,blank=False)
    
    objects = UserManager()
    class Meta:
        db_table = 'User'
        
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    class Meta:
        managed = True 
        db_table = 'Category'
        
class FavCategories(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    id_category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'FavCategories'
        
class UserProfile(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    picture = models.FileField()
    description = models.CharField(max_length=255)
    
    class Meta:
        managed = True
        db_table =  'UserProfile'

class Course(models.Model):
    ID_COURSE = models.AutoField(primary_key=True)
    ID_CATEGORY = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)    
    NAME = models.CharField(max_length=255)
    DESCRIPTION = models.TextField()
    LOGO = models.CharField(max_length=255)
    PRICE = models.DecimalField(max_digits=10, decimal_places=2)
    DURATION = models.PositiveIntegerField()
    
    class Meta:
        managed = True
        db_table = 'Course'
    