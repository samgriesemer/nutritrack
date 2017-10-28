from django.contrib import admin

# Register your models here.
from nutritrack.models import Meal, Nutrient, Ingredient

admin.site.register(Nutrient)
admin.site.register(Meal)
admin.site.register(Ingredient)

admin.site.site_header = "NutriTrack Admin"
admin.site.site_title = "NutriTrack"
