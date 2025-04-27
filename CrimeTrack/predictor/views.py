from django.shortcuts import render
import pandas as pd
import pickle
import os
import math

# === Path Setup ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'Model', 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

# === Lookup Dictionaries ===
city_names = {
    '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore',
    '4': 'Delhi', '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore',
    '8': 'Jaipur', '9': 'Kanpur', '10': 'Kochi', '11': 'Kolkata',
    '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai', '15': 'Nagpur',
    '16': 'Patna', '17': 'Pune', '18': 'Surat'
}

crime_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST',
    '3': 'Crime against Senior Citizen', '4': 'Crime against children',
    '5': 'Crime against women', '6': 'Cyber Crimes', '7': 'Economic Offences',
    '8': 'Kidnapping', '9': 'Murder'
}

population_map = {
    '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60,
    '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10,
    '12': 20.30, '13': 29.00, '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
}


# === Views ===

def index(request):
    return render(request, 'index.html')


def predict(request):
    if request.method == 'POST':
        city_code = request.POST.get('city')
        crime_code = request.POST.get('type')  # HTML uses "type"
        year = request.POST.get('year')

        # Validate inputs
        if not city_code or not crime_code or not year:
            return render(request, 'result.html', {'error': 'Missing input data.'})

        try:
            city_int = int(city_code)
            crime_int = int(crime_code)
            year_int = int(year)
        except ValueError:
            return render(request, 'result.html', {'error': 'Invalid input format.'})

        # Population adjustment
        pop = population_map[city_code]
        year_diff = year_int - 2011
        pop = round(pop + (0.01 * year_diff * pop), 2)

        # Model expects 4 inputs: [year, city, population, crime]
        input_data = [[year_int, city_int, pop, crime_int]]
        crime_rate = model.predict(input_data)[0]

        # Crime label
        if crime_rate <= 1:
            status = "Very Low Crime Area"
        elif crime_rate <= 5:
            status = "Low Crime Area"
        elif crime_rate <= 15:
            status = "High Crime Area"
        else:
            status = "Very High Crime Area"

        cases = math.ceil(crime_rate * pop)

        context = {
            'city_name': city_names[city_code],
            'crime_type': crime_names[crime_code],
            'year': year,
            'crime_status': status,
            'crime_rate': round(crime_rate, 4),
            'cases': cases,
            'population': pop
            
        }

        return render(request, 'result.html', context)

    return render(request, 'result.html', {'error': 'Invalid request method'})
