from flask import Flask, render_template, request, jsonify,session
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import base64
import imutils
from imutils import face_utils
import dlib
import subprocess
import requests
from datetime import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__, static_folder='static')
app.secret_key = 'smi'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/favorites")  
def favorites():
    favorites_list = session.get('favorites', [])
    return render_template("favorites.html", favorites=favorites_list)

@app.route("/process/favorites", methods=['POST'])
def add_to_favorites():
    data = request.json
    if 'favorites' not in session:
        session['favorites'] = []
    
    session['favorites'].append({
        'link': data['link'],
        'thumbnail': data['thumbnail'],
        'occasion': data['occasion']
    })
    session.modified = True
    return '', 200  

@app.route('/delete/favorites', methods=['POST'])
def delete_from_favorites():
    data = request.get_json()
    link = data['link']

    for item in session.get('favorites', []):
        if item['link'] == link:
            session['favorites'].remove(item)
            session.modified = True
            return jsonify({"message": "Removed from favorites"}), 200

    return jsonify({"message": "Item not found in favorites"}), 404

@app.route("/fashionrecommender")
def fashionrecommender():
    return render_template("fashionrecommender.html")

@app.route('/fashionrecommender/recommendations', methods=['POST'])
def fashionrecommender_cloth():
    culture = request.form['culture']
    gender = request.form['gender']
    age_group = request.form['ageGroup']
    occasion = request.form['occasion']
    date_time = request.form['dateTime']
    location=request.form['location']
    print(date_time)
    dt_object = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")  
    date = dt_object.date()
    time = dt_object.time()

    timestamp = int(dt_object.timestamp())

    
    user_agent = "MyGeocodingApp/1.0 (Python) contact@mygeocodingapp.com"

    geolocator = Nominatim(user_agent=user_agent)
    location_data = geolocator.geocode(location)
    if location_data:

        lat, lon = location_data.latitude, location_data.longitude
    else:
        raise ValueError("Location not found.")

# Get weather data
    w_api_key = "56627ef8f515848a6752e306c8004cc9"  # Replace with your actual OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'dt': timestamp,
        'appid': w_api_key,
        'units': 'metric'
}
    response = requests.get(url, params=params)
    response.raise_for_status()
    weather_data = response.json()
    print(weather_data)

# Extract temperature and conditions
    temperature = weather_data['main']['temp']
    conditions = weather_data['weather'][0]['description']
    search_query = f"{culture} {gender} {age_group} outfit for {occasion} in {location} on {date} at {time} with {conditions} and {temperature}°C weather "
    
    # SERP API request
    api_key = '4f0e88cd837468e305e164834844f31e5c2f4e704e16003d2cdf1b3e10abd6a9'
    params = {
        'engine': 'google',
        'q': search_query,
        'tbm': 'isch',
        'api_key': api_key
    }
    response = requests.get('https://serpapi.com/search', params=params)
    results = response.json()
    
    # Extract image URLs
    image_data = [
    {"thumbnail": item['thumbnail'], "link": item['link']}
    for item in results.get('images_results', [])[:10]  # Get top 10 images
]
    
    # Render results in recommendationresults.html
    return render_template("recommendationresult.html", image_data=image_data)
