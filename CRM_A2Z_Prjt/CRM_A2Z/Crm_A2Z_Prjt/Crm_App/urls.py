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
    path('usermanagement-view/<int:user_id>/', views.usermanagement_view,name='usermanagement_view'),
    path('branch', views.branch,name='branch'),
    path('token',views.token_send,name='token_send'),
    path('success',views.success,name='success'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('error',views.error_page,name='error'),
    path('branch-update/<int:branch_id>/', views.branch_update,name='branch_update'),
    path('branch-delete/<int:branch_id>/', views.branch_delete,name='branch_delete'),
    path('profile-view', views.profile_view,name='profile_view'),

    
    path('state-add', views.state_add,name='state_add'),
    path('state-update/<int:state_id>/', views.state_update,name='state_update'),
    path('state-delete/<int:state_id>/', views.state_delete,name='state_delete'),
    path('usertype-settings', views.usertype_settings,name='usertype_settings'),
    path('usertype-update/<int:user_id>/', views.usertype_update,name='usertype_update'),
    path('usertype-delete/<int:user_id>/', views.usertype_delete,name='usertype_delete'),
    
    
    path('district-add', views.district_add,name='district_add'),
    path('district-update/<int:district_id>/', views.district_update,name='district_update'),
    path('district-delete/<int:district_id>/', views.district_delete,name='district_delete'),
    path('city-add', views.city_add,name='city_add'),
    path('city-update/<int:city_id>/', views.city_update,name='city_update'),
    path('city-delete/<int:city_id>/', views.city_delete,name='city_delete'),

    

    path('lead-add',views.lead_add,name='lead_add'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-places/', views.load_places, name='ajax_load_places'),
    path('lead-view/<int:id>',views.lead_view,name='lead_view'),
    path('tlead-edit/<int:id>',views.tlead_edit,name='tlead_edit'),
    path('lead-preview/<int:id>',views.lead_preview,name='lead_preview'),
    path('lead-edit-approve/<int:id>',views.approve_lead_edit,name='approve_lead_edit'),
    path('lead-delete/<int:id>',views.lead_delete,name='lead_delete'),
    path('lead-change-request',views.lead_change_request,name='lead_change_request'),
    path('lead-change-request-view/<int:id>',views.lead_change_request_view,name='lead_change_request_view'),
    path('lead-change-request-preview/<int:id>',views.lead_request_change_preview,name='lead_request_change_preview'),
    path('lead-edit/<int:id>',views.lead_edit,name='lead_edit'),
    path('lead-change-request-edit-approve/<int:id>',views.approve_lead_request_change_edit,name='approve_lead_request_change_edit'),
    path('lead-change-request-edit/<int:id>',views.lead_change_request_edit,name='lead_change_request_edit'),

    path('lead-help-centre',views.lead_help_centre,name='lead_help_centre'),
    path('lead-help-centre/<int:id>',views.lead_help_centre_edit,name='exit_lead'),

    path('lead-manpower-request-edit/<int:id>',views.lead_manpower_request,name='lead_manpower_request'),
    path('notifications/<int:id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('lead-help-centre-action/<int:id>',views.lead_help_centre_action,name='help_centre_action'),
    path('exit-lead-action/<int:id>',views.exit_lead_action,name='exit_lead_action'),


    path('place-management',views.placemanagement,name='placemanagement'),
    path('state-add',views.state_add,name='state_add'),


    

    path('follow-up-reminder',views.follow_up_reminder,name='follow_up_reminder'),



    path('usermanagement-update/<int:user_id>/', views.usermanagement_update,name='usermanagement_update'),
    path('usermanagement-delete/<int:usr_id>/', views.usermanagement_delete,name='usermanagement_delete'),
    path('project-management/', views.project_management,name='project_management'),
    path('project-delete/<int:project_id>/', views.project_delete,name='project_delete'),
    path('project-view/<int:id>',views.project_view,name='project_view'),

    path('project-edit/<int:project_id>/', views.project_edit,name='project_edit'),
    path('module-add/<int:id>/', views.module_add,name='module_add'),
    path('module-delete/<int:id>/', views.module_delete,name='module_delete'),
    path('project-assignment/<int:id>/', views.project_assignment,name='project_assignment'),
    path('load_assign_globaly', views.load_assign_globaly, name='load_assign_globaly'),
    path('ajax/load-branches/', views.load_branches, name='ajax_load_branches'),






    

    


    
    

    

]