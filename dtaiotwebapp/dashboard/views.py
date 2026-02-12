from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, 'dashboard/index1.html')
# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Custom_Dashboard

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Custom_Dashboard

@login_required
def custom_dashboard(request):
    dashboards = Custom_Dashboard.objects.filter(user=request.user)

    if request.method == 'POST' and 'create_dashboard' in request.POST:
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title:
            # Check if dashboard with same title already exists for this user
            exists = Custom_Dashboard.objects.filter(user=request.user, title=title).exists()
            if exists:
                # You can return a message instead of creating
                return render(request, 'dashboard/custom_dashboard.html', {
                    'dashboards': dashboards,
                    'error': f"A dashboard with the title '{title}' already exists."
                })

            # Create if not exists
            Custom_Dashboard.objects.create(user=request.user, title=title, description=description)
            return redirect('custom_dashboard')

    return render(request, 'dashboard/custom_dashboard.html', {'dashboards': dashboards})

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Custom_Dashboard, DashboardWidget, WidgetData

# dashboard/views.py
@login_required
def view_dashboard(request, slug):
    dashboard = get_object_or_404(
        Custom_Dashboard,
        slug=slug,
        user=request.user
    )

    # CREATE WIDGET
    if request.method == "POST":
        name = request.POST.get("name")
        widget_type = request.POST.get("widget_type")

        if name and widget_type:
            # ✅ Check if widget with same name exists in this dashboard
            exists = DashboardWidget.objects.filter(dashboard=dashboard, name=name).exists()
            if exists:
                # Optional: show error in template
                widgets = dashboard.widgets.all()
                return render(request, 'dashboard/view_dashboard.html', {
                    'dashboard': dashboard,
                    'widgets': widgets,
                    'error': f"A widget with the name '{name}' already exists in this dashboard."
                })

            # Create new widget if not exists
            DashboardWidget.objects.create(
                dashboard=dashboard,
                name=name,
                widget_type=widget_type
            )
            return redirect('view_dashboard', slug=dashboard.slug)

    widgets = dashboard.widgets.all()

    return render(request, 'dashboard/view_dashboard.html', {
        'dashboard': dashboard,
        'widgets': widgets
    })

from django.utils.text import slugify

@login_required
def edit_dashboard(request, dashboard_id):
    dash = get_object_or_404(Custom_Dashboard, id=dashboard_id, user=request.user)

    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_description = request.POST.get('description')

        if new_title and new_title != dash.title:
            base_slug = slugify(new_title)
            slug = base_slug
            counter = 1
            while Custom_Dashboard.objects.filter(slug=slug).exclude(id=dash.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            dash.title = new_title
            dash.slug = slug

        dash.description = new_description
        dash.save()

    return redirect('custom_dashboard')


@login_required
def delete_dashboard(request, dashboard_id):
    dash = get_object_or_404(Custom_Dashboard, id=dashboard_id, user=request.user)
    dash.delete()
    return redirect('custom_dashboard')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Custom_Feed


@login_required
def custom_feed(request):
    feeds = Custom_Feed.objects.filter(user=request.user)

    # CREATE FEED
    if request.method == 'POST' and 'create_feed' in request.POST:
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title:
            # Check if feed with the same title already exists for this user
            exists = Custom_Feed.objects.filter(user=request.user, title=title).exists()
            if exists:
                return render(request, 'dashboard/custom_feed.html', {
                    'feeds': feeds,
                    'error': f"A feed with the title '{title}' already exists."
                })

            # Create if not exists
            Custom_Feed.objects.create(
                user=request.user,
                title=title,
                content=content
            )
        return redirect('custom_feed')

    return render(request, 'dashboard/custom_feed.html', {
        'feeds': feeds
    })


from .models import FeedData

@login_required
def view_feed(request, slug):
    feed = get_object_or_404(Custom_Feed, slug=slug, user=request.user)

    records = FeedData.objects.filter(feed=feed).order_by('created_at')[:100]

    labels = [r.created_at.strftime('%H:%M:%S') for r in records]
    values = [r.value for r in records]

    return render(request, 'dashboard/view_feed.html', {
        'feed': feed,
        'labels': labels,
        'values': values,
    })



@login_required
def edit_feed(request, feed_id):
    feed = get_object_or_404(
        Custom_Feed,
        id=feed_id,
        user=request.user
    )

    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')

        if new_title and new_title != feed.title:
            base_slug = slugify(new_title)
            slug = base_slug
            counter = 1

            while Custom_Feed.objects.filter(slug=slug).exclude(id=feed.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            feed.slug = slug
            feed.title = new_title

        feed.content = new_content
        feed.save()

        return redirect('custom_feed')


@login_required
def delete_feed(request, feed_id):
    feed = get_object_or_404(Custom_Feed, id=feed_id, user=request.user)
    feed.delete()
    return redirect('custom_feed')
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from users.models import CustomUser
from .models import Custom_Feed, FeedData
@csrf_exempt
def Feed_data(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    api_key = data.get("api_key")
    feed_name = data.get("feed_name")
    value = data.get("value")

    if not all([api_key, feed_name]):
        return JsonResponse({"error": "Missing fields"}, status=400)


    # # user from api key
    # try:
    #     user = CustomUser.objects.get(api_key=api_key)
    # except CustomUser.DoesNotExist:
    #     return JsonResponse({"error": "Invalid API key"}, status=403)

    # # feed from user
    # try:
    #     feed = Custom_Feed.objects.get(user=user, slug=feed_name)
    # except Custom_Feed.DoesNotExist:
    #     return JsonResponse({"error": "Feed not found"}, status=404)

    try:
        user = CustomUser.objects.get(api_key=api_key)
        feed = Custom_Feed.objects.get(user=user, title__iexact=feed_name)
    except (CustomUser.DoesNotExist, Custom_Feed.DoesNotExist):
        return JsonResponse({"error": "Authentication failed"}, status=401)

    # ✅ FEED MATCH BY TITLE (industry standard)
    # try:
    #     feed = Custom_Feed.objects.get(user=user, title__iexact=feed_name)
    # except Custom_Feed.DoesNotExist:
    #     return JsonResponse({"error": "Feed not found"}, status=404)

    if value is None:
        return JsonResponse({"error": "Value required"}, status=400)
    try:
        value = float(value)  # convert to numeric
    except (ValueError, TypeError):
        return JsonResponse({"error": "Value Type Error"}, status=400)

    # save data
    FeedData.objects.create(feed=feed, value=value)

    # keep only latest 5
    old_ids = (
        FeedData.objects
        .filter(feed=feed)
        .order_by('-created_at')
        .values_list('id', flat=True)[10:]
    )
    FeedData.objects.filter(id__in=list(old_ids)).delete()

    return JsonResponse({"message": "Data saved"})
@login_required
def feed_data_json(request, slug):
    feed = get_object_or_404(Custom_Feed, slug=slug, user=request.user)
    data = FeedData.objects.filter(feed=feed).order_by('created_at')
    
    return JsonResponse({
        "values": [d.value for d in data],
        "labels": [d.created_at.isoformat() for d in data]  # Send ISO format timestamps
    })
# dashboard/views.py
from .models import DashboardWidget

@login_required
def edit_widget(request, widget_id):
    widget = get_object_or_404(
        DashboardWidget,
        id=widget_id,
        dashboard__user=request.user
    )

    if request.method == "POST":
        widget.name = request.POST.get("name")
        widget.widget_type = request.POST.get("widget_type")
        widget.save()

    return redirect('view_dashboard', slug=widget.dashboard.slug)


@login_required
def delete_widget(request, widget_id):
    widget = get_object_or_404(
        DashboardWidget,
        id=widget_id,
        dashboard__user=request.user
    )

    dashboard_slug = widget.dashboard.slug
    widget.delete()

    return redirect('view_dashboard', slug=dashboard_slug)
@login_required
def dashboard_data_json(request, slug):
    dashboard = get_object_or_404(
        Custom_Dashboard, slug=slug, user=request.user
    )

    result = []


    for widget in dashboard.widgets.all():
        records = WidgetData.objects.filter(widget=widget).order_by("created_at")[:20]


        result.append({
            "widget": widget.name,
            "type": widget.widget_type,
            "labels": [r.created_at.isoformat() for r in records],  # Send ISO format timestamps
            "values": [r.value for r in records]
        })
    return JsonResponse(result, safe=False)
    


@csrf_exempt
def dashboard_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    api_key = data.get("api_key")
    dashboard_name = data.get("dashboard")   # TITLE sent by device
    widget_name = data.get("widget")
    value = data.get("value")

    if not all([api_key, dashboard_name, widget_name]):
        return JsonResponse({"error": "Missing fields"}, status=400)

    # USER
    try:
        user = CustomUser.objects.get(api_key=api_key)

        dashboard = Custom_Dashboard.objects.get(
            user=user,
            title__iexact=dashboard_name
        )

        widget = DashboardWidget.objects.get(
            dashboard=dashboard,
            name__iexact=widget_name
        )
    except (CustomUser.DoesNotExist,
        Custom_Dashboard.DoesNotExist,
        DashboardWidget.DoesNotExist):
        return JsonResponse({"error": "Authentication failed"}, status=401)

    # DASHBOARD
    # try:
    #     dashboard = Custom_Dashboard.objects.get(
    #         user=user,
    #         title__iexact=dashboard_name
    #     )

    #     widget = DashboardWidget.objects.get(
    #         dashboard=dashboard,
    #         name__iexact=widget_name
    #     )
    # except Custom_Dashboard.DoesNotExist:
    #     return JsonResponse({"error": "Authentication failed"}, status=401)

    # # WIDGET
    # try:
    #     widget = DashboardWidget.objects.get(
    #         dashboard=dashboard,
    #         name__iexact=widget_name
    #     )
    # except DashboardWidget.DoesNotExist:
    #     return JsonResponse({"error": "Widget not found"}, status=404)
    
    if value is None:
        return JsonResponse({"error": "Value required"}, status=400)
    try:
        value = float(value)  # convert to numeric
    except (ValueError, TypeError):
        return JsonResponse({"error": "Value Type Error"}, status=400)
    WidgetData.objects.create(widget=widget, value=value)

    old_ids = (
        WidgetData.objects
        .filter(widget=widget)
        .order_by('-created_at')
        .values_list('id', flat=True)[5:]
    )
    WidgetData.objects.filter(id__in=list(old_ids)).delete()

    return JsonResponse({"status": "success"})

    