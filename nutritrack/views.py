import datetime
import json

import cv2
from django.conf.urls import url
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from nutritrack import predict, nut_api, prices, recipes
from nutritrack.forms import UploadFileForm, RegistrationForm, ProfileForm
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
    mr = MealReport.objects.filter(user=request.user, timestamp__gte=datetime.datetime.now().date())
    for r in list(mr):
        for i in r.meal.ingredients.all():
            n = i.nutrients
            nut += n
    ratio = request.user.profile.bmr / 2000
    nut.vA /= ratio
    nut.vC /= ratio
    nut.iron /= ratio
    nut.calcium /= ratio

    meals = [mr.meal for mr in MealReport.objects.filter(user=request.user)]
    mrs = MealReport.objects.filter(user=request.user)
    for mmm in mrs:
      mmm.meal.nut = Nutrient()
      for inc in mmm.meal.ingredients.all():
        mmm.meal.nut += inc.nutrients
    return render(request, 'nutritrack/index.html', {'user': request.user, 'nut': nut,
                                                     'mrs': mrs})


@ensure_csrf_cookie
def splash(request):
    return render(request, 'splash.html')


@login_required
def report(request):
    if request.method == 'POST':
        if 'predictions' in request.POST:
            label = request.POST['predictions']
            query = label
            if label == 'pizza':
                query = '3 slices of pizza'
            m, new = Meal.objects.get_or_create(name=label)
            if new:
                nut = nut_api.load_nutrition_data(query)
                i = Ingredient(name=label, amount=1, nutrients=nut)
                i.save()
                m.ingredients.add(i)
                m.save()
            mr = MealReport(user=request.user, meal=m)
            mr.save()
            return redirect('/nutritrack/meals/')

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['file']
            with open('/tmp/image' + image.name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            opencvImage = cv2.imread('/tmp/image' + image.name)
            pred = predict.client.predict_image(opencvImage)

            return render(request, 'nutritrack/predict.html', {'options': pred['top5']})
    else:
        form = UploadFileForm()
    return render(request, 'nutritrack/form.html', {'form': form})


@login_required
def edamam(request, id):
    meal = recipes.import_recipe(recipes.recipes[int(id)])
    return redirect('/nutritrack/recipe/' + str(meal.id))


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            request.user.profile.age = form.cleaned_data['age']
            request.user.profile.height = form.cleaned_data['height']
            request.user.profile.weight = form.cleaned_data['weight']
            request.user.profile.sex = form.cleaned_data['sex']
            request.user.profile.activity_level = form.cleaned_data['activity_level']
            request.user.save()
            messages.info(request, 'Your information has been saved.')
            return render(request, 'registration/profile.html', {'profile': request.user.profile, 'form': form})
    else:
        form = ProfileForm()
    return render(request, 'registration/profile.html', {'profile': request.user.profile, 'form': form})


@login_required
def meals(request):
    return render(request, 'nutritrack/meals.html',
                  {'meals': [mr.meal for mr in MealReport.objects.filter(user=request.user)],
                   'meals_suggest': [(x, recipes.recipes[x]) for x in recipes.get_best_recipe(request.user)[::-1][:5]]})


@login_required
def recipe(request, recipe_id):
    r = Meal.objects.get(pk=recipe_id)
    inc = list(r.ingredients.all())
    for i in inc:
        p = prices.get_price(i.name)
        if p is None:
            i.price = '(Price Unavailable)'
        else:
            i.price = f'${(p["unit"] * i.amount):.2f} - ${(p["package"]):.2f} per package (Walmart)'
    return render(request, 'nutritrack/recipe.html', {'recipe': r, 'ingredients': inc})


@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            login(request, user)
            messages.info(request, 'Welcome to NutriTrack!')
            return redirect('/nutritrack/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

