from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Nutrient(models.Model):
    kcal = models.IntegerField()
    fat = models.FloatField()
    carb = models.FloatField()
    sugar = models.FloatField()
    protein = models.FloatField()
    sodium = models.FloatField()
    vA = models.FloatField()
    vC = models.FloatField()
    iron = models.FloatField()
    calcium = models.FloatField()


class Meal(models.Model):
    id = models.IntegerField(primary_key=True)


class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    amount = models.FloatField()
    nutrients = models.ForeignKey(Nutrient)
