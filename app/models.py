from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    

class Category(models.Model):
    categoryname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.categoryname

class Passes(models.Model):
    passnumber = models.IntegerField(default=0)
    fullname = models.CharField(max_length=250)
    gender = models.CharField(max_length=100)
    profile_pic1 = models.ImageField(upload_to='media/')
    mobilenumber = models.CharField(max_length=15)
    email = models.EmailField(max_length=200)
    identitytype = models.CharField(max_length=200)
    identitycardnumber = models.CharField(max_length=250)
    category_id = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    source = models.CharField(max_length=250)
    destinations = models.CharField(max_length=250)
    fromdate = models.CharField(max_length=250)
    todate = models.CharField(max_length=250)
    cost = models.IntegerField(default=0)
    passcreated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.fullname

class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    aboutus = models.TextField()
    email = models.EmailField(max_length=200)
    mobilenumber = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle

