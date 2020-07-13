from django.urls import path
from TestApp import views

urlpatterns = [
    path('login',views.LoginAPI.as_view()),
    path('profile',views.ProfileAPI.as_view()),
    path('logout',views.LogoutAPI.as_view()),
]
