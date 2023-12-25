from django.shortcuts import render,HttpResponseRedirect
from enroll.forms import SignUpForm,EditUserProfileForm,EditAadminProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User,Group
# Create your views here.
def sign_up(request):
    if request.method =="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            user=fm.save()
            group=Group.objects.get(name='editer')
            user.groups.add(group)

    else:
        fm=SignUpForm()
    return render(request,'enroll/signup.html',{'form':fm})

# login view Function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user= authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully!')
                    return HttpResponseRedirect('/profile/')
        else:
          fm=AuthenticationForm()        
        return render(request,'enroll/userlogin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser==True:
                fm=EditAadminProfileForm(request.POST,instance=request.user)
                users=User.objects.all()
            else:
                
                fm=EditUserProfileForm(request.POST,instance=request.user)
                
            
            if fm.is_valid():
              messages.success(request,'Profile updated')
              fm.save()
        else:
            if request.user.is_superuser == True:
                fm= EditAadminProfileForm(instance=request.user)
                users=User.objects.all()
            else:
                fm=EditUserProfileForm(instance=request.user)
                users=None
        return render(request,'enroll/dashbord.html',{'name':request.user.username,'form':fm,'users':users})
    else:
            return HttpResponseRedirect('/login/')
        
def user_details(request,id):
    if request.user.is_authenticated:
        pi=User.objects.get(pk=id)
        fm=EditAadminProfileForm(instance=pi)
        return render(request,'enroll/userdetails.html',{'form':fm})
    else:
        return  HttpResponseRedirect('/login/')


def user_dashbord(request):
    if request.user.is_authenticated:
        return render(request,'enroll/dashbord.html')
    else:
        return HttpResponseRedirect('/login/')




def user_logout(request):
        
    logout(request)
    return HttpResponseRedirect('/login/')


#change password with old password
def user_change_password(request):
    if request.user.is_authenticated:
            
        if request.method=="POST":
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                print('entered')
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,'Password Changed Successfully...')
                return HttpResponseRedirect('/profile/')
        else:
            fm=PasswordChangeForm(user=request.user)
        return render(request,'enroll/changepass.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')