from django.db import models
from django.utils.text import slugify

class Custom_Dashboard(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Custom_Dashboard.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
from django.db import models
from django.utils.text import slugify

class Custom_Feed(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Custom_Feed.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# models.py
class FeedData(models.Model):
    feed = models.ForeignKey(Custom_Feed, on_delete=models.CASCADE)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feed.slug} = {self.value}"
# dashboard/models.py
class DashboardWidget(models.Model):
    dashboard = models.ForeignKey(
        Custom_Dashboard,
        on_delete=models.CASCADE,
        related_name="widgets"
    )

    name = models.CharField(max_length=100)
    widget_type = models.CharField(
        max_length=20,
        choices=[
            ('line', 'Line Chart'),
            ('bar', 'Bar Chart'),
            ('gauge', 'Gauge'),
            ('text', 'Text')
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dashboard', 'name')  # ✅ VERY IMPORTANT

    def __str__(self):
        return f"{self.dashboard.title} → {self.name}"
class WidgetData(models.Model):
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)