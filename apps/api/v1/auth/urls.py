from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.api.v1.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='auth-login'),
    path('register/', views.UserRegisterView.as_view(), name='auth-register'),
    path('refresh/token/', TokenRefreshView.as_view(), name="auth-refresh-token"),
    path('logout/', views.LogoutView.as_view(), name="auth-logout"),
]
