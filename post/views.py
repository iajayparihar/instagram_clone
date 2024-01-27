from django.shortcuts import render,redirect, get_object_or_404
from .models import Post,Comment,User,Profile,Friendship

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def follow_friendship(request,receiver):
    rec = User.objects.get(username=receiver)

    if Friendship.objects.filter(sender=request.user,receiver=rec).count() == 0 :
        sen_F = Friendship.objects.create(sender=request.user,receiver=rec)
        sen_F.save()
    return redirect('/enter')
    
@login_required
def index(request):
    cur_user = request.user
    all_profile = Profile.objects.all()

    # friends = Friendship.objects.all()
    # <QuerySet [<Friendship: ajay123, pending>, <Friendship: ajay123, pending>]>
    # ajay123 vij
    # for i in range(len(friends)):
    #     if friends[i].sender == request.user and 
    # print("/////////////////////////////////////////////////////////",friends[0].sender,friends[0].receiver)

    prof = Profile.objects.get(user=cur_user)

    return render(request,'index.html',{'profile': prof,'all_profile':all_profile})
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


def other_user(request):
    if request.method == "GET":
        new_user_id = int(request.GET.get('other_user'))
        user = User.objects.get(id=new_user_id)
        new_user_prof = get_object_or_404(Profile, user=new_user_id)
        new_user_post = Post.objects.filter(user=new_user_id)
        no_of_post = len(new_user_post)
        
        nav_profile = Profile.objects.get(user=request.user)
        nav_profile_image = nav_profile.profile_image
        
        return render(request, "profile/profile.html", {'profile': new_user_prof, 'allpost': new_user_post, 'post_count': no_of_post,'user':user,'nav_profile':nav_profile_image})

def profile(request):
    cur_user = request.user
    user = User.objects.get(username=cur_user)
    allProfile_details = Profile.objects.get(user=cur_user)
    cur_user_post = Post.objects.filter(user=cur_user)
    post_count = cur_user_post.count()

    nav_profile = Profile.objects.get(user=request.user)
    nav_profile_image = nav_profile.profile_image

    return render(request,"profile/profile.html", {'profile': allProfile_details, 'allpost': cur_user_post, 'post_count': post_count,"user":user,'nav_profile':nav_profile_image})

def followers_count(request):
    if request.method == "POST":
        value = request.POST.get('value')
        user = request.POST.get('user')
        follower = request.POST.get('follower')
        print("0000000000000000000000000000000000000",value,user,follower)

        sender = User.objects.get(username=user)
        receiver = User.objects.get(username=follower)
        if value == "follow":
            fri = Friendship.objects.create(sender=sender,receiver=receiver)
            fri.save()
        else:
            #for unfollow
            fri = Friendship.objects.filter(sender=sender,receiver=receiver)
            fri.delete()
        other_user_id = User.objects.get(username=follower)
        other_user_id = other_user_id.id

    return redirect(f'/enter/other_user/?other_user={str(other_user_id)}')


def reels(request):
    return render(request,'reels/reels.html')

#here we can save over file to database / redirect to same page again
def file_upload(request):
    return render(request,"upload/upload.html")
