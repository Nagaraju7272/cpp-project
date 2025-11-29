from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class UserModel(UserAdmin):
    list_display =['username','email']
admin.site.register(CustomUser,UserModel)
admin.site.register(Category)
admin.site.register(Passes)
admin.site.register(Page)