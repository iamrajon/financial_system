from django.urls import path, include
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', views.UserRegisterView.as_view(), name="user-signup"),
    path('login/', views.UserLoginView.as_view(), name="user-login"),
    path('logout/', views.UserLogoutView.as_view(), name="user-logout"),
    path('profile/', views.UserProfileView.as_view(), name="user-profile"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
]