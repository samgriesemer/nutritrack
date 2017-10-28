from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
def index(request):
    return render(request, 'nutritrack/index.html')


@ensure_csrf_cookie
def splash(request):
    return render(request, 'splash.html')
