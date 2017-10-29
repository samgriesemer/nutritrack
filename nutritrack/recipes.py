import datetime
import json

from nutritrack import nut_api
from nutritrack.models import Nutrient, MealReport, Meal, Ingredient

from django.utils import timezone


def import_recipe(recipe):
    meal, created = Meal.objects.get_or_create(name=recipe['recipe']['label'])
    if created:
        print(f"Importing {recipe['recipe']['label']}")
        meal.description = f"<a href='{recipe['recipe']['url']}'>{recipe['recipe']['label']}</a>"
        for ing in recipe['recipe']['ingredients']:
            nut = nut_api.load_nutrition_data(f"{ing['weight']} g {ing['text']}")
            if nut is None:
                print("WARN nut-api is none")
                nut = Nutrient()
                nut.save()
            inc = Ingredient(name=ing['text'], amount=ing['weight'], nutrients=nut)
            inc.save()
            meal.ingredients.add(inc)
        meal.save()
    return meal


file = open("recipes.json", "r")
recipes = file.read()
recipes = json.loads(recipes)
file.close()

arr = []

for i in range(600):
    arr.append([])

    try:
        arr[i].append(float(recipes[i]['recipe']['yield']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['ENERC_KCAL']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['FAT']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['CHOCDF']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['SUGAR']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['PROCNT']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['NA']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['VITA_RAE']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['VITC']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['FE']['quantity']))
    except KeyError:
        arr[i].append(0)

    try:
        arr[i].append(float(recipes[i]['recipe']['totalNutrients']['CA']['quantity']))
    except KeyError:
        arr[i].append(0)

    # import_recipe(recipes[i])


def get_best_recipe(user):
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
    mr = MealReport.objects.filter(user=user, timestamp__gte=datetime.datetime.now().date())
    for r in list(mr):
        for i in r.meal.ingredients.all():
            n = i.nutrients
            nut += n

    # space out nutrients depending on which meal this is
    hour = timezone.now().hour
    factor = 1
    if hour < 11:
        factor = 1 / 3
    elif hour < 16:
        factor = 2 / 3

    totalDietNeeds = [2000.0, 65, 300, 90, 50, 2400, 2500, 1200, 18, 1000]
    totalDietNeeds = [(user.profile.bmr / 2000.0) * t * factor for t in totalDietNeeds]

    currentDietNeeds = [totalDietNeeds[0] - nut.kcal,
                        totalDietNeeds[1] - nut.fat,
                        totalDietNeeds[2] - nut.carb,
                        totalDietNeeds[3] - nut.sugar,
                        totalDietNeeds[4] - nut.protein,
                        totalDietNeeds[5] - nut.sodium,
                        totalDietNeeds[6] - totalDietNeeds[6] * nut.vA,
                        totalDietNeeds[7] - totalDietNeeds[7] * nut.vC,
                        totalDietNeeds[8] - totalDietNeeds[8] * nut.iron,
                        totalDietNeeds[9] - totalDietNeeds[9] * nut.calcium]

    scoreWeighting = []
    scores = []

    AvgdNuts = []
    for i in range(600):
        AvgdNuts.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        AvgdNuts[i][0] = arr[i][1] / arr[i][0]
        AvgdNuts[i][1] = arr[i][2] / arr[i][0]
        AvgdNuts[i][2] = arr[i][3] / arr[i][0]
        AvgdNuts[i][3] = arr[i][4] / arr[i][0]
        AvgdNuts[i][4] = arr[i][5] / arr[i][0]
        AvgdNuts[i][5] = arr[i][6] / arr[i][0]
        AvgdNuts[i][6] = arr[i][7] / arr[i][0]
        AvgdNuts[i][7] = arr[i][8] / arr[i][0]
        AvgdNuts[i][8] = arr[i][9] / arr[i][0]
        AvgdNuts[i][9] = arr[i][10] / arr[i][0]

    for i in range(600):
        scores.append(0)
        for j in range(10):
            scores[i] -= (abs((currentDietNeeds[j] - AvgdNuts[i][j])) / totalDietNeeds[j]) ** 2

    """sorted scores will contain indexes of all recipes sorted by how good they are, [0] is worst, [499] is best"""
    sortedScores = [0]

    for i in range(599):
        for j in range(len(sortedScores)):
            if scores[i + 1] <= scores[sortedScores[j]]:
                sortedScores.insert(j, i + 1)
                break
            if j + 1 == len(sortedScores):
                sortedScores.append(i + 1)

    for i in range(600):
        print("")
        print(str(sortedScores[i]) + ":")
        print(scores[sortedScores[i]])

    print(recipes[sortedScores[599]]['recipe']['url'])
    print(json.dumps(recipes[sortedScores[599]]['recipe']))
    # print(recipes[0]['recipe']['totalNutrients'])

    for i in range(10):
        print(AvgdNuts[sortedScores[599]][i])

    return sortedScores
