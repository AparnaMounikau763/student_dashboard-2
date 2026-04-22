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
# HEALTH CHECK
# =========================
@main.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


# =========================
# REGISTER
# =========================
@main.route('/register', methods=['POST'])
def register():
    try:
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

    except Exception as e:
        db.session.rollback()
        return error_response(f"Server error: {str(e)}", 500)


# =========================
# LOGIN
# =========================
@main.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True) or {}

        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return error_response("Username and password required")

        user = Student.query.filter_by(
            username=username,
            password=password
        ).first()

        if not user:
            return error_response("Invalid credentials", 401)

        return success_response("Login successful", {
            "id": user.id,
            "username": user.username
        })

    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


# =========================
# SEARCH
# =========================
@main.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q')

        if not query or query.strip() == "":
            return error_response("Query parameter required")

        results = Student.query.filter(Student.username.contains(query)).all()

        data = [
            {"id": u.id, "username": u.username}
            for u in results
        ]

        return success_response("Search results", data)

    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


# =========================
# STUDENTS (GET + POST)
# =========================
@main.route('/students', methods=['GET', 'POST'])
def students():
    try:

        # -----------------
        # GET ALL STUDENTS
        # -----------------
        if request.method == 'GET':
            students_list = Student.query.all()

            data = [
                {
                    "id": s.id,
                    "username": s.username,
                    "email": s.email
                }
                for s in students_list
            ]

            return success_response("Students fetched", data)

        # -----------------
        # CREATE STUDENT
        # -----------------
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

    except Exception as e:
        db.session.rollback()
        return error_response(f"Server error: {str(e)}", 500)


# =========================
# GET SINGLE STUDENT
# =========================
@main.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    try:
        student = db.session.get(Student, id)

        if not student:
            return error_response("Student not found", 404)

        return success_response("Student found", {
            "id": student.id,
            "username": student.username,
            "email": student.email
        })

    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


# =========================
# UPDATE STUDENT
# =========================
@main.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        student = db.session.get(Student, id)

        if not student:
            return error_response("Student not found", 404)

        data = request.get_json(silent=True) or {}

        new_username = data.get("username")
        new_email = data.get("email")

        # username update
        if new_username:
            new_username = new_username.strip()
            existing = Student.query.filter_by(username=new_username).first()
            if existing and existing.id != id:
                return error_response("Username already exists")
            student.username = new_username

        # email update
        if new_email:
            new_email = new_email.strip()
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

    except Exception as e:
        db.session.rollback()
        return error_response(f"Server error: {str(e)}", 500)


# =========================
# DELETE STUDENT
# =========================
@main.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = db.session.get(Student, id)

        if not student:
            return error_response("Student not found", 404)

        db.session.delete(student)
        db.session.commit()

        return success_response("Deleted successfully")

    except Exception as e:
        db.session.rollback()
        return error_response(f"Server error: {str(e)}", 500)
