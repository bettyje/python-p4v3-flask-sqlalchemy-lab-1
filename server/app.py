#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        response_body = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year,
        }

        return make_response(response_body, 200)
    else:
        response_body = {"message": f"Earthquake {id} not found."}
        return make_response(jsonify(response_body), 404)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for earthquakes with magnitude >= given value
    earthquakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude).all()

    # Format the response data
    response_body = {
        "count": len(earthquakes),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            } for quake in earthquakes
        ]
    }
    return make_response(jsonify(response_body), 200)


if __name__ == '__main__':
    with app.app_context():
        # Optional: Perform any startup queries or tasks here
        earthquake = Earthquake.query.get(2)
        if earthquake:
            print(f"Earthquake found: {earthquake}")
        else:
            print("Earthquake with ID 2 not found.")

    app.run(port=5555, debug=True)
