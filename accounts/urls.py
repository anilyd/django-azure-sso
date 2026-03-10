from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("azure-login/", views.azure_login, name="azure_login"),
    path("microsoft/login/callback/", views.azure_callback, name="azure_callback"),
    path("logout/", views.azure_logout, name="azure_logout"),
     path("home/", views.home, name="home"),  # ✅ Add this line
]