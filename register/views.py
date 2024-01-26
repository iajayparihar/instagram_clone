from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
# from post.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from post.models import Profile
from .forms import ProfileForm
# login -> Session maintain
#authenticate -> password decription

#profile edit 
def register_profile(request):
    # ins = get_object_or_404(User, id=request.user.id)
    # print(ins)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user

            if user.is_authenticated:
                bio=form.cleaned_data.get('bio')
                link=form.cleaned_data.get('link')
                profile_image=form.cleaned_data.get('profile_image')
                if profile_image:
                    print('profile image available.................................................')

                temp = Profile.objects.get(user=user)
                print('user infor .............', temp)
                temp.user = user
                temp.bio = bio
                temp.link = link
                temp.profile_image = profile_image
                temp.save()

            return redirect('/enter/profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/profile_update.html', {'form': form})

# Create your views here.
def user_register(request):
    if request.method != 'POST':
        return render(request,'register/register.html')
        
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
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

    #---also save user profile when user is chreated---

    prof = Profile.objects.create(user=user)
    prof.save()

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


