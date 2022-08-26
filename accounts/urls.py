from django.urls import path
from django.contrib import messages

from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('login/', views.login, name='login_url'),
    path('register', views.register_view, name='register'),
    path("logout", LogoutView.as_view(next_page='index_view_url'), name="logout"),
    path("edit", views.edit_profile, name="edit"),
    path('dashboard', views.dashboard, name='dashboard')
]
# path('logout', views.logout, name='logout'),
