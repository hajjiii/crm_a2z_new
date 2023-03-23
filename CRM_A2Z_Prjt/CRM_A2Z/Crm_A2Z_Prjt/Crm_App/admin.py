from django.contrib import admin
from Crm_App.models import Branch,Status,Usertype,ExtendedUserModel
# Register your models here.
admin.site.register(Branch)
admin.site.register(Usertype)
admin.site.register(ExtendedUserModel)
admin.site.register(Status)

