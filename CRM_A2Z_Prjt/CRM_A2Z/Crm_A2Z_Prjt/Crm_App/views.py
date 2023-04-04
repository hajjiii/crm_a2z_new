from django.forms import modelformset_factory
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http.response import JsonResponse
from django.urls import reverse
from Crm_App.models import Branch,Usertype,ExtendedUserModel
import uuid
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from .filters import LeadFilter
from django.db import transaction, IntegrityError
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.humanize.templatetags.humanize import apnumber
from django.template.loader import render_to_string
from hashlib import blake2b
import time
from django.db.models import Q

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, State):
            return str(obj)
        return super().default(obj)

def serialize_edited_value(data):
    return json.dumps(data, cls=CustomJSONEncoder)


def index(request):
    if 'username' in request.session:
        return render(request,'index.html')
    else:
        return redirect('Crm_App:login')




def usermanagement(request):
    branch = Branch.objects.all()
    usertype = Usertype.objects.all()
    usermanagement = ExtendedUserModel.objects.all().order_by('-id')
    if request.method == 'POST':
        if request.POST.get('password') == request.POST.get('password2'):
            try:
                user = User.objects.get(username=request.POST.get('username'))
                print('username already taken')
                messages.error(request,'Username already taken')
                return redirect('Crm_App:usermanagement')
                # return render(request,'usermanagement.html',{'error':"Username already taken"})
                
            except User.DoesNotExist:
                email = request.POST.get('email')
                user = User.objects.create_user(username = request.POST.get('username'), password = request.POST.get('password'),email=email)
                usertype = request.POST.get('usertype')
                mob = request.POST.get('mob')
                branch = request.POST.get('branch')
                print(branch)
                address = request.POST.get('address')
                emp_type = request.POST.get('emp_type')
                # if len(request.FILES) !=0:
                profile_pic = request.FILES.get('profile_pic')
                visibility = request.POST.get('visiblity')
                auth_token = str(uuid.uuid4())
                extenduser = ExtendedUserModel(branch=branch,address=address,phn_number=mob,usertype=usertype,user=user,user_photo=profile_pic,visibility=visibility,employee_type=emp_type,auth_token= auth_token)
                
                extenduser.save();
                print('user created')

                messages.success(request,'Successfully Registered')
                # return redirect('Crm_App:usermanagement')
                send_mail_after_registration(email , token=auth_token)
                return redirect('Crm_App:token_send')
        else:
            print('password not matching')
            messages.error(request,'Password not matching')
            return redirect('Crm_App:usermanagement')
    else:
        context = {
            'branch':branch,
            'usertype':usertype,
            'usermanagement':usermanagement,
        }
        return render(request,'usermanagement.html',context)


def lead_add(request):
    if request.user.is_superuser:
            name = request.user
    else:
        name = request.user.username
        added_by = ExtendedUserModel.objects.get(user__username = name )
    form = LeadAddForm()
    if request.method == 'POST':
        form = LeadAddForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            if request.user.is_superuser:
                data.added_by_admin.set([name])

            else:
                data.added_by.set([added_by])

            form.save_m2m()
            return redirect('Crm_App:lead_add')
    else:
        form=LeadAddForm()
    
    all_leads = Leads.objects.all()
    lead_filter = LeadFilter(request.GET, queryset=all_leads)

    context ={
        'form':form,
        'all_leads':all_leads,
        'filter': lead_filter

    }
    return render(request,'leads.html',context)

def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = District.objects.filter(state=country_id).all()
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def load_places(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(district=country_id).all()
    return render(request, 'place_dropdown_list_options.html', {'cities': cities})



def lead_view(request,id):

    qs = Leads.objects.get(id=id)
    form = LeadAddForm(instance=qs)
    ProductsFormset = modelformset_factory(LeadsView, form=LeadViewForm)
    formset = ProductsFormset(request.POST or None, queryset=qs.leads.all(), prefix='leads')


    context = {
        'form':form,
        'formset':formset,
    }
    return render(request,'leads-view.html',context)


def lead_delete(request,id):
    qs = Leads.objects.get(id=id)
    qs.delete()
    return redirect('Crm_App:lead_add')

def lead_edit(request, id):
    ProductsFormset = modelformset_factory(LeadsView, form=LeadViewForm)
    lead = Leads.objects.filter(id=id).first()
    form = LeadAddForm(instance=lead)
    formset = ProductsFormset(request.POST or None, queryset=lead.leads.all(), prefix='leads')
    if request.method == 'POST':
        form = LeadAddForm(request.POST, instance=lead)
        print(form)
        if form.is_valid() and formset.is_valid():
            lead_edit = TempLead.objects.create(
                # user=request.user,
                lead=lead,
                lead_title=form.cleaned_data['lead_title'],
                lead_description=form.cleaned_data['lead_description'],
                contact_person_name=form.cleaned_data['contact_person_name'],
                contact_person_phone=form.cleaned_data['contact_person_phone'],
                contact_person_designation = form.cleaned_data['contact_person_designation'],
                business_name = form.cleaned_data['business_name'],
                state = form.cleaned_data['state'],
                district = form.cleaned_data['district'],
                city = form.cleaned_data['city'],
                business_address = form.cleaned_data['business_address'],
                interest_rate = form.cleaned_data['interest_rate'],
                lead_generated_date = form.cleaned_data['lead_generated_date'],
                next_follow_up_date = form.cleaned_data['next_follow_up_date'],
                min_price = form.cleaned_data['min_price'],
                max_price = form.cleaned_data['max_price'],
                lead_category = form.cleaned_data['lead_category'],
                status = form.cleaned_data['status'],
                notes_about_client = form.cleaned_data['notes_about_client'],
            )
            lead_edit.save()
            if all('notes_about_client' in forms.cleaned_data and forms.cleaned_data['notes_about_client'] for forms in formset):
                with transaction.atomic():
                    for data in formset.save(commit=False):
                        data.lead = lead
                        data.save()
                return redirect('Crm_App:lead_add')
            else:
                formset.non_form_errors().append("Note field cannot be empty")
        else:
            print(formset.errors)
    
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'lead-edit.html', context)

def lead_preview(request,id):
    temp = TempLead.objects.filter(lead__id=id).first()
    print(temp)
    if not temp:
        return HttpResponseNotFound("Lead not found")

    form = LeadAddForm(instance=temp)
    context = {
        'form':form,
        'approve_url': reverse('Crm_App:approve_lead_edit', args=[temp.id]),
    }
    return render(request,'lead-preview.html',context)

def approve_lead_edit(request, id):
    lead_edit = TempLead.objects.filter(id=id).first()
    if lead_edit:
        lead = lead_edit.lead
        lead.lead_title = lead_edit.lead_title
        lead.lead_description = lead_edit.lead_description
        lead.contact_person_name = lead_edit.contact_person_name
        lead.contact_person_phone = lead_edit.contact_person_phone
        lead.contact_person_designation = lead_edit.contact_person_designation
        lead.business_name = lead_edit.business_name
        lead.state = lead_edit.state
        lead.district = lead_edit.district
        lead.city = lead_edit.city
        lead.business_address = lead_edit.business_address
        lead.interest_rate = lead_edit.interest_rate
        lead.lead_generated_date = lead_edit.lead_generated_date
        lead.next_follow_up_date = lead_edit.next_follow_up_date
        lead.min_price = lead_edit.min_price
        lead.max_price = lead_edit.max_price
        lead.lead_category = lead_edit.lead_category
        lead.status = lead_edit.status
        lead.notes_about_client = lead_edit.notes_about_client
        lead.save()
        lead_edit.delete()
    return redirect('Crm_App:lead_add')


def lead_change_request(request):
    qs = TempLead.objects.all()
    print(qs)
    context = {
        'qs':qs
    }
    return render(request,'lead-change-request.html',context)



def lead_change_request_view(request,id):

    qs = TempLead.objects.filter(id=id).first()
    qss = qs.lead
    form = LeadAddForm(instance=qs)
    ProductsFormset = modelformset_factory(LeadsView, form=LeadViewForm)
    formset = ProductsFormset(request.POST or None, queryset=qss.leads.all(), prefix='leads')
    # print(formset)


    context = {
        'form':form,
        'formset':formset,
    }
    return render(request,'leads-change-request-view.html',context)

def lead_request_change_preview(request,id):
    temp = TempLead.objects.filter(id=id).first()
    print('leadname',temp)
    if not temp:
        return HttpResponseNotFound("Lead not found")

    form = LeadAddForm(instance=temp)
    context = {
        'form':form,
        'approve_url': reverse('Crm_App:approve_lead_request_change_edit', args=[temp.id]),
    }
    return render(request,'lead-request-change-preview.html',context)



def approve_lead_request_change_edit(request, id):
    lead_edit = TempLead.objects.filter(id=id).first()
    if lead_edit:
        lead = lead_edit.lead
        lead.lead_title = lead_edit.lead_title
        lead.lead_description = lead_edit.lead_description
        lead.contact_person_name = lead_edit.contact_person_name
        lead.contact_person_phone = lead_edit.contact_person_phone
        lead.contact_person_designation = lead_edit.contact_person_designation
        lead.business_name = lead_edit.business_name
        lead.state = lead_edit.state
        lead.district = lead_edit.district
        lead.city = lead_edit.city
        lead.business_address = lead_edit.business_address
        lead.interest_rate = lead_edit.interest_rate
        lead.lead_generated_date = lead_edit.lead_generated_date
        lead.next_follow_up_date = lead_edit.next_follow_up_date
        lead.min_price = lead_edit.min_price
        lead.max_price = lead_edit.max_price
        lead.lead_category = lead_edit.lead_category
        lead.status = lead_edit.status
        lead.notes_about_client = lead_edit.notes_about_client
        lead.save()
        lead_edit.delete()
    return redirect('Crm_App:lead_change_request')



def lead_help_centre(request):
    
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
    leads = Leads.objects.filter(added_by__user=request.user)
    print(leads)
    # lead = Leads.objects.get(id=<lead_id>)
    # for lead in leads:
    #     for user in lead.added_by.all(): many to many field
    #         print(user)

    all_notification = Notification.objects.all()
    
    
    notification =Notification.objects.filter(status=0)
    notification_count = notification.count()
    context = {
        'leads':leads,
        'notification_count':notification_count,
        'notification':notification,
        'all_notification':all_notification
    }
    return render(request,'helpcenter.html',context)



def lead_help_centre_edit(request,id):
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
    lead = Leads.objects.get(id=id)
    added_by = request.user.username
    table_link = 'http://192.168.1.10:8989/lead-help-centre/'
    instance = Notification.objects.filter(lead=lead, notified_by=added_by,table_link=table_link).first()
    form = NotificationForm(request.POST or None, instance=instance)
    leads_form = LeadAddForm(request.POST or None, instance=lead)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.key = key
            form.instance.notification_title = 'request for exitlead'
            form.instance.lead = lead
            form.instance.notified_by = added_by
            form.instance.table_link = table_link
            form.save()
            return redirect('Crm_App:lead_help_centre')
    context = {'form': form,'leads_form':leads_form}
    return render(request,'exit-lead.html', context)



def lead_manpower_request(request,id):
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
    lead = Leads.objects.get(id=id)
    added_by = request.user.username
    table_link = 'http://192.168.1.10:8989/lead-manpower-request-edit/'
    instance = Notification.objects.filter(lead=lead, notified_by=added_by,table_link=table_link).first()
    leads_form = LeadAddForm(request.POST or None, instance=lead)
    form = NotificationForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.key = key
            form.instance.notification_title = 'request for Manpower'
            form.instance.lead = lead
            form.instance.notified_by = added_by
            form.instance.table_link = table_link
            form.save()
            return redirect('Crm_App:lead_help_centre')
    context = {'form': form,'leads_form': leads_form}
    return render(request,'manpower-request.html',context)




def mark_notification_as_read(request, id):
    notification = Notification.objects.get(id=id)
    notification.status = 1
    notification.save()
    return redirect('Crm_App:lead_help_centre')
    # return JsonResponse({'success': True})
    # return redirect('{}{}'.format(notification.table_link, notification.lead.id))


def lead_help_centre_action(request,id):
    notification = Notification.objects.get(id=id)
    lead = notification.lead
    form = LeadsManpowerAssignmentForm(request.POST or None,instance=lead)

    if request.method == 'POST':
        if form.is_valid():
            lead = form.save(commit=False)  # don't save the form yet
            form.save_m2m()  # save the many-to-many relationships
            lead.save()
            return redirect('Crm_App:lead_help_centre')
        
    context = {
        'form':form
    }
    return render(request,'help-centre-action.html',context)


def exit_lead_action(request,id):
    notification = Notification.objects.get(id=id)
    lead = notification.lead
    # lead_owner_branch = lead.added_by.Branch
    form = ExitLeadAssignmentForm(request.POST or None,instance=lead)
    if request.method == 'POST':
        if form.is_valid():
            lead = form.save(commit=False)  # don't save the form yet
            lead.added_by.clear()
            form.save_m2m()  # save the many-to-many relationships
            lead.save()
            return redirect('Crm_App:lead_help_centre')
        
    context = {
        'form':form
    }
    return render(request,'exit-lead-action.html',context)










def super_admin_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")  
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("username alredy exists")
                messages.info(request,"username already exist")
                return redirect("Crm_App:super_admin_register")
            elif User.objects.filter(email=email).exists():
                print("email alredy exists")
                messages.info(request,"email already registered")
                return redirect("Crm_App:super_admin_register")
            else:
                user = User.objects.create_user(username=username,email=email,password=password1,is_superuser=True,is_active=True,is_staff=True)
                user.save();
                print('user created')
               
                return redirect('Crm_App:login')
        else:
            print('Password Not Matched')
            messages.info(request,"Incorrect Password")
            return redirect('Crm_App:super_admin_register')
    return render(request,'super-admin-signup.html')






def login(request):
    if 'username' in request.session:
        return redirect('Crm_App:index')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        obj = User.objects.filter(username=username).first()
        user_obj = ExtendedUserModel.objects.filter(user=obj).first()
        # print(user_obj)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                request.session['username'] = username
                auth.login(request, user)
                print('logged in as superuser')
                return JsonResponse({'success':True}, safe=False)
            else:
                user_obj = ExtendedUserModel.objects.filter(user=user).first()
                print(user_obj)
                if user_obj.is_verified:
                    request.session['username'] = username
                    auth.login(request, user)
                    print('logged in')
                    return JsonResponse({'success':True}, safe=False)
                else:
                    print('not verified')
                    messages.error(request,'Email is not verified, please check your email inbox')
                    return render(request, 'login.html', {'error':'error'})
        else:
            messages.error(request,'Invalid username or password')
            return render(request, 'login.html', {'error':'error'})
        
    else:
        return render(request,'login.html')





def logout(request):
    if 'username' in request.session:
        request.session.flush();
    return redirect("Crm_App:login")





def success(request):
    return render(request,'success.html')


def token_send(request):
    return render(request,'token_send.html')


def verify(request,auth_token):
    try:
        user_obj = ExtendedUserModel.objects.filter(auth_token = auth_token).first()
        print(user_obj)
        if user_obj:
            if user_obj.is_verified:
                print('Your account is already verified')
                messages.success(request,'Your account is already verified')
                return redirect('Crm_App:login')
            user_obj.is_verified = True
            user_obj.save()
            messages.success(request,'Your account has been verified')
            return redirect('Crm_App:usermanagement')
        else:
            return redirect('Crm_App:error')
    except Exception as e:
        print(e)


def error_page(request):
    return render(request,'error.html')


def send_mail_after_registration(email,token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://192.168.1.10:8989/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email ,]
    send_mail(subject ,message,email_from, recipient_list)


    