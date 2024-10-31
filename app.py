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
from flask import Flask, render_template,request, session, redirect, url_for, render_template_string, send_file, flash, jsonify
import requests
import numpy as np
import pandas as pd
import pandas_datareader as data
import webbrowser
from flask_sqlalchemy import SQLAlchemy
import keras.models
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, validators
from wtforms.validators import InputRequired, Email, Length 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import time
import jsonpickle
import wtforms

app = Flask(__name__, static_folder='static')
app.secret_key = 'smi'
db = SQLAlchemy()

app.config['SECRET_KEY'] = 'vogueXProject'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///vogueX.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return (self.sno)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.username} - {self.date_created}"
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    style ={}
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = wtforms.PasswordField(validators=[validators.EqualTo('password', 'Password mismatch')])
    show_password = BooleanField('Show Password')


class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm New Password', validators=[
        InputRequired(), Length(min=8, max=80), validators.EqualTo('new_password', message="Passwords must match")
    ])

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    print("hello")
    if form.validate_on_submit():
        username = form.username.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        user = User.query.filter_by(username=username).first()
        
        if user:
            
            if new_password == confirm_password:
                # Hash the new password and update the user’s password in the database
                hashed_password = generate_password_hash(new_password)
                user.password = hashed_password
                db.session.commit()
                flash('Your password has been updated successfully!', 'success')
                return redirect(url_for('login'))
            else:
                flash("New password and confirm password do not match.", 'danger')
        else:
            print("No user")
            flash('No user found with that username.', 'danger')

    return render_template('forgot_password.html', form=form)

@app.route("/home")
@login_required
def home_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    print("Redirect to home page for user")
    return render_template('home.html', username=session['username'])
    

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username = form.username.data, email= form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit() 
        return redirect(url_for('home'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html',form=form)

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user,remember = form.remember.data)
                session['username'] = form.username.data
                print("User Verified\n")
                return redirect(url_for('home_page'))
            else:
                return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('try.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                session['username'] = form.username.data
                return redirect(url_for('home_page'))
            else:
                return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    
    return render_template('try.html', form=form)

# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/favorites")  
def favorites():
    favorites_list = session.get('favorites', [])
    print("Current favorites list:", favorites_list)  # Debug line to check data structure
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
    print(occasion)
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
    {"thumbnail": item['thumbnail'], "link": item['link'], "occasion":occasion}
    for item in results.get('images_results', [])[:10]  # Get top 10 images
]
    # Render results in recommendationresults.html
    return render_template("recommendationresult.html", image_data=image_data)

@app.route("/tryon")
def tryon():
    return render_template("tryon.html")

@app.route('/tryon/cloth')
def tryon_cloth():
    image_data = request.args.get('uploaded-image')
    return render_template('tryon_cloth.html', image_data=image_data)

@app.route('/tryon/glasses')
def tryon_glass():
    image_data = request.args.get('uploaded-image')
    return render_template('tryon_glasses.html', image_data=image_data)

CASCADES_DIR = '/static/cascades'

@app.route('/process/glass', methods=['POST'])
def process_glasses():
    image_data = request.form['imageData']
    glasses_file = request.files['glasses']

    image_bytes = image_data.split(",")[1]  
    nparr = np.frombuffer(base64.b64decode(image_bytes), np.uint8)

    image = cv.imdecode(nparr, cv.IMREAD_COLOR)
    glasses = cv.imdecode(np.frombuffer(glasses_file.read(), np.uint8), cv.IMREAD_UNCHANGED)

    if image is None:
            return jsonify({'error': 'Received image is empty'})

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    face_cascade = cv.CascadeClassifier('static\cascades\haarcascade_frontalface_alt.xml')
    eye_cascade = cv.CascadeClassifier('static\cascades\haarcascade_eye.xml')

    #gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)
    face = face_cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5) 

    fx, fy, fw, fh = face[0]
    roi_face  = gray[fy : fy + fh, fx : fx + fw] 
    roi_color = image[fy : fy + fh, fx : fx + fw]

    eyes = eye_cascade.detectMultiScale(roi_face, scaleFactor = 1.1, minNeighbors = 5)
    ex, ey, ew, eh = eyes[0]

    def image_resize(image, width = None, height = None, inter = cv.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2] 

        if width is None and height is None:
            return image

        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)

        else:
            r = width / float(w)
            dim = (width, int(h * r))

        resized = cv.resize(image, dim, interpolation = inter)
        return resized
    roi_eyes = roi_face[ey : ey + eh, ex : ex + ew]
    glasses2 = image_resize(glasses.copy(), width = ew)
    print('Glasses shape= ' + str(glasses2.shape))

    gw, gh, gc= glasses2.shape
    for i in range(0, gw):
        for j in range(0, gh):
            if glasses2[i,j][3] != 0:
                roi_color[ey + i, ex + j] = glasses2[i,j]
    
    image = cv.cvtColor(image, cv.COLOR_BGRA2RGB)
    processed_image = image
    processed_image = cv.cvtColor(processed_image, cv.COLOR_BGR2RGB)
    cv.imwrite('output.jpg', processed_image)
   
    _, processed_image_data = cv.imencode('.jpg', processed_image)
    processed_image_bytes = processed_image_data.tobytes()
    processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
    
    return render_template('tryon_result.html', image=processed_image_base64, tryon_type='Glass')

@app.route('/tryon/necklace')
def tryon_necklace():
    image_data = request.args.get('uploaded-image')
    return render_template('tryon_necklace.html', image_data=image_data)

@app.route('/process/necklace', methods=['POST'])
def process_necklace():
    image_data = request.form['imageData']
    necklace_file = request.files['necklace']

    image_bytes = image_data.split(",")[1]  
    nparr = np.frombuffer(base64.b64decode(image_bytes), np.uint8)

    image = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)
    necklace = cv.imdecode(np.frombuffer(necklace_file.read(), np.uint8), cv.IMREAD_UNCHANGED)

    if image is None:
            return jsonify({'error': 'Received image is empty'})
    
    def fit_factor(dim, dis):
        fac = round(dis / dim, 2)
        return fac

    def map_factor(img_dim, s2, tar_dim):
        if tar_dim[1] > img_dim[0] - (s2 + 80):
            new_dim = img_dim[0] - (s2 + 40)
        else:
            new_dim = tar_dim[1]
        return new_dim

    def acc_crop_side(image):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        ret, mask = cv.threshold(gray, 220, 255, cv.THRESH_BINARY_INV)
        cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv.contourArea)
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        return extTop

    def acc_crop_bottom(image):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        ret, mask = cv.threshold(gray, 220, 255, cv.THRESH_BINARY_INV)
        cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv.contourArea)
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        return extBot, extRight, extLeft

    def acc_cor_points(oimage):
        first_half = oimage[0:oimage.shape[1], 0:int(oimage.shape[0] / 2)]
        second_half = oimage[0:oimage.shape[1], int(oimage.shape[0] / 2):oimage.shape[0]]
        topl = acc_crop_side(first_half)
        topr = acc_crop_side(second_half)
        bot, right, left = acc_crop_bottom(oimage)
        dis = (int(oimage.shape[0] / 2) + topr[0])
        if topl[1] > topr[1]:
            y = topr[1]
        else:
            y = topl[1]
        if topl[0] > left[0]:
            x = left[0]
        else:
            x = topl[0]
        if dis > right[0]:
            w = dis
        else:
            w = right[0]
        h = bot[1]
        return x, y, w, h
    
    x, y, w, h = acc_cor_points(necklace)
    image1 = necklace[y:h, x:w]

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('static\misc\shape_predictor_68_face_landmarks.dat')

    height, width, _ = image.shape

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        (s1, s2) = shape[3]  # Example landmarks, adjust as needed
        (e1, e2) = shape[13]  # Example landmarks, adjust as needed
        dis = e1 - s1
        dim = image1.shape[1]

        m_factor = fit_factor(dim, dis)
        p_dim = (int(image1.shape[1] * m_factor), int(image1.shape[0] * m_factor))
        mf = map_factor(image.shape, s2, p_dim)
        if mf == p_dim[0]:
            dim = p_dim
        else:
            dim = (p_dim[0], mf)

        resized = cv.resize(image1, dim, interpolation=cv.INTER_AREA)
        img2gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
        ret, mask = cv.threshold(img2gray, 220, 255, cv.THRESH_BINARY_INV)
        mask_inv = cv.bitwise_not(mask)
        resized1 = cv.resize(resized, (resized.shape[1] * 10, resized.shape[0] * 10), interpolation=cv.INTER_AREA)
        mask = cv.resize(mask, (resized.shape[1] * 10, resized.shape[0] * 10), interpolation=cv.INTER_AREA)
        mask_inv = cv.resize(mask_inv, (resized.shape[1] * 10, resized.shape[0] * 10), interpolation=cv.INTER_AREA)

        point1 = s2 + 22
        roi1 = image[point1:point1 + dim[1], s1:s1 + dim[0]]
        roi = cv.resize(roi1, (roi1.shape[1] * 10, roi1.shape[0] * 10), interpolation=cv.INTER_AREA)

        roi_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
        roi_fg = cv.bitwise_and(resized1, resized1, mask=mask)

        roi_fg_rgb = cv.cvtColor(roi_fg, cv.COLOR_BGRA2BGR)
        dst1 = cv.add(roi_bg, roi_fg_rgb)
        dst = cv.resize(dst1, (int(dst1.shape[1] / 10), int(dst1.shape[0] / 10)), interpolation=cv.INTER_AREA)

        image[point1:point1 + dim[1], s1:s1 + dim[0]] = dst
    
      
    # image = cv.cvtColor(image, cv.COLOR_BGRA2RGB)
    processed_image = image
    # processed_image = cv.cvtColor(processed_image, cv.COLOR_BGR2RGB)
    cv.imwrite('output-necklace.png', processed_image)
   
    _, processed_image_data = cv.imencode('.png', processed_image)
    processed_image_bytes = processed_image_data.tobytes()
    processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
    
    return render_template('tryon_result.html', image=processed_image_base64, tryon_type='Necklace')

@app.route('/tryon/earring')
def tryon_earrings():
    image_data = request.args.get('uploaded-image')
    return render_template('tryon_earrings.html', image_data=image_data)

@app.route('/process/earrings', methods=['POST'])
def process_earrings():
    image_data = request.form['imageData']
    lear_file = request.files['lear']
    rear_file = request.files['rear']

    image_bytes = image_data.split(",")[1]  
    nparr = np.frombuffer(base64.b64decode(image_bytes), np.uint8)

    image = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)
    left_ear = cv.imdecode(np.frombuffer(lear_file.read(), np.uint8), cv.IMREAD_UNCHANGED)
    right_ear = cv.imdecode(np.frombuffer(rear_file.read(), np.uint8), cv.IMREAD_UNCHANGED)

    if image is None:
            return jsonify({'error': 'Received image is empty'})
    
    def resize_earrings(face_width, face_height, earring_image):
        earring_height = int(face_height * 0.3)
        earring_width = int(face_width * 0.3)
        resized_earring = cv.resize(earring_image, (earring_width, earring_height))
        return resized_earring
    
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        left_earring_resized = resize_earrings(w, h, left_ear)
        right_earring_resized = resize_earrings(w, h, right_ear)

        left_ear_x = face_center_x - int(w * 0.65)
        left_ear_y = y + int(h * 0.55)

        right_ear_x = face_center_x + int(w * 0.15)
        right_ear_y = y + int(h * 0.7)

        for i in range(left_earring_resized.shape[0]):
            for j in range(left_earring_resized.shape[1]):
                if left_earring_resized[i, j, 3] != 0:
                    image[left_ear_y + i, left_ear_x + j] = left_earring_resized[i, j, :3]

        for i in range(right_earring_resized.shape[0]):
            for j in range(right_earring_resized.shape[1]):
                if right_earring_resized[i, j, 3] != 0:
                    image[right_ear_y + i, right_ear_x + j] = right_earring_resized[i, j, :3]
    else:
        print("No face detected in the input image.")
    
    # image = cv.cvtColor(image, cv.COLOR_BGRA2RGB)
    processed_image = image
    # processed_image = cv.cvtColor(processed_image, cv.COLOR_BGR2RGB)
    cv.imwrite('output-earrings.jpg', processed_image)
   
    _, processed_image_data = cv.imencode('.jpg', processed_image)
    processed_image_bytes = processed_image_data.tobytes()
    processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
    
    return render_template('tryon_result.html', image=processed_image_base64, tryon_type='Earrings')

@app.route('/tryon/lip')
def tryon_lips():
    image_data = request.args.get('uploaded-image')
    return render_template('tryon_lipcolor.html', image_data=image_data)

@app.route('/process/lip', methods=['POST'])
def process_lips():
    image_data = request.form['imageData']
    lip_color = request.form['lipcolor']

    image_bytes = image_data.split(",")[1]  
    nparr = np.frombuffer(base64.b64decode(image_bytes), np.uint8)

    image = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)

    if image is None:
            return jsonify({'error': 'Received image is empty'})
    
    if lip_color == 'punch':
        color_option = '1'
    elif lip_color == 'rose':
        color_option = '2'
    elif lip_color == 'brickred':
        color_option = '3'
    elif lip_color == 'dustyrose':
        color_option = '4'
    elif lip_color == 'nude':
        color_option = '5'
    elif lip_color == 'royalblue':
        color_option = '6'
    else:
        color_option = '7'

    # print(lip_color)

    def get_lip_landmark(img):
        '''Finding lip landmark and return list of corresponded coordinations'''
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('static\misc\shape_predictor_68_face_landmarks.dat')
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        faces = detector(gray_img)
        for face in faces:
            landmarks = predictor(gray_img, face)
            lmPoints = []
            for n in range(48, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                lmPoints.append([x, y])
        return lmPoints
    
    def change_lip_color(img, color):
        '''Change lip color based on given color option'''
        img_original = img.copy()
        lm_points = get_lip_landmark(img_original)

        # Color options
        colors = {
            "1": (83, 55, 220),   # Punch
            "2": (126, 109, 229), # Rose
            "3": (14, 22, 139),   # Brick red
            "4": (106, 105, 184),# Dusty rose
            "5": (158, 172, 204),# Nude
            "6": (86, 52, 49),     # Royal blue
            "7": (0, 0, 255)    # Red
        }

        selected_color = colors.get(color)

        poly1 = np.array(lm_points[:12], np.int32).reshape((-1, 1, 2))
        poly2 = np.array(lm_points[12:], np.int32).reshape((-1, 1, 2))

        colored = cv.fillPoly(img, [poly1, poly2], selected_color)

        colored = cv.GaussianBlur(colored, (7, 7), 0)

        result = cv.addWeighted(colored, 0.3, img_original, 0.7, 0)

        return result

    modified_img = change_lip_color(image, color_option)    
    
    processed_image = modified_img
    cv.imwrite('output-lips.jpg', processed_image)
   
    _, processed_image_data = cv.imencode('.jpg', processed_image)
    processed_image_bytes = processed_image_data.tobytes()
    processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
    
    return render_template('tryon_result.html', image=processed_image_base64, tryon_type='Lip Color')

@app.route('/tryon/hair')
def tryon_hairstyle():
    image_data = request.args.get('uploaded-image')
    return render_template('tryon_hairstyle.html', image_data=image_data)

@app.route('/process/hairstyle', methods=['POST'])
def process_hairstyle():
    image_data = request.form['imageData']
    hairstyle_file = request.files['hairstyle']

    image_bytes = image_data.split(",")[1]  
    nparr = np.frombuffer(base64.b64decode(image_bytes), np.uint8)

    image = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)
    hairstyle = cv.imdecode(np.frombuffer(hairstyle_file.read(), np.uint8), cv.IMREAD_UNCHANGED)

    cv.imwrite('hairstyle-try-on/1.jpg', image)
    cv.imwrite('hairstyle-try-on/hairstyle.jpg', hairstyle)

    if image is None:
            return jsonify({'error': 'Received image is empty'})
    
    cmd_process_0 = "cd hairstyle-try-on && python inference.py --seg_model_path image_segmentation/face_segment_checkpoints_256.pth.tar --t 500 --target_image_path 1.jpg --source_image_path hairstyle.jpg"
    
    # cmd_process = "python hairstyle-try-on/inference.py --seg_model_path hairstyle-try-on/image_segmentation/face_segment_checkpoints_256.pth.tar --t 500 --target_image_path hairstyle-try-on/hairstyle.jpg --source_image_path hairstyle-try-on/1.jpg"
    subprocess.call(cmd_process_0, shell=True)
    
    processed_image_path = 'hairstyle-try-on/exp/image_samples/images/original_input.png'

    with open(processed_image_path, "rb") as image_file:
        processed_image_bytes = image_file.read()

    processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
    
    return render_template('tryon_result.html', image=processed_image_base64, tryon_type='Hairstyle')

if __name__ == "__main__":
    app.run(debug=True)
# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0')