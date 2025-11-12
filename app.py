from flask import Flask, request, jsonify, render_template
import util

app = Flask(__name__)

util.load_saved_artifacts()

@app.route('/')
def home():
    locations = util.get_location_names()
    return render_template('index.html', locations=locations)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    loc = jsonify({
        'locations': util.get_location_names()
    })
    loc.headers.add('Access-Control-Allow-Origin', '*')

    return loc

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    bath = int(request.form['bath'])
    balcony = int(request.form['balcony'])
    bhk = int(request.form['bhk'])
    room_size_avg = float(request.form['room_size_avg'])
    location = request.form['location']

    estimated_price = util.get_estimated_price(location, bath, balcony, bhk, total_sqft, room_size_avg)
    return render_template(
        'index.html',
        estimated_price=estimated_price,
        locations=util.get_location_names()
    )

if __name__ == '__main__':
    app.run()

