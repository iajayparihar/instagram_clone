from django.urls import path
from post import views


urlpatterns = [
    path('',views.index, name = "index"),
    path('upload/',views.upload, name = "upload"),
    path('chat/',views.chat, name = "chat"),
    path('profile/',views.profile, name = "profile"),
    path('reels/',views.reels, name = "reels"),
    path('file_upload/',views.file_upload, name = "file_upload"),
    path('follow_friendship/<str:receiver>/',views.follow_friendship,name = 'follow_friendship'),
    path('followers_count/',views.followers_count,name='followers_count'),
    path('other_user/',views.other_user,name='other_user'),
]
