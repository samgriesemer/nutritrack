from django.contrib import admin

# Register your models here.
from nutritrack.models import Meal, Nutrient, Ingredient, MealReport, Profile

admin.site.register(Nutrient)
admin.site.register(Meal)
admin.site.register(Ingredient)
admin.site.register(MealReport)
admin.site.register(Profile)

admin.site.site_header = "NutriTrack Admin"
admin.site.site_title = "NutriTrack"
