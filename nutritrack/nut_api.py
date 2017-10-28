import requests
import json
from models import Nutrient

def _nut_info(query):
  appId  = "93483ede"
  appKey = "08a82146aa79bb1e5cbb5189e8a618a9"

  r = requests.post('https://api.nutritionix.com/v1_1/search', data = {
    "appId" : appId,
    "appKey": appKey,
    "query" : query
  }).json()

  #parsed_r = json.loads(r.text)
  query_id = r['hits'][0]['_id']

  nut_r = requests.get(f'https://api.nutritionix.com/v1_1/item?id={query_id}&appId={appId}&appKey={appKey}').json()
  #parsed_nut = json.loads(nut_r.text)

  nut = Nutrient()
  nut.kcal = nut_r['nf_calories']
  nut.sugar = nut_r['nf_sugars']
  nut.sodium = nut_r['nf_sodium']
  nut.fat = nut_r['nf_total_fat']
  nut.carbs = nut_r['nf_total_carbohydrate']
  nut.protein = nut_r['nf_protein']
  nut.calcium = nut_r['nf_calcium_dv']
  nut.vA = nut_r['nf_vitamin_a_dv']
  nut.vC = nut_r['nf_vitamin_c_dv']
  nut.iron = nut_r['nf_iron_dv']

  nut.save()
