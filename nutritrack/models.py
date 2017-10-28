from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Nutrient(models.Model):
    kcal = models.IntegerField(default=0)
    fat = models.FloatField(default=0)
    carb = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    vA = models.FloatField(default=0)
    vC = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    calcium = models.FloatField(default=0)

    def __str__(self):
        return f'{self.kcal} kcal, {self.fat} g total fat, {self.carb} g total carbohydrate, {self.sugar} g sugars, ' \
               f'{self.protein} g protein, {self.sodium} mg sodium, {self.vA}% Vitamin A, {self.vC}% Vitamin C, ' \
               f'{self.iron}% Iron, {self.calcium}% Calcium '

    def __add__(self, other):
        self.kcal += other.kcal
        self.fat += other.fat
        self.carb += other.carb
        self.sugar += other.sugar
        self.protein += other.protein
        self.sodium += other.sodium
        self.vA += other.vA
        self.vC += other.vC
        self.iron += other.iron
        self.calcium += other.calcium
        return self


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


class MealReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    meal = models.ForeignKey(Meal)

    def __str__(self):
        return f'{self.timestamp} - {self.user.username} - {self.meal.name}'
