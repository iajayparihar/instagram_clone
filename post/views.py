from django.shortcuts import render,redirect
from .models import Post,Comment,User,Profile

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    cur_user = request.user
    prof = Profile.objects.get(user=cur_user)
    return render(request,'index.html',{'profile': prof})
@login_required
def upload(request):
    
    if request.method == 'POST':
        upload_pic = request.FILES.get('pic') # FILES method is use for images or files
        upload_cap = request.POST.get('cap')

        if upload_pic and upload_cap:
            new_post = Post(user=request.user,caption=upload_cap,image=upload_pic)
            new_post.save()
            return redirect('/enter/profile/')
            
    return render(request,'upload/upload.html')

def chat(request):
    return render(request,'chat/chat.html')

def profile(request):
    cur_user = request.user
    cur_user_post = Post.objects.filter(user=cur_user)
    # when we have query set then we can iterate over the querty otherwise we can directly user fields
    allProfile_details = Profile.objects.get(user=cur_user)
    post_count = Post.objects.filter(user=cur_user).all().count()
    print('......................................',post_count)
    return render(request,"profile/profile.html",{'profile':allProfile_details, 'allpost': cur_user_post,'post_count':post_count})

def reels(request):
    return render(request,'reels/reels.html')

#here we can save over file to database / redirect to same page again
def file_upload(request):
    return render(request,"upload/upload.html")
