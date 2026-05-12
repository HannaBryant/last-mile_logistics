from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from database import (
    init_db,
    create_driver, get_drivers, update_driver, delete_driver,
    create_vehicle, get_vehicles, update_vehicle, delete_vehicle,
    create_route, get_routes, update_route, delete_route,
    create_package, get_packages, update_package, delete_package
)

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)


@app.route("/drivers", methods=["GET"])
def drivers():
    return jsonify(get_drivers()), 200

@app.route("/drivers", methods=["POST"])
def add_driver():
    data = request.get_json()
    create_driver(data["name"], data["license_type"])
    return jsonify({"message":"Driver Created"})

@app.route("/drivers/<int:driver_id>", methods=["PUT"])
def edit_driver(driver_id):

    data = request.get_json()

    update_driver(
        driver_id,
        data["name"],
        data["license_type"]
    )
    
    return {"message": "Driver updated successfully"}

@app.route("/drivers/<int:driver_id>", methods=["DELETE"])
def remove_driver(driver_id):

    delete_driver(driver_id)

    return {"message": "Driver deleted successfully"}

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

@app.route("/vehicles/<int:vehicle_id>", methods=["PUT"])
def edit_vehicle(vehicle_id):

    data = request.get_json()

    update_vehicle(
        vehicle_id,
        data["license_plate"],
        data["model"]
    )

    return {"message": "Vehicle updated successfully"}

@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def remove_vehicle(vehicle_id):

    delete_vehicle(vehicle_id)

    return {"message": "Vehicle deleted successfully"}

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

@app.route("/routes/<int:route_id>", methods=["PUT"])
def edit_route(route_id):

    data = request.get_json()

    update_route(
        route_id,
        data["service_zone"]
    )

    return {"message": "Route updated successfully"}

@app.route("/routes/<int:route_id>", methods=["DELETE"])
def remove_route(route_id):

    delete_route(route_id)

    return {"message": "Route deleted successfully"}

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

@app.route("/packages/<int:package_id>", methods=["PUT"])
def edit_package(package_id):

    data = request.get_json()

    update_package(
        package_id,
        data["description"],
        data["weight"]
    )

    return {"message": "Package updated successfully"}

@app.route("/packages/<int:package_id>", methods=["DELETE"])
def remove_package(package_id):

    delete_package(package_id)

    return {"message": "Package deleted successfully"}

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
