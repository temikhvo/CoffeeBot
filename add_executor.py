import json

data = {}
data['executors'] = []
data['executors'].append({
        "id": 191435757,
        "firstname": "Артем",
        "lastname": "Хворостянский",
        "username": "temikhvo",
        "cafe": "Кооператив_Черный"
})
data['executors'].append({
        "id": 226259176,
        "firstname": "Valeriya",
        "lastname": None,
        "username": 'lerahvrst',
        "cafe": "SURFCoffee",
})


with open('executors.json', 'w') as outfile:
        json.dump(data, outfile)