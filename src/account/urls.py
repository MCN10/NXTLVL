from django.urls import path

from . import views

app_name = "account"


urlpatterns = [
    #Leave as empty string for base url
	path('', views.account_view, name="profile"),
	path('edit/', views.account_edit, name="edit"),
	path('register/', views.registration_view, name="register"),
	path('logout/', views.logout_view, name="logout"),
	path('login/', views.login_view, name="login"),
    ]
