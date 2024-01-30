from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.http import HttpResponseRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.urls import reverse
#this fun is not used yet
@login_required
def follow_friendship(request,receiver):
    rec = User.objects.get(username=receiver)

    if Friendship.objects.filter(sender=request.user,receiver=rec).count() == 0 :
        sen_F = Friendship.objects.create(sender=request.user,receiver=rec)
        sen_F.save()
    return redirect('/enter')
    
@login_required
def index(request):
    user = request.user
    all_profile = Profile.objects.all()
    prof = Profile.objects.get(user=user)

    # showing post in index page
    all_post = Post.objects.all()
    for post in all_post:
        post.liked_by_user = Like.objects.filter(user=user, post=post).exists()

    all_cmt = Comment.objects.all()    

    return render(request,'index.html',{'profile': prof,'all_profile':all_profile,'all_posts':all_post,'cmt':all_cmt})


@login_required
def like(request, post_id):
    cur_user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Like.objects.filter(user=cur_user,post=post).count()
    
    # Check if the user has already liked the post
    if not liked:
        # If not, create a new Like object and increment the likes count
        l = Like.objects.create(user=cur_user, post=post)
        l.save()
        post.likes += 1
        post.save()

    return redirect('index')


@login_required
def unlike(request, post_id):
    cur_user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    like = Like.objects.filter(user=cur_user,post=post)
    liked = like.count()
    
    # Check if the user has already liked the post
    if liked:
        # If yes, delete the Like object and decrement the likes count
        like.delete()
        post.likes -= 1
        post.save()

    return redirect('index')



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
        #other user prof
        new_user_prof = get_object_or_404(Profile, user=new_user_id)
        new_user_post = Post.objects.filter(user=new_user_id)
        no_of_post = len(new_user_post)
        # cur user prof
        cur_profile = Profile.objects.get(user=request.user)
        nav_profile_image = cur_profile.profile_image
        
        # Use get_object_or_404 to handle the case when the profile does not exist
        user_profile = get_object_or_404(Profile, user=user)

        # Retrieve followers and following for the user
        user_followers = len(user_profile.followed_by.all())
        user_following = len(user_profile.follows.all())

        # follow unfollow 
        cur_user_follows = cur_profile.follows.all()
        if (new_user_prof in cur_user_follows):
            follow_button_value = "unfollow"
        else:
            follow_button_value = "follow"


        return render(request, "profile/profile.html", {'profile': new_user_prof, 'allpost': new_user_post, 'post_count': no_of_post,'user':user,'nav_profile':nav_profile_image,'user_followers': user_followers,
        'user_following': user_following,"follow_button_value":follow_button_value})

@login_required
def profile(request):
    cur_user = request.user
    user = User.objects.get(username=cur_user)
    allProfile_details = Profile.objects.get(user=cur_user)
    cur_user_post = Post.objects.filter(user=cur_user)
    post_count = cur_user_post.count()

    nav_profile = Profile.objects.get(user=request.user)
    nav_profile_image = nav_profile.profile_image

    cur = request.user
    
    # Use get_object_or_404 to handle the case when the profile does not exist
    user_profile = get_object_or_404(Profile, user=cur)

    # Retrieve followers and following for the user
    user_followers = len(user_profile.followed_by.all())
    user_following = len(user_profile.follows.all())

    return render(request, "profile/profile.html", {
        'profile': allProfile_details,
        'allpost': cur_user_post,
        'post_count': post_count,
        'user': user,
        'nav_profile': nav_profile_image,
        'user_followers': user_followers,
        'user_following': user_following,
    })

def followers_count(request):
    if request.method == "POST":
        value = request.POST.get('value')
        user = request.POST.get('user')
        follower = request.POST.get('follower')

        sender = User.objects.get(username=user)
        receiver = User.objects.get(username=follower)

        sender_profile = Profile.objects.get(user=sender)
        receiver_profile = Profile.objects.get(user=receiver)

        if value == "follow":
            # Add the follower to the follows field of the sender's profile
            sender_profile.follows.add(receiver_profile)
        else:
            # For unfollow, remove the follower from the follows field of the sender's profile
            sender_profile.follows.remove(receiver_profile)

        other_user_id = User.objects.get(username=follower)
        other_user_id = other_user_id.id

        return redirect(f'/enter/other_user/?other_user={str(other_user_id)}')

    # Handle the case when the method is not POST
    # You might want to add additional logic or redirect to an appropriate page
    return redirect('/enter')

def reels(request):
    return render(request,'reels/reels.html')

#here we can save over file to database / redirect to same page again
def file_upload(request):
    return render(request,"upload/upload.html")




def comment(request,post_id):
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(id=post_id)
        # cmt from index 
        cmt = request.POST.get('user_cmt')
        
        mod_cmt = Comment.objects.create(user=user,post=post,text=cmt)
        mod_cmt.save()


    return HttpResponseRedirect(reverse(index))