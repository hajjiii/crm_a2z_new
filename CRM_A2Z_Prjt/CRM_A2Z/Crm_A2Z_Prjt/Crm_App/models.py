from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Branch(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=250)
    addrs = models.TextField(max_length=50)
    phn = models.CharField(max_length=10)

class Usertype(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=250)


class Status(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=25)

class ExtendedUserModel(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=False,null=False)
    address = models.TextField(blank=False,null=False)
    usertype = models.CharField(max_length=25,blank=False,null=False)
    phn_number = models.CharField(max_length=15,blank=False,null=False)
    user_photo = models.ImageField(upload_to = 'User images',blank=True,null=True)
    visibility = models.CharField(max_length=250,blank=False,null=True)
    employee_type = models.CharField(max_length=250,blank=True,null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,default=1)
    auth_token = models.CharField(max_length=100,blank=True,null=True)
    is_verified = models.BooleanField(default=False)

    



class State(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100,blank=True,null=True)

    
    
class District(models.Model):
    def __str__(self):
        return self.name

    state = models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)

 
class City(models.Model):
    def __str__(self):
        return self.name

    district = models.ForeignKey(District,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    
    

    
    
class InterestRate(models.Model):
    def __str__(self):
        return str(self.name)
    
    name = models.IntegerField(blank = True,null=True)


class LeadStatus(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=100, null=True, blank=True)


class ProjectStatus(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=100, null=True, blank=True)



    
    
class LeadCategory(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=100, null=True, blank=True)




class Leads(models.Model):
    def __str__(self):
        return self.lead_title
    
    added_by=models.ManyToManyField(ExtendedUserModel, blank=True)
    # added_by = models.ForeignKey(ExtendedUserModel,on_delete=models.CASCADE, blank=True, null=True)
    added_by_admin = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    lead_title = models.CharField(max_length=100, blank=True, null=True)
    lead_description = models.TextField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person_phone = models.CharField(max_length=30, blank=True, null=True)
    contact_person_designation = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE, blank=True, null=True)
    # city = models.CharField(max_length=100,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    interest_rate = models.ForeignKey(InterestRate,on_delete=models.CASCADE , blank=True, null=True)
    lead_generated_date = models.DateField(blank=False, null=False)
    next_follow_up_date = models.DateField(blank=False, null=False)
    added_on = models.DateField(auto_now_add=True, blank=False, null=False)
    min_price = models.PositiveBigIntegerField(blank=True, null=True)
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    lead_category = models.ForeignKey(LeadCategory, on_delete=models.CASCADE,blank=True,null=True)
    status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE,blank=True,null=True,default=7)
    lead_delivery_date = models.DateField(blank=True,null=True)
    # notes_about_client = models.TextField(blank=True,null=True)
    note_about_field_executive = models.TextField(blank=True,null=True)




class TempLead(models.Model):
    def __str__(self):
        return self.lead_title
    lead = models.ForeignKey(Leads, on_delete=models.SET_NULL,blank=True,null=True)
    lead_title = models.CharField(max_length=100, blank=True, null=True)
    lead_description = models.TextField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person_phone = models.CharField(max_length=30, blank=True, null=True)
    contact_person_designation = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    interest_rate = models.ForeignKey(InterestRate, on_delete=models.CASCADE , blank=True, null=True)
    lead_generated_date = models.DateField(blank=False, null=False)
    next_follow_up_date = models.DateField(blank=False, null=False)
    min_price = models.PositiveBigIntegerField(blank=True, null=True)
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    lead_category = models.ForeignKey(LeadCategory, on_delete=models.CASCADE, blank=True, null=True)
    lead_delivery_date = models.DateField(blank=True,null=True)
    status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, blank=True, null=True, default='Fresh')
    notes_about_client = models.TextField(blank=True,null=True)




class LeadsView(models.Model):
    lead = models.ForeignKey(Leads,on_delete=models.CASCADE,blank=True,null=True,related_name='leads')
    temp_lead = models.ForeignKey(TempLead,on_delete=models.CASCADE,blank=True,null=True,related_name='tleads')
    notes_about_client = models.TextField(blank=True,null=True) 
    # project = models.ForeignKey(Project,on_delete=models.CASCADE,blank=True,null=True,related_name='projects')






class Notification(models.Model):
    def __str__(self):
        return self.key
    status_choices = (
        ('0','0'),
        ('1','1'),
    )
    key = models.CharField(max_length=25, blank=True, null=True)
    notification_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=25,choices=status_choices,blank=False,null=False,default=0)
    added_on = models.DateField(auto_now_add=True, blank=False, null=False)
    notified_by = models.CharField(max_length=100, blank=True, null=True)
    table_link = models.TextField(blank=True, null=True)
    lead = models.ForeignKey(Leads,on_delete=models.SET_NULL,blank=True,null=True,related_name='nlead')


class Project(models.Model):
    def __str__(self):
        return self.lead_title
    
    key = models.CharField(max_length=25, blank=True, null=True)
    added_by=models.ManyToManyField(ExtendedUserModel, blank=True)
    # added_by = models.ForeignKey(ExtendedUserModel,on_delete=models.CASCADE, blank=True, null=True)
    added_by_admin = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    lead_title = models.CharField(max_length=100, blank=True, null=True)
    lead_description = models.TextField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person_phone = models.CharField(max_length=30, blank=True, null=True)
    contact_person_designation = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE, blank=True, null=True)
    # city = models.CharField(max_length=100,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    interest_rate = models.ForeignKey(InterestRate,on_delete=models.CASCADE , blank=True, null=True)
    lead_generated_date = models.DateField(blank=False, null=False)
    next_follow_up_date = models.DateField(blank=False, null=False)
    added_on = models.DateField(auto_now_add=True, blank=False, null=False)
    min_price = models.PositiveBigIntegerField(blank=True, null=True)
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    lead_category = models.ForeignKey(LeadCategory, on_delete=models.CASCADE,blank=True,null=True)
    status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE,blank=True,null=True,default=1)
    lead_delivery_date = models.DateField(blank=True,null=True)
    lead = models.ForeignKey(Leads, on_delete=models.SET_NULL,blank=True,null=True,related_name='projectlead')
    lead_view = models.ForeignKey(LeadsView,on_delete=models.SET_NULL,blank=True,null=True,related_name='lead_view')



class ProjectModule(models.Model):
    def __str__(self):
        return self.module_title
    key = models.CharField(max_length=25, blank=True, null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,blank=True,null=True,related_name='projectmoduleprjct')
    lead = models.ForeignKey(Leads,on_delete=models.SET_NULL,blank=True,null=True,related_name='projectmodulelead')
    added_by = models.ForeignKey(ExtendedUserModel,on_delete=models.CASCADE,blank=True,null=True,related_name='projectModuleuser')
    added_by_admin = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    added_on = models.DateField(auto_now_add=True, blank=False, null=False)
    module_title = models.CharField(max_length=100, blank=True, null=True)
    module_description = models.TextField(blank=True, null=True)
    status_choices = (
        ('0','0'),
        ('1','1'),

    )
    status = models.CharField(choices=status_choices,max_length=10,default='1')




class ProjectAssignment(models.Model):
    key = models.CharField(max_length=25, blank=True, null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,blank=True,null=True,related_name='projectasgnmntmodule')    
    lead = models.ForeignKey(Leads,on_delete=models.SET_NULL,blank=True,null=True,related_name='projectasgnmntlead')
    # project_module = models.ForeignKey(ProjectModule,on_delete=models.CASCADE,blank=True,null=True,related_name='module')
    added_by = models.ForeignKey(ExtendedUserModel,on_delete=models.CASCADE,blank=True,null=True)
    added_by_admin = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    added_on = models.DateField(auto_now_add=True, blank=False, null=False)
    module_assigned = models.ManyToManyField(ProjectModule,related_name='module_assigned', blank=True)
    project_assignment = models.ManyToManyField(ExtendedUserModel,related_name='project_assignment', blank=True)
    branch =  models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='branch', blank=True)
    assign_globaly = models.ForeignKey(ExtendedUserModel,related_name='assign_globaly', blank=True,on_delete=models.SET_NULL,null=True)



