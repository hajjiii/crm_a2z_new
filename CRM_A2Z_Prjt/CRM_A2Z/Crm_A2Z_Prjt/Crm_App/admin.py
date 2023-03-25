from django.contrib import admin
from Crm_App.models import Branch, City, LeadsView,Status,Usertype,ExtendedUserModel,State,District,InterestRate,LeadStatus,LeadCategory,Leads
# Register your models here.
admin.site.register(Branch)
admin.site.register(Usertype)
admin.site.register(ExtendedUserModel)
admin.site.register(Status)
admin.site.register(State)
admin.site.register(District)
admin.site.register(City)

admin.site.register(InterestRate)
admin.site.register(LeadStatus)
admin.site.register(LeadCategory)
admin.site.register(Leads)
admin.site.register(LeadsView)









