from email import message
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from myproject import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from . import views

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname') #you can also write it as request.POST['fname']
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if User.objects.filter(username = username).exists():
            messages.error(request,"Username already exists")
            return redirect('signup')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')
        
        if len(username)>10:
            messages.errot(request, "Username must be under 10 characters")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username is not Alpha numeric!")
                    
        if(pass1 != pass2):
            message.error(request,"Passwords do not match")
            return redirect('signup')
                    
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        
        myuser.save()
        
        messages.success(request, "Your account has been successfully created.\n")
        
        return redirect('signin')
        
        
    return render(request, 'authentication/signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']
        
        user = authenticate(username = username, password = password,)
        
        if user is not None:
            login(request, user) 
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname':fname})
            
        else:
            messages.error(request, " Bad Credentials")
            return redirect('home')
    
    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

