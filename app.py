from flask import Flask, jsonify, request
from database import ( 
    init_db,
      create_driver, get_drivers,
       create_vehicle, get_vehicles,
        create_route, get_routes,
         create_package, get_packages 
         )

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Last Mile Logistics Online"})

@app.route("/drivers", methods=["GET"])
def drivers():
    return jsonify(get_drivers()), 200

@app.route("/drivers", methods=["POST"])
def add_driver():
    data = request.get_json()
    create_driver(data["name"], data["license_type"])
    return jsonify({"message":"Driver Created"})

@app.route("/vehicles", methods=["GET"])
def vehicles():
    return jsonify(get_vehicles()), 200

@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    data = request.get_json()
    create_vehicle(
        data["license_plate"], 
        data["model"],
        data["driver_id"]
    )
    return jsonify({"message": "Vehicle added"})

@app.route("/routes", methods=["GET"])
def routes():
    return jsonify(get_routes()), 200

@app.route("/routes", methods=["POST"])
def add_route():
    data = request.get_json()
    create_route(
        data["date"], 
        data["service_zone"],
        data["driver_id"]
    )
    return jsonify({"message": "Routed added"})

@app.route("/packages", methods=["GET"])
def packages():
    return jsonify(get_packages()), 200

@app.route("/packages", methods=["POST"])
def add_package():
    data = request.get_json()
    create_package(
        data["description"], 
        data["weight"],
        data["route_id"]
    )
    return jsonify({"message": "Package added"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
