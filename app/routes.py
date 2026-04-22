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
    try:
        data = request.get_json(silent=True)

        if not data:
            return error_response("Payload missing", 400)

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not username or not email or not password:
            return error_response("All fields are required", 400)

        if Student.query.filter_by(username=username).first():
            return error_response("Username already exists", 400)

        if Student.query.filter_by(email=email).first():
            return error_response("Email already exists", 400)

        student = Student(username=username, email=email, password=password)
        db.session.add(student)
        db.session.commit()

        return success_response("User registered", None, 201)

    except Exception:
        db.session.rollback()
        return error_response("Server error", 500)


# =========================
# LOGIN
# =========================
@main.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True)

        if not data:
            return error_response("Payload missing", 400)

        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return error_response("Username and password required", 400)

        user = Student.query.filter_by(username=username, password=password).first()

        if not user:
            return error_response("Invalid credentials", 401)

        return success_response("Login success", {
            "id": user.id,
            "username": user.username
        })

    except Exception:
        return error_response("Server error", 500)


# =========================
# SEARCH
# =========================
@main.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q')

        if not query or query.strip() == "":
            return error_response("Query required", 400)

        results = Student.query.filter(Student.username.contains(query)).all()

        data = [{"id": u.id, "username": u.username} for u in results]

        return success_response("Results", data)

    except Exception:
        return error_response("Server error", 500)


# =========================
# STUDENTS
# =========================
@main.route('/students', methods=['GET', 'POST'])
def students():

    # GET
    if request.method == 'GET':
        students = Student.query.all()

        data = [
            {"id": s.id, "username": s.username, "email": s.email}
            for s in students
        ]

        return success_response("Fetched", data)

    # POST
    data = request.get_json(silent=True)

    if not data:
        return error_response("Payload missing", 400)

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return error_response("Fields required", 400)

    if Student.query.filter_by(username=username).first():
        return error_response("Duplicate username", 400)

    if Student.query.filter_by(email=email).first():
        return error_response("Duplicate email", 400)

    student = Student(username=username, email=email, password=password)
    db.session.add(student)
    db.session.commit()

    return success_response("Created", None, 201)


# =========================
# GET SINGLE
# =========================
@main.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = db.session.get(Student, id)

    if not student:
        return error_response("Not found", 404)

    return success_response("Found", {
        "id": student.id,
        "username": student.username,
        "email": student.email
    })


# =========================
# UPDATE
# =========================
@main.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = db.session.get(Student, id)

    if not student:
        return error_response("Not found", 404)

    data = request.get_json(silent=True) or {}

    new_username = data.get("username", student.username).strip()
    new_email = data.get("email", student.email).strip()

    existing_user = Student.query.filter(
        Student.username == new_username,
        Student.id != id
    ).first()

    if existing_user:
        return error_response("Username already exists", 400)

    # 🔴 CHECK DUPLICATE EMAIL
    existing_email = Student.query.filter(
        Student.email == new_email,
        Student.id != id
    ).first()

    if existing_email:
        return error_response("Email already exists", 400)

    student.username = new_username
    student.email = new_email

    db.session.commit()

    return success_response("Updated", {
        "id": student.id,
        "username": student.username,
        "email": student.email
    })
# =========================
# DELETE
# =========================
@main.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = db.session.get(Student, id)

    if not student:
        return error_response("Not found", 404)

    db.session.delete(student)
    db.session.commit()

    return success_response("Deleted")


@main.route('/health', methods=['GET'])
def health_check():
    try:
        # 1. DB check
        db.session.execute(db.text("SELECT 1"))

        # 2. Basic route existence check (lightweight)
        routes = {
            "register": "/register",
            "login": "/login",
            "search": "/search",
            "students": "/students"
        }

        return success_response("System Healthy", {
            "status": "UP",
            "database": "CONNECTED",
            "routes": routes
        })

    except Exception as e:
        return error_response(f"System unhealthy: {str(e)}", 500)