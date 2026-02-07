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
            Custom_Dashboard.objects.create(user=request.user, title=title, description=description)
        return redirect('custom_dashboard')

    return render(request, 'dashboard/custom_dashboard.html', {'dashboards': dashboards})

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Custom_Dashboard

@login_required
def view_dashboard(request, slug):
    dashboard = get_object_or_404(
        Custom_Dashboard,
        slug=slug,
        user=request.user
    )
    return render(request, 'dashboard/view_dashboard.html', {
        'dashboard': dashboard
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
            Custom_Feed.objects.create(
                user=request.user,
                title=title,
                content=content
            )
        return redirect('custom_feed')

    return render(request, 'dashboard/custom_feed.html', {
        'feeds': feeds
    })


@login_required
def view_feed(request, slug):
    feed = get_object_or_404(
        Custom_Feed,
        slug=slug,
        user=request.user
    )
    return render(request, 'dashboard/view_feed.html', {
        'feed': feed
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
