import requests

from .models import Nutrient


def load_nutrition_data(query):
    appId = "93483ede"
    appKey = "08a82146aa79bb1e5cbb5189e8a618a9"

    r = requests.post('https://api.nutritionix.com/v1_1/search', data={
        "appId": appId,
        "appKey": appKey,
        "query": query
    }).json()

    # parsed_r = json.loads(r.text)
    if 'hits' not in r.keys():
        print(r)
        return None

    query_id = r['hits'][0]['_id']

    nut_r = requests.get(f'https://api.nutritionix.com/v1_1/item?id={query_id}&appId={appId}&appKey={appKey}').json()
    # parsed_nut = json.loads(nut_r.text)

    nut = Nutrient()
    nut.kcal = 0 if nut_r['nf_calories'] is None else nut_r['nf_calories']
    nut.sugar = 0 if nut_r['nf_sugars'] is None else nut_r['nf_sugars']
    nut.sodium = 0 if nut_r['nf_sodium'] is None else nut_r['nf_sodium']
    nut.fat = 0 if nut_r['nf_total_fat'] is None else nut_r['nf_total_fat']
    nut.carb = 0 if nut_r['nf_total_carbohydrate'] is None else nut_r['nf_total_carbohydrate']
    nut.protein = 0 if nut_r['nf_protein'] is None else nut_r['nf_protein']
    nut.calcium = 0 if nut_r['nf_calcium_dv'] is None else nut_r['nf_calcium_dv']
    nut.vA = 0 if nut_r['nf_vitamin_a_dv'] is None else nut_r['nf_vitamin_a_dv']
    nut.vC = 0 if nut_r['nf_vitamin_c_dv'] is None else nut_r['nf_vitamin_c_dv']
    nut.iron = 0 if nut_r['nf_iron_dv'] is None else nut_r['nf_iron_dv']

    nut.save()

    return nut
