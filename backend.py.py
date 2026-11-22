from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///feastforward.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    freshness_score = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="available", nullable=False)


class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=True)


class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    food_requirements = db.Column(db.String(200), nullable=True)
    number_of_people = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


def json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, (jsonify({"error": "Request body must be valid JSON."}), 400)
    return data, None


def required_text(data, field, max_length):
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    return value if len(value) <= max_length else None


@app.errorhandler(IntegrityError)
def handle_integrity_error(_error):
    db.session.rollback()
    return jsonify({"error": "A record with the supplied unique value already exists, or a related record is missing."}), 409


@app.errorhandler(500)
def handle_server_error(_error):
    db.session.rollback()
    return jsonify({"error": "An unexpected server error occurred."}), 500


@app.get("/")
def home():
    return jsonify({"message": "Welcome to FeastForward Backend!", "status": "ok"})


@app.post("/register")
def register():
    data, error = json_body()
    if error:
        return error

    name = required_text(data, "name", 100)
    email = required_text(data, "email", 255)
    password = data.get("password")
    role = required_text(data, "role", 50)
    location = required_text(data, "location", 100)

    if not all([name, email, role, location]) or not isinstance(password, str) or len(password) < 8:
        return jsonify({
            "error": "Provide name, email, role, and location. Password must contain at least 8 characters."
        }), 400

    allowed_roles = {"provider", "volunteer", "recipient"}
    if role not in allowed_roles:
        return jsonify({"error": "Role must be provider, volunteer, or recipient."}), 400

    user = User(
        name=name,
        email=email.lower(),
        password=generate_password_hash(password),
        role=role,
        location=location,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully.", "user_id": user.id}), 201


@app.post("/food")
def post_food():
    data, error = json_body()
    if error:
        return error

    try:
        provider_id = int(data.get("provider_id"))
        quantity = int(data.get("quantity"))
    except (TypeError, ValueError):
        return jsonify({"error": "provider_id and quantity must be valid integers."}), 400

    food_type = required_text(data, "type", 100)
    location = required_text(data, "location", 100)
    freshness_score = data.get("freshness_score")

    if provider_id <= 0 or quantity <= 0 or not food_type or not location:
        return jsonify({"error": "Provide a valid provider_id, positive quantity, type, and location."}), 400

    if freshness_score is not None:
        try:
            freshness_score = float(freshness_score)
        except (TypeError, ValueError):
            return jsonify({"error": "freshness_score must be a number between 0 and 1."}), 400
        if not 0 <= freshness_score <= 1:
            return jsonify({"error": "freshness_score must be between 0 and 1."}), 400

    provider = db.session.get(User, provider_id)
    if provider is None or provider.role != "provider":
        return jsonify({"error": "A registered provider account is required."}), 404

    food = Food(
        provider_id=provider_id,
        type=food_type,
        quantity=quantity,
        freshness_score=freshness_score,
        location=location,
    )
    db.session.add(food)
    db.session.commit()
    return jsonify({"message": "Food posted successfully.", "food_id": food.id}), 201


@app.get("/food")
def get_food():
    status = request.args.get("status", "available").strip().lower()
    allowed_statuses = {"available", "picked up", "delivered"}
    if status not in allowed_statuses:
        return jsonify({"error": "Unsupported food status filter."}), 400

    posts = Food.query.filter_by(status=status).order_by(Food.id.desc()).all()
    return jsonify({
        "food_posts": [{
            "id": food.id,
            "provider_id": food.provider_id,
            "type": food.type,
            "quantity": food.quantity,
            "freshness_score": food.freshness_score,
            "location": food.location,
            "status": food.status,
        } for food in posts]
    })


@app.post("/volunteer")
def register_volunteer():
    data, error = json_body()
    if error:
        return error

    try:
        user_id = int(data.get("user_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "user_id must be a valid integer."}), 400

    user = db.session.get(User, user_id)
    if user is None or user.role != "volunteer":
        return jsonify({"error": "A registered volunteer account is required."}), 404

    vehicle_type = data.get("vehicle_type")
    if vehicle_type is not None and (not isinstance(vehicle_type, str) or len(vehicle_type) > 50):
        return jsonify({"error": "vehicle_type must be a string of at most 50 characters."}), 400

    volunteer = Volunteer(user_id=user_id, vehicle_type=vehicle_type.strip() if vehicle_type else None)
    db.session.add(volunteer)
    db.session.commit()
    return jsonify({"message": "Volunteer registered successfully.", "volunteer_id": volunteer.id}), 201


@app.post("/recipient")
def register_recipient():
    data, error = json_body()
    if error:
        return error

    try:
        user_id = int(data.get("user_id"))
        number_of_people = int(data.get("number_of_people"))
    except (TypeError, ValueError):
        return jsonify({"error": "user_id and number_of_people must be valid integers."}), 400

    user = db.session.get(User, user_id)
    if user is None or user.role != "recipient":
        return jsonify({"error": "A registered recipient account is required."}), 404
    if number_of_people <= 0:
        return jsonify({"error": "number_of_people must be greater than zero."}), 400

    requirements = data.get("food_requirements")
    if requirements is not None and (not isinstance(requirements, str) or len(requirements) > 200):
        return jsonify({"error": "food_requirements must be a string of at most 200 characters."}), 400

    recipient = Recipient(
        user_id=user_id,
        food_requirements=requirements.strip() if requirements else None,
        number_of_people=number_of_people,
    )
    db.session.add(recipient)
    db.session.commit()
    return jsonify({"message": "Recipient registered successfully.", "recipient_id": recipient.id}), 201


if __name__ == "__main__":
    app.run(debug=False)
