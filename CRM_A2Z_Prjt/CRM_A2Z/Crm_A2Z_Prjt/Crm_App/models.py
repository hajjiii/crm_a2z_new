from django.db import models
from django.contrib.auth.models import User
# from django.utils.timezone import localdate
import django

# Create your models here.

class Branch(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=250)

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
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    branch = models.CharField(max_length = 25,blank=False,null=False)
    address = models.TextField(blank=False,null=False)
    usertype = models.CharField(max_length=25,blank=False,null=False)
    phn_number = models.CharField(max_length=15,blank=False,null=False)
    user_photo = models.ImageField(upload_to = 'User images',blank=True,null=True)
    visibility = models.CharField(max_length=250,blank=False,null=True)
    employee_type = models.CharField(max_length=250,blank=True,null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,default=1)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)



    # is_employee = models.BooleanField('Is employee', default=False)
    # def save(self,*args,**kwargs):
    #     account_sid = 'AC29149f221485419dafba9246c3e1576e'
    #     auth_token = '4ff5723d9c94257517183cbac5355e84'
    #     client = Client(account_sid,auth_token)
    #     template = render_to_string('registermessge.html',{'emp_name':self.employe_name,'emp_id':self.user.username})
    #     messege = client.messages.create(
    #         body = template,
    #         from_ = '+19705949271',
    #         to = f'+91{self.phn_number}'
    #     )
    #     return super().save(*args,**kwargs)

class State(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100,blank=True,null=True)

    
    
class District(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100,blank=True,null=True)

    
    
class InterestRate(models.Model):
    def __str__(self):
        return self.name
    
    name = models.IntegerField(blank = True,null=True)

    
    
class LeadCategory(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=100, null=True, blank=True)
    




class Leads(models.Model):
    def __str__(self):
        return self.lead_title
    added_by = models.ForeignKey(ExtendedUserModel,on_delete=models.CASCADE, blank=True, null=True)
    lead_title = models.CharField(max_length=100, blank=True, null=True)
    lead_description = models.TextField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person_phone = models.CharField(max_length=30, blank=True, null=True)
    contact_person_designation = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    business_address = models.TextField(blank=True, null=True)
    interest_rate = models.ForeignKey(InterestRate,on_delete=models.CASCADE , blank=True, null=True)
    lead_generated_date = models.DateField(blank=False, null=False)
    next_follow_up_date = models.DateField(blank=False, null=False)
    added_on = models.DateField(auto_now_add=True, blank=False, null=False)
    min_price = models.PositiveBigIntegerField(blank=True, null=True)
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    lead_category = models.ForeignKey(LeadCategory, on_delete=models.CASCADE,blank=True,null=True)
    notes_about_client = models.TextField(blank=True,null=True)


