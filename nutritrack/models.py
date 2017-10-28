from django.contrib.auth.models import User
from django.db import models


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


class Ingredient(models.Model):
    name = models.CharField(max_length=256, default='')
    amount = models.FloatField()
    nutrients = models.ForeignKey(Nutrient, blank=True)

    def __str__(self):
        return f'{self.name} - {self.amount} g'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.nutrients_id is None:
            from nutritrack import nut_api
            self.nutrients = nut_api.load_nutrition_data(f'{self.amount} g {self.name}')
            self.nutrients_id = self.nutrients.id
        super().save(force_insert, force_update, using, update_fields)


class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')
    description = models.TextField(default='')
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name


class MealReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    meal = models.ForeignKey(Meal)

    def __str__(self):
        return f'{self.timestamp} - {self.user.username} - {self.meal.name}'

