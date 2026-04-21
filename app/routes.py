from flask import Blueprint, request, jsonify
from .models import Student
from . import db

main = Blueprint('main', __name__)

# =========================
# HELPERS
# =========================
def error_response(message, status_code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code


def success_response(message, data=None, status_code=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), status_code


# =========================
# REGISTER
# =========================
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return error_response("All fields are required")

    if Student.query.filter_by(username=username).first():
        return error_response("Username already exists")

    if Student.query.filter_by(email=email).first():
        return error_response("Email already exists")

    student = Student(username=username, email=email, password=password)
    db.session.add(student)
    db.session.commit()

    return success_response("User Registration successful", None, 201)


# =========================
# LOGIN
# =========================
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return error_response("Username and password required")

    user = Student.query.filter_by(username=username, password=password).first()

    if not user:
        return error_response("Invalid credentials", 401)

    return success_response("Login successful", {
        "id": user.id,
        "username": user.username
    })


# =========================
# SEARCH
# =========================
@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')

    if not query or query.strip() == "":
        return error_response("Query parameter required")

    results = Student.query.filter(Student.username.contains(query)).all()

    data = [{"id": u.id, "username": u.username} for u in results]

    return success_response("Search results", data)


# =========================
# STUDENTS (IMPORTANT FIX HERE)
# =========================
@main.route('/students', methods=['GET', 'POST'])
def students():

    # GET ALL
    if request.method == 'GET':
        students_list = Student.query.all()

        data = [
            {
                "id": s.id,
                "username": s.username,
                "email": s.email
            } for s in students_list
        ]

        # ✅ FIXED: must return "data" not "result"
        return success_response("Students fetched", data)

    # CREATE
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return error_response("All fields required")

    if Student.query.filter_by(username=username).first():
        return error_response("Username already exists")

    if Student.query.filter_by(email=email).first():
        return error_response("Email already exists")

    student = Student(username=username, email=email, password=password)
    db.session.add(student)
    db.session.commit()

    return success_response("Student created", None, 201)


# =========================
# GET SINGLE
# =========================
@main.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)

    if not student:
        return error_response("Student not found", 404)

    return success_response("Student found", {
        "id": student.id,
        "username": student.username,
        "email": student.email
    })


# =========================
# UPDATE
# =========================
@main.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)

    if not student:
        return error_response("Student not found", 404)

    data = request.get_json(silent=True) or {}

    new_username = data.get("username")
    new_email = data.get("email")

    if new_username:
        existing = Student.query.filter_by(username=new_username).first()
        if existing and existing.id != id:
            return error_response("Username already exists")
        student.username = new_username

    if new_email:
        existing = Student.query.filter_by(email=new_email).first()
        if existing and existing.id != id:
            return error_response("Email already exists")
        student.email = new_email

    db.session.commit()

    return success_response("Updated successfully", {
        "id": student.id,
        "username": student.username,
        "email": student.email
    })


# =========================
# DELETE
# =========================
@main.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)

    if not student:
        return error_response("Student not found", 404)

    db.session.delete(student)
    db.session.commit()

    return success_response("Deleted successfully")


# =========================
# HEALTH CHECK
# =========================
@main.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})
