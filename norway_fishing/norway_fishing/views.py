from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import json
import os
import numpy as np
import warnings
from django.http import HttpResponse

# Load the trained ML model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'knn_tools_clf.pkl')
model = joblib.load(file_path)

rf_file_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'random_forest.pkl')
rf_classifier = joblib.load(open(rf_file_path, 'rb'))

rf_scaler_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'random_forest_scaler.pkl')
rf_scaler = joblib.load(open(rf_scaler_path, 'rb'))

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
      
def randomforest(request):
    if request.method == 'GET':
        return render(request, 'basic_input.html')

    elif request.method == 'POST':
        features_input_list = ['Fishing municipality (code)', 'Crew', 'Ship municipality (code)',
            'Vessel county (code)', 'Greatest length', 'Year of construction',
            'Engine power', 'Year of engine construction', 'Quota type (code)',
            'Tool - group (code)', 'Tools - main group (code)',
            'Coast/ocean (code)', 'Lon (location)', 'Lat (location)',
            'Landing month (code)', 'Preservation method (code)', 'Quality (code)',
            'Application (code)', 'Product weight', 'Ship age', 'Zone (code)']
        test_input = {}
        for features in features_input_list:
            test_input[features] = request.POST.get(features, None)

        #Convert Zone (code) into encoded format
        encoded_zones = {'Zone (code)_NOR': 0, 'Zone (code)_XSV': 0, 'Zone (code)_GBR': 0, 'Zone (code)_RUS': 0, 'Zone (code)_XEU': 0, 'Zone (code)_FRO': 0, 'Zone (code)_GRL': 0, 'Zone (code)_XBS': 0, 'Zone (code)_ISL': 0, 'Zone (code)_XNW': 0, 'Zone (code)_XJM': 0, 'Zone (code)_XRR': 0}
        encoded_zones["Zone (code)_"+test_input['Zone (code)']] = 1
        test_input['Coast/ocean (code)'] = int(test_input['Coast/ocean (code)'] == 'True')

        test_input.pop('Zone (code)')
        test_input.update(encoded_zones)
        print(test_input)
        testip_np = np.array(list(test_input.values())).reshape(1, -1)
        warnings.simplefilter("ignore")
        scaled_data = rf_scaler.transform(testip_np)
        predicted_val = rf_classifier.predict(scaled_data)
        print(predicted_val[0])
        
        return HttpResponse(json.dumps({'success' : True, 'value': 'Random forest called', 'Prediction' : str(predicted_val[0])}), content_type="application/json")   
