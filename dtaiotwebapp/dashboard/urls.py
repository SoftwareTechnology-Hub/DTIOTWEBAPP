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
    path('api/feed_data', views.Feed_data, name='Feed_data'),
    path("feed/json/<slug:slug>/", views.feed_data_json, name="feed_data_json"),
    # dashboard/urls.py
    # path("feed/json/<slug:slug>/", views.feed_json, name="feed_json"),
# dashboard/urls.py
    path('widget/edit/<int:widget_id>/', views.edit_widget, name='edit_widget'),
    path('widget/delete/<int:widget_id>/', views.delete_widget, name='delete_widget'),
    path('api/data', views.dashboard_data, name='dashboard_data'),

    path("dashboard/data/<slug:slug>/", views.dashboard_data_json, name="dashboard_data_json"),



]
