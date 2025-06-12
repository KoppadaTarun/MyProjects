from rest_framework.urls import path
from .views import register_view, login_view, logout_view
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('refresh/access/token/', TokenRefreshView.as_view(), name='access_token')
]