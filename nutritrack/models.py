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

    def __str__(self):
        return f'{self.kcal} kcal, {self.fat} g total fat, {self.carb} g total carbohydrate, {self.sugar} g sugars, ' \
               f'{self.protein} g protein, {self.sodium} mg sodium, {self.vA}% Vitamin A, {self.vC}% Vitamin C, ' \
               f'{self.iron}% Iron, {self.calcium}% Calcium '


class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')

    @property
    def ingredients(self):
        return Ingredient.objects.filter(meal=self)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='')
    amount = models.FloatField()
    nutrients = models.ForeignKey(Nutrient)

    def __str__(self):
        return f'{self.name} - {self.amount} g'
