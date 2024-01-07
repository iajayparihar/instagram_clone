from django.shortcuts import render,redirect
from django.contrib import messages
# from post.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout

# login -> Session maintain
#authenticate -> password decription

# Create your views here.
def user_register(request):
    if request.method != 'POST':
        return render(request,'register/register.html')

    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = User.objects.filter(username=username)
    if user.exists():
        messages.error(request, "User already exists!!!")
        return redirect('/register/')

    user = User.objects.create(
    email = email,
    first_name = first_name,
    last_name = last_name,
    username = username,
    )
    user.set_password(password)
    user.save()
    messages.success(request, "Account created succesfully.")
    return redirect('/')


def user_login(request):
    if request.method != 'POST':
        return render(request,'register/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if not User.objects.filter(username=username).exists():
        messages.error(request, "User already exists!!!")
        return redirect('/')
    
    user = authenticate(username=username,password=password)
    if user is None:
        messages.error(request, "Invalid password or username")
        return redirect('/')
    else:
        login(request,user)
        return render(request,'index.html')

def user_logout(request):
    logout(request)
    return redirect('/')


