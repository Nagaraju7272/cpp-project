
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('login/', views.LOGIN, name='login'),
    path('doLogout', views.doLogout, name='logout'),
   


    path('Dashboard', views.DASHBOARD, name='dashboard'),    
    path('doLogin', views.doLogin, name='doLogin'),
    path('', views.LANDINGPAGE, name='landingpage'),


    #profile Path
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),
    #Category Path
    path('Category/add', views.ADD_CATEGORY, name='add_category'),
    path('ManageCategory', views.MANAGE_CATEGORY, name='manage_category'),
    path('DeleteCategory/<str:id>', views.DELETE_Category, name='delete_category'),
    path('UpdateCategory/<str:id>', views.UPDATE_Category, name='update_category'),
    path('UPDATE_CATEGORY_DETAILS', views.UPDATE_CATEGORY_DETAILS, name='update_category_details'),

    #Passes Path
     path('Pases/add', views.ADD_PASSSES, name='add_passes'),
     path('ManagePasses', views.MANAGE_PASSES, name='manage_passes'),
     path('DeletePasses/<str:id>', views.DELETE_PASSES, name='delete_passes'),
     path('ViewPasses/<str:id>', views.VIEW_PASSES, name='view_passes'),
     path('my_view/', views.my_view, name='my_view'),

     #Website Page
     path('Website/update', views.WEBSITE_UPDATE, name='website_update'),
     path('UPDATE_WEBSITE_DETAILS', views.UPDATE_WEBSITE_DETAILS, name='update_website_details'),

     #search passes
     path('Search', views.Search_Passes, name='search_passes'),

      path('data-between-dates/', views.data_between_dates, name='data_between_dates'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
