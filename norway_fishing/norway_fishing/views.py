from django.shortcuts import render
import json
import joblib
import numpy as np
import os
import warnings

from django.http import HttpResponse

from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rf_file_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'random_forest.pkl')
rf_classifier = joblib.load(open(rf_file_path, 'rb'))

rf_scaler_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'random_forest_scaler.pkl')
rf_scaler = joblib.load(open(rf_scaler_path, 'rb'))

def home(request):
    return render(request, 'home.html')

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