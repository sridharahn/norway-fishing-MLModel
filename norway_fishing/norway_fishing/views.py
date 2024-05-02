from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import json
import os

# Load the trained ML model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'knn_tools_clf.pkl')
model = joblib.load(file_path)

def home(request):
    return render(request, 'home.html')

def predict(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        
        # Extract features from the request data
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        crew = float(data.get('crew'))
        ship_length = float(data.get('shipLength'))
        engine_power = float(data.get('enginePower'))
        ship_age = float(data.get('shipAge'))
        cod = 1 if data.get('species') == 'cod' else 0
        pok = 1 if data.get('species') == 'pok' else 0
        had = 1 if data.get('species') == 'had' else 0
        lin = 1 if data.get('species') == 'lin' else 0
        kcd = 1 if data.get('species') == 'kcd' else 0
        hal = 1 if data.get('species') == 'hal' else 0
        mon = 1 if data.get('species') == 'mon' else 0
        usk = 1 if data.get('species') == 'usk' else 0
        reg = 1 if data.get('species') == 'reg' else 0
        pra = 1 if data.get('species') == 'pra' else 0
        
        # Make prediction using the loaded ML model
        prediction = model.predict([[ship_length, crew, engine_power, longitude, latitude, ship_age, cod, pok, had, lin, kcd, hal, mon, usk, reg, pra]])

        return JsonResponse({'prediction': str(prediction[0])})
    else:
        return JsonResponse({'error': 'Invalid request method'})
