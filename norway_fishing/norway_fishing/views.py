from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import json
import os
import numpy as np
import warnings
from django.http import HttpResponse
from datetime import datetime

# Load the trained ML model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

knn_file_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'knn_tools_clf.pkl')
knn_model = joblib.load(knn_file_path)
knn_scaler_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'knn_tools_scaler.pkl')
knn_scaler = joblib.load(knn_scaler_path)

rf_file_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'random_forest.pkl')
rf_classifier = joblib.load(open(rf_file_path, 'rb'))

rf_scaler_path = os.path.join(BASE_DIR, 'norway_fishing', 'ML_models', 'random_forest_scaler.pkl')
rf_scaler = joblib.load(open(rf_scaler_path, 'rb'))
import numpy as np

def landing(request):

    fishing_municipalties = [4204, 1149, 1145, 4613, 4602, 1515, 1579, 4626, 1506, 4625, 1508, 3807, 1507, 1532, 5403, 5601, 5413, 1580, 4649, 1870, 1554, 5401, 1160, 5060, 1520, 1573, 1804, 5414, 1837, 1528, 4601, 301, 3019, 3011, 4215, 4202, 4203, 1119, 1111, 4206, 4201, 4207, 4205, 1505, 5404, 5442, 5405, 1860, 5014, 5441, 5028, 5436, 5439, 5444, 5434, 5423, 1874, 5001, 5433, 5435, 1865, 5406, 1871, 5443, 5438, 5437, 1859, 4617, 4636, 5427, 1867, 1857, 5424, 4645, 5440, 3035, 5432, 1511, 1838, 5421, 1834, 5430, 5059, 3438, 1124, 1835, 1868, 1813, 5422, 1866, 1875, 5419, 5057, 5061, 5428, 1103, 1836, 1820, 5402, 1815, 1851, 1822, 3808, 5420, 1806, 1576, 5054, 1514, 1106, 4615, 4616, 5426, 1856, 1151, 3813, 1845, 5429, 4621, 5007, 5412, 1848, 3804, 5058, 5418, 1818, 5630, 5634, 1130, 5425, 1547, 1108, 4648, 4632, 4631, 4624, 4634, 4612, 1557, 1535, 5055, 1101, 1134, 5020, 1516, 1531, 1539, 4614, 4622, 1517, 5056, 3003, 1827, 1824, 1812, 1811, 5047, 1841, 5417, 3029, 4212, 1816, 3004, 1833, 3403, 1121, 5037, 4635, 5049, 5053, 1127, 5411, 3024, 5052, 3022, 4225, 1146, 1133, 3430, 5006, 5501, 5614, 3805, 3811, 5603, 3814, 3806, 5038, 4638, 4633, 4627, 3017]
    vessel_county = [42, 11, 46, 15, 54, 38, 18, 50, 30,  3, 34]
    appcode_list = {800:'Flour and oil', 100:'Fresh (consumption)', 110:'Fresh export (also icing)', 200:'Freezing', 400:'Salting',  90:'Breeding', 220:'Frozen fillet', 111:'Fresh domestic', 700:'Other consumption', 500:'Hanging', 912:'Animal feed',
       921:'Survey', 210:'Round freezing', 710:'Canning', 470:'Sugar salting', 717:'Pilling/lacquering', 260:'Pilling/freezing', 920:'Silage', 899:'Sorted fish', 999:'Unspecified', 230:'Frozen bait', 799:'Unspecified consumption',
       450:'Clipfish', 130:'Fresh bait', 211:'Freezing for consumption', 120:'Fresh fillet', 510:'Drying'}
    quotacode_list = {1:'Normal', 14:'Apprentice',  2:'Research',  3:'Academic', 11:'King Crab',  5:'Recreational', 13:'Live storage',  7:'Delivery', 15:'Additional',  9:'Bait', 10:'Tourist sale'}
    ZoneCodes = ['NOR', 'XSV', 'GBR', 'RUS', 'XEU', 'FRO', 'GRL']
    species_map = {'COD':'Atlantic Cod', 'POK':'Pollock', 'HAD':'Haddock', 'LIN':'Ling', 'KCD':'Red King Crab', 'HAL':'Atlantic Halibut', 'MON':'Angler(Monk)', 'USK':'Cusk', 'REG':'Golden Redfish', 'PRA':'Northern Prawn'}
    months = [
        {'code': 1, 'name': 'January'},
        {'code': 2, 'name': 'February'},
        {'code': 3, 'name': 'March'},
        {'code': 4, 'name': 'April'},
        {'code': 5, 'name': 'May'},
        {'code': 6, 'name': 'June'},
        {'code': 7, 'name': 'July'},
        {'code': 8, 'name': 'August'},
        {'code': 9, 'name': 'September'},
        {'code': 10, 'name': 'October'},
        {'code': 11, 'name': 'November'},
        {'code': 12, 'name': 'December'},
    ]

    toolGroup = {5:'Trawl', 2:'Yarn', 1:'knot', 3:'Hook tackle', 6:'Spinning wade', 4:'Cages', 8:'Other tools'}
    # Convert numpy array to list
    context = {
        'fm_list': fishing_municipalties,
        'vc_list': vessel_county,
        'ac_list': appcode_list,
        'qc_list': quotacode_list,
        'zone_list': ZoneCodes,
        'months': months,
        'tg_list': toolGroup,
        'species_list':species_map
    }

    return render(request, 'landing.html', context)

def predict_knn(request):
        data = json.loads(request.body)
        
        species_map = {'COD':'Atlantic Cod', 'POK':'Pollock', 'HAD':'Haddock', 'LIN':'Ling', 'KCD':'Red King Crab', 'HAL':'Atlantic Halibut', 'MON':'Angler(Monk)', 'USK':'Cusk', 'REG':'Golden Redfish', 'PRA':'Northern Prawn'}
        toolGroup = {5:'Trawl', 2:'Yarn', 1:'knot', 3:'Hook tackle', 6:'Spinning wade', 4:'Cages', 8:'Other tools'}
        # Extract features from the request data
        latitude = float(data.get('Lon (location)'))
        longitude = float(data.get('Lat (location)'))
        crew = int(data.get('Crew'))
        ship_length = float(data.get('Greatest length'))
        engine_power = int(data.get('Engine power'))
        reqSpeciesCode = data.get('speciesCode').lower()
        
        current_year = datetime.now().year
        ship_age = current_year - int(data.get('Year of construction'))

        data_list = []
        selectedSpecies = []
        response = []
        for code in species_map.keys():
            species = code.lower()
            cod = 1 if species == 'cod' else 0
            pok = 1 if species == 'pok' else 0
            had = 1 if species == 'had' else 0
            lin = 1 if species == 'lin' else 0
            kcd = 1 if species == 'kcd' else 0
            hal = 1 if species == 'hal' else 0
            mon = 1 if species == 'mon' else 0
            usk = 1 if species == 'usk' else 0
            reg = 1 if species == 'reg' else 0
            pra = 1 if species == 'pra' else 0
            data_list.append([ship_length, crew, engine_power, longitude, latitude, ship_age, cod, pok, had, lin, kcd, hal, mon, usk, reg, pra])
            response.append({
                'code':code,
                'name':species_map[code]
            })

        print(data_list)
        # Make prediction using the loaded ML model
        scaled_data = knn_scaler.transform(data_list)
        knn_prediction = knn_model.predict(scaled_data)

        for index, prediction in  enumerate(knn_prediction):
            response[index]['tool'] = toolGroup[prediction]

        selected_species_list = []
        remaining_species_list = []

        for fish in response:
            if fish["code"].lower() == reqSpeciesCode.lower():
                selected_species_list.append(fish)
            else:
                remaining_species_list.append(fish)

        return JsonResponse({'success' : True, 'value': 'KNN Model called','prediction': selected_species_list, 'suggestion': remaining_species_list})
      
import logging

def randomforest(request):
    if request.method == 'GET':
        return render(request, 'basic_input.html')

    elif request.method == 'POST':
        data = json.loads(request.body)
        print("request",data)
        print("request",data.get('Zone (code)', None))
        features_input_list = ['Fishing municipality (code)', 'Crew', 'Ship municipality (code)',
            'Vessel county (code)', 'Greatest length', 'Year of construction',
            'Engine power', 'Year of engine construction', 'Quota type (code)',
            'Tool - group (code)', 'Tools - main group (code)',
            'Coast/ocean (code)', 'Lon (location)', 'Lat (location)',
            'Landing month (code)', 'Preservation method (code)', 'Quality (code)',
            'Application (code)', 'Product weight', 'Ship age', 'Zone (code)']
        test_input = {}
        for features in features_input_list:
            test_input[features] = data.get(features, None)

        current_year = datetime.now().year
        test_input['Ship age'] = current_year - int(test_input['Year of construction'])
        test_input['Ship municipality (code)'] = test_input['Fishing municipality (code)']

        #Convert Zone (code) into encoded format
        toolGroup = {5:'Trawl', 2:'Yarn', 1:'knot', 3:'Hook tackle', 6:'Spinning wade', 4:'Cages', 8:'Other tools'}
        toolMain_list = {5:1, 1: 2, 2: 3, 3: 3, 4:3, 6:3, 8:4}
        encoded_zones = {'Zone (code)_NOR': 0, 'Zone (code)_XSV': 0, 'Zone (code)_GBR': 0, 'Zone (code)_RUS': 0, 'Zone (code)_XEU': 0, 'Zone (code)_FRO': 0, 'Zone (code)_GRL': 0, 'Zone (code)_XBS': 0, 'Zone (code)_ISL': 0, 'Zone (code)_XNW': 0, 'Zone (code)_XJM': 0, 'Zone (code)_XRR': 0}
        encoded_zones["Zone (code)_"+test_input['Zone (code)']] = 1
        test_input['Coast/ocean (code)'] = int(test_input['Coast/ocean (code)'] == 'coast')

        test_input.pop('Zone (code)')
        test_input.update(encoded_zones)

        data_list = []
        for tools in toolGroup.keys():
            test_input['Tool - group (code)'] = tools
            test_input['Tools - main group (code)'] = toolMain_list[int(test_input['Tool - group (code)'])]
            data_list.append(list(test_input.values()))

        species_map = {'COD':'Atlantic Cod', 'POK':'Pollock', 'HAD':'Haddock', 'LIN':'Ling', 'KCD':'Red King Crab', 'HAL':'Atlantic Halibut', 'MON':'Angler(Monk)', 'USK':'Cusk', 'REG':'Golden Redfish', 'PRA':'Northern Prawn'}
        
        print(data_list)
        testip_np = np.array(data_list)
        warnings.simplefilter("ignore")
        scaled_data = rf_scaler.transform(testip_np)
        predicted_val = rf_classifier.predict(scaled_data)
        print(predicted_val)
        toolList = [tool for tool in toolGroup.values()]

        
        response = []

        for index, prediction in  enumerate(predicted_val):
            response.append({
                'code':prediction,
                'tool':toolList[index],
                'name':species_map[prediction]
            })

        return HttpResponse(json.dumps({'success' : True, 'value': 'Random forest called', 'prediction' : response}), content_type="application/json")   
