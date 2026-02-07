from django.urls import path
from . import views   # THIS is correct! use relative import

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('custom/', views.custom_dashboard, name='custom_dashboard'),
    path('custom/<slug:slug>/', views.view_dashboard, name='view_dashboard'),
    path('custom/edit/<int:dashboard_id>/', views.edit_dashboard, name='edit_dashboard'),
    path('custom/delete/<int:dashboard_id>/', views.delete_dashboard, name='delete_dashboard'),
    path('feed/', views.custom_feed, name='custom_feed'),
    path('feed/<slug:slug>/', views.view_feed, name='view_feed'),
    path('feed/edit/<int:feed_id>/', views.edit_feed, name='edit_feed'),
    path('feed/delete/<int:feed_id>/', views.delete_feed, name='delete_feed'),    
    # path('profile/', views.profile, name='profile'),    # Profile page
]
