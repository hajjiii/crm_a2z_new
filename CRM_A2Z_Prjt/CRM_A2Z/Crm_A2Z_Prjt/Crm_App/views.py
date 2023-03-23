from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http.response import JsonResponse
from Crm_App.models import Branch,Usertype,ExtendedUserModel
import uuid
from django.conf import settings
from django.core.mail import send_mail
from .forms import *



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


# def lead_add(request):
#     form = LeadAddForm()
#     if request.method == 'POST':
#         FORM =







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


    