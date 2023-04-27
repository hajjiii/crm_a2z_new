from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http.response import JsonResponse
from django.urls import reverse
from Crm_App.models import *
from .forms import *
from django.template.loader import render_to_string
from .filters import LeadFilter
from email.message import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction, IntegrityError
from hashlib import blake2b
import time
import uuid
from django.forms import modelformset_factory
import datetime


# Create your views here.



def index(request):
    if 'username' in request.session:
        return render(request,'index.html')
    else:
        return redirect('Crm_App:login')





def usermanagement(request):
    branch = Branch.objects.all()
    usertype = Usertype.objects.all()
    usermanagement = User.objects.prefetch_related('user').exclude(is_superuser = 1).order_by('-id')
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


    
def usermanagement_update(request,user_id):
    usertype = Usertype.objects.all()
    branch = Branch.objects.all()
    usrmanagement = User.objects.prefetch_related('user').exclude(is_superuser = 1).filter(id=user_id).first()
    if request.method == 'POST':
        usrmanagement.username = request.POST.get('username')
        usrmanagement.user.phn_number = request.POST.get('mob')
        usrmanagement.email = request.POST.get('email')
        usrmanagement.user.usertype = request.POST.get('usertype')
        usrmanagement.user.user_photo = request.FILES.get('profile_pic')
        usrmanagement.user.branch = request.POST.get('branch')
        usrmanagement.user.visibility = request.POST.get('visibility')
        usrmanagement.user.employee_type = request.POST.get('employe_type')
        usrmanagement.user.address = request.POST.get('addrs')
        usrmanagement.user.save() # Save the related ExtendedUserModel instance
        usrmanagement.save() # Save the User instance
        messages.success(request,'Updated Successfully...')
        return redirect('Crm_App:usermanagement')
    else:
        context = {
            'form':usrmanagement,
            'usertype':usertype,
            'branch':branch
        }
        return render(request,'usermanagement-update.html',context)



def usermanagement_view(request,user_id):
    usrmanagement = User.objects.prefetch_related('user').filter(id=user_id).first()
    context = {
        'usrmanagement':usrmanagement
    }
    return render(request,'usermanagement-view.html',context)






    
def usermanagement_delete(request,usr_id):
    dlt = User.objects.filter(id=usr_id)
    dlt.delete()
    messages.success(request,'Deleted')
    return redirect('Crm_App:usermanagement')



def branch(request):
    branch = Branch.objects.all()
    if request.method == 'POST':
        form = BranchAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Branch Created')
            return redirect('Crm_App:branch')
    else:
        form = BranchAddForm()
    return render(request,'branch.html',{'form':form,'branch':branch})


def branch_update(request,branch_id):
    branch = Branch.objects.filter(id = branch_id).first()
    if request.method == 'POST':
        form = BranchUpdateForm(request.POST,instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Updated')
            return redirect('Crm_App:branch')
    else:
        form = BranchUpdateForm(instance=branch)
        messages.error(request,'Updation Failed')
    return render(request,'branch-update.html',{'form':form})





def branch_delete(request,branch_id):
    branch = Branch.objects.filter(id=branch_id)
    branch.delete()
    messages.success(request,'Deleted')
    return redirect('Crm_App:branch')



def profile_view(request):
    return render(request,'profile-view.html')




def lead_add(request):
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
    if request.user.is_superuser:
        name = request.user
    else:
        name = request.user.username
        added_by = ExtendedUserModel.objects.get(user__username=name)
    form = LeadAddForm()
    if request.method == 'POST':
        form = LeadAddForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            if request.user.is_superuser:
                data.added_by_admin = name
            else:
                data.save()
                data.added_by.set([added_by])

            # Check if the status of the lead is 'Closed'
            data.save()
            if str(data.status) == 'Closed':

                project = Project.objects.create(
                    key=key,
                    lead_title=data.lead_title,
                    lead_description=data.lead_description,
                    contact_person_name=data.contact_person_name,
                    contact_person_phone=data.contact_person_phone,
                    contact_person_designation=data.contact_person_designation,
                    business_name=data.business_name,
                    state=data.state,
                    district=data.district,
                    city=data.city,
                    business_address=data.business_address,
                    interest_rate=data.interest_rate,
                    lead_generated_date=data.lead_generated_date,
                    next_follow_up_date=data.next_follow_up_date,
                    min_price=data.min_price,
                    max_price=data.max_price,
                    lead_category=data.lead_category,
                    lead_delivery_date=data.lead_delivery_date,
                    lead=data
                )
                for i in data.added_by.all():
                    project.added_by.add(i)
                project.save()
            messages.success(request, 'Lead Added')
            return redirect('Crm_App:lead_add')
    else:
        form = LeadAddForm()

    if request.user.is_superuser:
        all_leads = Leads.objects.all().order_by('-id')
        lead_filter = LeadFilter(request.GET, queryset=all_leads)
    else:
        all_leads = Leads.objects.filter(added_by__user__username=request.user.username).order_by('-id')
        lead_filter = LeadFilter(request.GET, queryset=all_leads)

    context = {
        'form': form,
        'all_leads': all_leads,
        'filter': lead_filter
    }
    return render(request, 'leads.html', context)


  


def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = District.objects.filter(state=country_id).all()
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def load_places(request):
    country_id = request.GET.get('districtId')
    cities = City.objects.filter(district=country_id).all()
    return render(request, 'place_dropdown_list_options.html', {'cities': cities})

def load_branches(request):
    branch_id = request.GET.get('branch_id')
    branches = ExtendedUserModel.objects.filter(branch=branch_id).all()
    
    return render(request, 'branch_dropdown_list_options.html', {'branches': branches})

def load_assign_globaly(request):
    branch_id = request.GET.get('branch_id')
    assign_globaly = ExtendedUserModel.objects.filter(employee_type='Global', branch=branch_id).exclude(branch=request.user.user.branch)
    html = render_to_string('assign-globally-options.html', {'assign_globaly': assign_globaly})
    return HttpResponse(html)


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



def tlead_edit(request, id):
    lead = Leads.objects.filter(id=id).first()
    
    # Check if a corresponding TempLead object exists
    
    
    ProductsFormset = modelformset_factory(LeadsView, form=LeadViewForm)
    form = LeadAddForm(instance=lead)
    formset = ProductsFormset(request.POST or None, queryset=lead.leads.all(), prefix='leads')
    if request.method == 'POST':
        form = LeadAddForm(request.POST, instance=lead)
        print(form)
        if form.is_valid() and formset.is_valid():
            if TempLead.objects.filter(lead=lead).exists():
                # Lead has already been approved, cannot be edited
                messages.error(request, 'This lead has already been waiting for approval and cannot be edited.')
                return redirect('Crm_App:lead_add')
            
            lead_edit = TempLead.objects.create(
                lead=lead,
                lead_title=form.cleaned_data['lead_title'],
                lead_description=form.cleaned_data['lead_description'],
                contact_person_name=form.cleaned_data['contact_person_name'],
                contact_person_phone=form.cleaned_data['contact_person_phone'],
                contact_person_designation=form.cleaned_data['contact_person_designation'],
                business_name=form.cleaned_data['business_name'],
                state=form.cleaned_data['state'],
                district=form.cleaned_data['district'],
                city=form.cleaned_data['city'],
                business_address=form.cleaned_data['business_address'],
                interest_rate=form.cleaned_data['interest_rate'],
                lead_generated_date=form.cleaned_data['lead_generated_date'],
                next_follow_up_date=form.cleaned_data['next_follow_up_date'],
                min_price=form.cleaned_data['min_price'],
                max_price=form.cleaned_data['max_price'],
                lead_category=form.cleaned_data['lead_category'],
                lead_delivery_date=form.cleaned_data['lead_delivery_date'],
                status=form.cleaned_data['status'],
                notes_about_client=form.cleaned_data['notes_about_client'],
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
    if lead.status.name == 'Closed':
        for field in form.fields.values():
            field.disabled = True

        for frm in formset.forms:
            for field in frm.fields.values():
                field.disabled = True

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'tlead-edit.html', context)







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
        print('HELLOOOOO',lead.status)
        if lead_edit.status == 'Closed':
                project = Project.objects.create(
                    added_by = lead.added_by,
                    lead_title = lead.lead_title,
                    lead_description = lead.lead_description,
                    contact_person_name = lead.contact_person_name,
                    contact_person_phone = lead.contact_person_phone,
                    contact_person_designation = lead.contact_person_designation,
                    business_name = lead.business_name,
                    state = lead.state,
                    district = lead.district,
                    city = lead.city,
                    business_address = lead.business_address,
                    interest_rate =lead.interest_rate,
                    lead_generated_date = lead.lead_generated_date,
                    next_follow_up_date = lead.next_follow_up_date,
                    min_price = lead.min_price,
                    max_price = lead.max_price,
                    lead_category = lead.lead_category,
                    lead_delivery_date = lead.lead_delivery_date,
                )
                project.save()
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
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
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
        if lead.status.name == 'Closed':
                project = Project.objects.create(

                    key=key,
                    lead_title = lead.lead_title,
                    lead_description = lead.lead_description,
                    contact_person_name = lead.contact_person_name,
                    contact_person_phone = lead.contact_person_phone,
                    contact_person_designation = lead.contact_person_designation,
                    business_name = lead.business_name,
                    state = lead.state,
                    district = lead.district,
                    city = lead.city,
                    business_address = lead.business_address,
                    interest_rate =lead.interest_rate,
                    lead_generated_date = lead.lead_generated_date,
                    next_follow_up_date = lead.next_follow_up_date,
                    min_price = lead.min_price,
                    max_price = lead.max_price,
                    lead_category = lead.lead_category,
                    lead_delivery_date = lead.lead_delivery_date,
                    lead = lead
                )
                for i in lead.added_by.all():
                    project.added_by.add(i)
                project.save()
        lead.save()
        lead_edit.delete()
    return redirect('Crm_App:lead_change_request')



def lead_edit(request,id):
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
    lead = Leads.objects.filter(id=id).first()
    form = LeadEditForm(request.POST or None, instance=lead)
    if form.is_valid():
        data = form.save(commit=False)
        print('helloo',type(data.status))
        if data.status.name == 'Closed':
                project = Project.objects.create(
                    # added_by = data.added_by,
                    key = key,
                    lead_title = data.lead_title,
                    lead_description = data.lead_description,
                    contact_person_name = data.contact_person_name,
                    contact_person_phone = data.contact_person_phone,
                    contact_person_designation = data.contact_person_designation,
                    business_name = data.business_name,
                    state = data.state,
                    district = data.district,
                    city = data.city,
                    business_address = data.business_address,
                    interest_rate =data.interest_rate,
                    lead_generated_date = data.lead_generated_date,
                    next_follow_up_date = data.next_follow_up_date,
                    min_price = data.min_price,
                    max_price = data.max_price,
                    lead_category = data.lead_category,
                    lead_delivery_date = data.lead_delivery_date,
                    lead = data
                )
                for i in data.added_by.all():
                    project.added_by.add(i)
                project.save()
                
        data.save()
        return redirect('Crm_App:lead_add')
    else:
        # Check if the lead status is closed and disable form fields
        if lead.status.name == 'Closed':
            for field in form.fields.values():
                field.disabled = True
        
    
    context = {
        'form':form
    }
    return render(request,'lead-edit.html',context)









def lead_change_request_edit(request,id):
    qs = TempLead.objects.filter(id=id).first()
    lead = qs.lead
    form = LeadAddForm(request.POST or None, instance=lead)
    if form.is_valid():
        form.save()
        return redirect('Crm_App:lead_change_request')
    
    context = {
        'form':form
    }
    return render(request,'lead-change-request-edit.html',context)

    




def lead_delete(request,id):
    qs = Leads.objects.get(id=id)
    qs.delete()
    messages.success(request,'Deleted')
    return redirect('Crm_App:lead_add')



def project_edit(request,project_id):

    
    return render(request,'project-edit.html')



def project_view(request,id):

    project = Project.objects.get(id=id)
    form = ProjectViewForm(instance=project)
   
    return render(request,'project-view.html',{"form":form})












def follow_up_reminder(request):
    current_date = datetime.datetime.today().date()
    tmw_count = current_date +  datetime.timedelta(days=1)
    after3days_count = current_date + datetime.timedelta(days=2)
    after7days_count = current_date + datetime.timedelta(days=6)
    today_followup = Leads.objects.filter(next_follow_up_date__contains = current_date)
    tommorrow_followup = Leads.objects.filter(next_follow_up_date = tmw_count)
    after3days = Leads.objects.filter(next_follow_up_date = after3days_count)
    after7days = Leads.objects.filter(next_follow_up_date = after7days_count)
    context = {
        'today_followup':today_followup,
        'tommorrow_followup' :tommorrow_followup,
        'after3days':after3days,
        'after7days':after7days,

    }
    return render(request,'follow-up-reminder.html',context)


def module_add(request,id):
    project = Project.objects.get(id=id)
    lead = project.lead
    print(lead)
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
    form = ProjectModuleForm()
    if request.method == 'POST':
        form = ProjectModuleForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.key = key
            data.project = project
            data.lead = lead
            if request.user.is_superuser:
                data.added_by_admin = request.user
            else:
                data.added_by = ExtendedUserModel.objects.get(user__username=request.user.username) 
            data.save()

        return redirect(reverse('Crm_App:module_add', args=[id]))

    
    form = ProjectModuleForm()

    all_module = ProjectModule.objects.filter(project = project )
    context = {
        'form':form,
        'all_module':all_module
    }
    return render(request,'module.html',context)




def module_delete(request, id):
    try:
        module = ProjectModule.objects.get(id=id)
        project_id = module.project_id
        module.delete()
        # messages.success(request, 'Deleted..')
        return redirect(reverse('Crm_App:module_add', args=[project_id]))
    except ObjectDoesNotExist:
        messages.error(request, 'Project module not found.')
        return redirect('Crm_App:module_add')



def project_assignment(request, id):
    
    
    branch = []
    name = request.user.username
    project = Project.objects.get(id=id)
    lead = project.lead
    instance = ProjectAssignment.objects.filter(project=project).first()
    added_by_users = project.added_by.all()  # Accessing the ManyToManyField
    user_names = [user.user.username for user in added_by_users]   
    for user_name in user_names:
        user = ExtendedUserModel.objects.get(user__username=user_name)
        branch.append(user.branch)

    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()

    if request.method == 'POST':
        form = ProjectAsignmentForm(request.POST, project=project, branch=branch,instance=instance,request=request)
        if form.is_valid():
            data = form.save(commit=False)
            data.key = key
            data.project = project
            data.lead = lead
            if request.user.is_superuser:
                data.added_by_admin = request.user
            else:
                data.added_by = ExtendedUserModel.objects.get(user__username=name)
            data.save()
            form.save_m2m()
            return redirect('Crm_App:project_management')
    else:
        # if request.user.is_superuser:
        #     form = ProjectAsignmentForm(project=project, instance=instance, branch=branch, request=request)
        # else:
        form = ProjectAsignmentForm(project=project, instance=instance, branch=branch,request=request)

    context = {
        'form': form,
        'project': project,
       
    }

   
    return render(request, 'project-asignment.html', context)

def get_assign_globally(request):
    selected_branches = request.GET.getlist('selected_branches[]')
    assign_globaly = ExtendedUserModel.objects.filter(branch__in=selected_branches, employee_type='Global').exclude(branch=request.user.user.branch)
    html = render_to_string('assign-globally-options.html', {'assign_globaly': assign_globaly})
    return HttpResponse(html)


def lead_help_centre(request):
    
    k = str(time.time()).encode('utf-8')
    h = blake2b(key=k, digest_size=10)
    key = h.hexdigest()
    leads = Leads.objects.filter(added_by__user=request.user)
    # leads = Leads.objects.all()
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






def placemanagement(request):
    state = State.objects.all()
    district = District.objects.all()
    city = City.objects.all()
    
    context ={
        'state':state,
        'district':district,
        'city':city,
    }
    return render(request,'place-management.html',context)


def state_add(request):
    State.objects.create(name=request.POST.get('state')).save()
    messages.success(request,'Succesfully Added')
    return redirect('Crm_App:placemanagement')

def state_update(request,state_id):
    updte = State.objects.filter(id = state_id).first()
    print(updte.name)
    if request.method == 'POST':
        updte.name = request.POST.get('name')
        updte.save()
        messages.success(request,'Updated..')
        return redirect('Crm_App:placemanagement')
    return render(request,'state-update.html',{'updte':updte})


def state_delete(request,state_id):
    dlt = State.objects.filter(id=state_id)
    dlt.delete()
    messages.success(request,'Deleted..')
    return redirect('Crm_App:placemanagement')


def district_add(request):
    state_name = request.POST.get('state')
    state = State.objects.get(name=state_name)
    District.objects.create(state = state,name=request.POST.get('district')).save()
    messages.success(request,'Succesfully Added')
    return redirect('Crm_App:placemanagement')


def district_update(request,district_id):
    state = State.objects.all()
    updte = District.objects.filter(id = district_id).first()
    if request.method == 'POST':
        state_name = request.POST.get('state')
        state = State.objects.get(name=state_name)
        updte.name = request.POST.get('name')
        updte.state = state
        updte.save()
        messages.success(request,'Updated..')
        return redirect('Crm_App:placemanagement')
    return render(request,'district-update.html',{'updte':updte,'state':state})


def district_delete(request,district_id):
    dlt = District.objects.filter(id=district_id)
    dlt.delete()
    messages.success(request,'Deleted..')
    return redirect('Crm_App:placemanagement')

def city_add(request):
    district_name = request.POST.get('district')
    district = District.objects.get(name=district_name)
    City.objects.create(district = district,name=request.POST.get('city')).save()
    messages.success(request,'Succesfully Added')
    return redirect('Crm_App:placemanagement')



def city_update(request,city_id):
    district = District.objects.all()
    updte = City.objects.filter(id = city_id).first()
    if request.method == 'POST':
        district_name = request.POST.get('district')
        district = District.objects.get(name=district_name)
        updte.name = request.POST.get('name')
        updte.district = district
        updte.save()
        messages.success(request,'Updated..')
        return redirect('Crm_App:placemanagement')
    return render(request,'city-update.html',{'updte':updte,'district':district})



def city_delete(request,city_id):
    dlt = City.objects.filter(id=city_id)
    dlt.delete()
    messages.success(request,'Deleted..')
    return redirect('Crm_App:placemanagement')



def usertype_settings(request):
    usertype = Usertype.objects.all()
    if request.method == 'POST':
        Usertype.objects.create(name=request.POST.get('type')).save()
        messages.success(request,'Created..')
    return render(request,'usertype-management.html',{'usertype':usertype})


def usertype_update(request,user_id):
    update = Usertype.objects.filter(id=user_id).first()
    if request.method == 'POST':
        update.name = request.POST.get('name')
        update.save()
        messages.success(request,'Created..')
        return redirect('Crm_App:usertype_settings')
    return render(request,'usertype-update.html',{'update':update})


def usertype_delete(request,user_id):
    dlt = Usertype.objects.filter(id=user_id)
    dlt.delete()
    messages.success(request,'Deleted')
    return redirect('Crm_App:usertype_settings')






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
    message = f'Hi, Click the link to verify your account http://192.168.1.10:8989/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email ,]
    send_mail(subject ,message,email_from, recipient_list)




def project_management(request):
    # if request.user.is_superuser:
    projects = Project.objects.all()
    module_count = ProjectModule.objects.all().count()
    # elif request.user.extendedusermodel.usertype=='Admin':
    #     added_by = ExtendedUserModel.objects.flter(user__username=request.user.username)
    #     print(added_by)
    #     projects = Project.objects.filter()

    return render(request,'project.html',{'projects':projects,'module_count':module_count})




def project_delete(request,project_id):
    dlt = Project.objects.filter(id=project_id)
    dlt.delete()
    messages.success(request,'Deleted..')
    return redirect('Crm_App:project_management')







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
                # MESSAGE SENDING CODE
                # template = render_to_string('admin-register-email.html',{'emp_name':username})
                # email = EmailMessage(
                #     'Account Registration', #subject
                #     template, #body
                #     settings.EMAIL_HOST_USER, #sender mail id
                #     [email] #recever mail id
                # )
                # email.fail_silently = False
                # email.send()
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
        print(password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            request.session['username'] = username
            auth.login(request,user)
            print('logged in')
            return JsonResponse(
                {'success':True},
                safe=False
            )
        else:
            auth.login
            return JsonResponse(
                {'success':False},
                safe=False
            )
    else:
        return render(request,'login.html')





def logout(request):
    if 'username' in request.session:
        request.session.flush();
    return redirect("Crm_App:login")



