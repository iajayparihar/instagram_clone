from django.urls import path
from Message import views


urlpatterns = [
    path('inbox/',views.inbox, name = "inbox"),
]
