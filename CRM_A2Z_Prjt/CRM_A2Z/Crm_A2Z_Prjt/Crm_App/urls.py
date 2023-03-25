from django.contrib import admin
from django.urls import path
from Crm_App import views


app_name = 'Crm_App'

urlpatterns = [

    path('', views.login,name='login'),
    path('logout/',views.logout,name="logout"),
    path('super-admin-register', views.super_admin_register,name='super_admin_register'),
    path('index/', views.index,name='index'),
    path('usermanagement/', views.usermanagement,name='usermanagement'),
    # path('activate-user',views.activate_user,name='activate')
    path('token',views.token_send,name='token_send'),
    path('success',views.success,name='success'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('error',views.error_page,name='error'),
    path('lead-add',views.lead_add,name='lead_add'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-places/', views.load_places, name='ajax_load_places'),
    path('lead-view/<int:id>',views.lead_view,name='lead_view'),
    path('lead-delete/<int:id>',views.lead_delete,name='lead_delete'),
    path('lead-edit/<int:id>',views.lead_edit,name='lead_edit')





    

]