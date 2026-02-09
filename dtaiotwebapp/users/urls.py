from django.urls import path
from .views import signup, login_view
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('regenerate-api/', views.regenerate_api_key, name='regenerate_api'),
    path('logout/', views.user_logout, name='logout'),
    path('notifications/', views.notifications, name='notifications'),

]
