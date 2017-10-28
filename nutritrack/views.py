import cv2
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from nutritrack import predict
from nutritrack.forms import UploadFileForm
from nutritrack.models import MealReport, Nutrient, Ingredient, Meal


@login_required
def index(request):
    nut = Nutrient()
    nut.kcal = 0
    nut.fat = 0
    nut.carb = 0
    nut.sugar = 0
    nut.protein = 0
    nut.sodium = 0
    nut.vA = 0
    nut.vC = 0
    nut.iron = 0
    nut.calcium = 0
    mr = MealReport.objects.filter(user=request.user)
    for r in list(mr):
        for i in list(r.meal.ingredients):
            n = i.nutrients
            nut += n
    return render(request, 'nutritrack/index.html', {'user': request.user, 'nut': nut})


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
            m, _ = Meal.objects.get_or_create(name=pred['prediction']['label'])
            mr = MealReport(user=request.user, meal=m)
            mr.save()
            # return render(request, 'nutritrack/form.html', {'form': pred})
            return redirect('/nutritrack/meals/')
    else:
        form = UploadFileForm()
    return render(request, 'nutritrack/form.html', {'form': form})


@login_required
def profile(request):
    return redirect('/nutritrack/')


@login_required
def meals(request):
    return render(request, 'nutritrack/meals.html', {'meals': [mr.meal for mr in MealReport.objects.filter(user=request.user)]})

