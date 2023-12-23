from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    return render(request,'index.html')

def upload(request):
    return render(request,'upload/upload.html')

def chat(request):
    return render(request,'chat/chat.html')

def profile(request):
    return render(request,"profile/profile.html")

def reels(request):
    return render(request,'reels/reels.html')

#here we can save over file to database / redirect to same page again
def file_upload(request):
    return render(request,"upload/upload.html")