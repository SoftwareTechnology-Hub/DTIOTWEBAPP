from django.contrib import admin

# Register your models here.
from .models import Custom_Dashboard, Custom_Feed, FeedData, DashboardWidget, WidgetData

admin.site.register(Custom_Dashboard)
admin.site.register(Custom_Feed)
admin.site.register(FeedData)
admin.site.register(DashboardWidget)
admin.site.register(WidgetData)
