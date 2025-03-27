from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

#fxn to find a user
def find_staff_by_email(email):
    for details in staff_directory:
        if details["email"] == email:
            return details
        
def find_staff_by_id(id):
    for staff in staff_directory:
        if staff["id"] == id:
            return staff

#in-memory storage
staff_directory = [
    {
        "id": str(uuid.uuid4()),
        "name": "Sharon",
        "email": "sbenishwilliams@gmail.com",
        "role" : "Frontend dev"
    },
    {
        "id" : str(uuid.uuid4()),
        "name": "Gozie",
        "email": "gozagu.com",
        "role" : "Frontend dev"
    }
]

@app.route('/')
def home():
    return '<h1>Flask Api</h1>'

#GET
@app.route("/v1/staff", methods=["GET"])
def get_staffs():
    return jsonify(staff_directory)

@app.route("/v1/staff/<string:staff_id>", methods=["GET"])
def get_staff(staff_id):
    staff = find_staff_by_id(staff_id)
    print(staff)
    print(staff_directory)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify(staff)

#POST 
@app.route("/v1/staff", methods=["POST"])
def add_staff():
    data = request.get_json()

    required_fields= {"name", "email", "role"}
    if not required_fields.issubset(data.keys()):
        return jsonify({"error": "Missing required fields", "required_fields": list(required_fields)}), 400

    staff_email = data.get("email")

    if not staff_email:
        return jsonify({"error": "Invalid email"}), 400
    if find_staff_by_email(staff_email):
        return jsonify({"error": "Duplicate staff email"}), 400

    staff_id = str(uuid.uuid4())
    staff_directory.append({
        "id" : staff_id,
        "name" : data.get("name"),
        "email" : data.get("email"),
        "role" : data.get("role"),
    })

    return jsonify({"message": "staff added", "id": staff_id}), 201

#PUT
@app.route("/v1/staff/<string:staff_id>", methods=['PUT'])
def update_staff(staff_id):
    data = request.get_json()
    staff = find_staff_by_id(staff_id)

    if staff:
        staff_index = next((i for i , staff in enumerate(staff_directory) if staff["id"]==staff_id), -1)
        staff_directory[staff_index]["name"] = data.get("name", staff_directory[staff_index]["name"])
        staff_directory[staff_index]["email"] = data.get("email", staff_directory[staff_index]["email"])
        staff_directory[staff_index]["role"] = data.get("role", staff_directory[staff_index]["role"])

        return jsonify({"message": "Staff updated successfully"}), 200
    else:
        return jsonify({"error": "Staff not found!"}), 404
    

#DELETE
@app.route("/v1/staff/<string:staff_id>", methods= ["DELETE"])
def delete_staff(staff_id):
    staff = find_staff_by_id(staff_id)

    if staff:
        staff_directory.remove(staff)
        return jsonify({"message": "staff deleted"}),200
    else:
        return jsonify({"error": "staff not found"}), 404


if __name__ == '__main__' :
    app.run(debug=True)