import csv
import re
from fuzzywuzzy import process, fuzz


def _to_grams(value):
    m = re.search(r'(\d+) (.+)', value)
    if m is not None:
        number = int(m.group(1))
        unit = m.group(2)
        if unit == 'oz':
            return number * 30
        if unit == 'lbs':
            return number * 450
        if unit == 'fl oz':
            return number * 30
        if unit == 'gal':
            return number * 3785
    return None


def _to_money(value):
    m = re.search(r'\$(.+)', value)
    if m is not None:
        return float(m.group(1))
    else:
        return None


prices = {}
with open('prices.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        g = _to_grams(row[2].strip())
        d = _to_money(row[1].strip())
        if g is not None and d is not None:
            prices[row[0]] = {'unit': d / g, 'package': d}


def get_price(item):
    choices = prices.keys()
    arr = process.extract(item, choices, limit=5)
    result = None
    for r, confidence in arr:
        good = True
        if confidence < 70:
            continue
        for word in item.split(' '):
            if word.lower() not in r.lower():
                good = False
        if good:
            result = r
            break
    if result is None:
        return None

    o = prices[result]
    o['keyw'] = result
    return o
