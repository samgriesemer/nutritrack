import cv2
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from nutritrack import predict
from nutritrack.forms import UploadFileForm


@login_required
def index(request):
    return render(request, 'nutritrack/index.html', {'user': request.user})


@ensure_csrf_cookie
def splash(request):
    return render(request, 'splash.html')


@login_required
def report(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['file']
            with open('/tmp/image' + image.name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            opencvImage = cv2.imread('/tmp/image' + image.name)
            pred = predict.client.predict_image(opencvImage)
            return render(request, 'nutritrack/form.html', {'form': pred})
    else:
        form = UploadFileForm()
    return render(request, 'nutritrack/form.html', {'form': form})


@login_required
def profile(request):
    return redirect('/nutritrack/')

