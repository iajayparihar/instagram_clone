from django.urls import path
from post import views

urlpatterns = [
    path('',views.index, name = "index"),
    path('upload/',views.upload, name = "upload"),
    path('chat/',views.chat, name = "chat"),
    path('profile/',views.profile, name = "profile"),
    path('reels/',views.reels, name = "reels"),
]
