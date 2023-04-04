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
    path('lead-edit/<int:id>',views.lead_edit,name='lead_edit'),
    path('lead-preview/<int:id>',views.lead_preview,name='lead_preview'),
    path('lead-edit-approve/<int:id>',views.approve_lead_edit,name='approve_lead_edit'),
    path('lead-change-request',views.lead_change_request,name='lead_change_request'),
    path('lead-change-request-view/<int:id>',views.lead_change_request_view,name='lead_change_request_view'),
    path('lead-change-request-preview/<int:id>',views.lead_request_change_preview,name='lead_request_change_preview'),
    path('lead-change-request-edit-approve/<int:id>',views.approve_lead_request_change_edit,name='approve_lead_request_change_edit'),
    path('lead-help-centre',views.lead_help_centre,name='lead_help_centre'),
    path('lead-help-centre/<int:id>',views.lead_help_centre_edit,name='exit_lead'),
    path('lead-manpower-request-edit/<int:id>',views.lead_manpower_request,name='lead_manpower_request'),
    path('notifications/<int:id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('lead-help-centre-action/<int:id>',views.lead_help_centre_action,name='help_centre_action'),
    path('exit-lead-action/<int:id>',views.exit_lead_action,name='exit_lead_action'),







    



    











    

]