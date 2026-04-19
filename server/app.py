import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# Config
EXPECTED_API_KEY = "GROUPE10-KEY"

# Base de données simulée avec des dictionnaires pour recherche rapide
db = {
    "students": {
        "MAT-2026-001": {"id": "MAT-2026-001", "name": "Saul Eric", "email": "sauleric34@gmail.com"},
        "MAT-2026-002": {"id": "MAT-2026-002", "name": "Alice Martin", "email": "alice.m@email.com"},
        "MAT-2026-003": {"id": "MAT-2026-003", "name": "Bob Durand", "email": "bob.d@email.com"},
        "MAT-2026-004": {"id": "MAT-2026-004", "name": "Charlie King", "email": "charlie@email.com"},
        "MAT-2026-005": {"id": "MAT-2026-005", "name": "Eva Solar", "email": "eva.s@email.com"},
        "MAT-2026-006": {"id": "MAT-2026-006", "name": "Frank Castle", "email": "frank.c@email.com"},
        "MAT-2026-007": {"id": "MAT-2026-007", "name": "Grace Hopper", "email": "grace@email.com"},
    },
    "subjects": {
        "MATH101": {"id": "MATH101", "name": "Mathématiques", "credits": 6},
        "API202": {"id": "API202", "name": "Développement API REST", "credits": 4},
        "CYB303": {"id": "CYB303", "name": "Cybersécurité", "credits": 3},
        "NET404": {"id": "NET404", "name": "Réseaux & Télécoms", "credits": 4},
        "ARC505": {"id": "ARC505", "name": "Architecture des Systèmes", "credits": 3},
    },
    "grades": [
        # Saul
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-001", "subject_id": "API202", "cc": 15, "exam": 19, "grade": 17.4, "date": "2026-04-10"},
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-001", "subject_id": "MATH101", "cc": 12, "exam": 15, "grade": 13.8, "date": "2026-04-12"},
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-001", "subject_id": "NET404", "cc": 14, "exam": 17, "grade": 15.8, "date": "2026-04-14"},
        # Alice
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-002", "subject_id": "API202", "cc": 10, "exam": 14, "grade": 12.4, "date": "2026-04-10"},
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-002", "subject_id": "CYB303", "cc": 16, "exam": 16, "grade": 16.0, "date": "2026-04-15"},
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-002", "subject_id": "ARC505", "cc": 13, "exam": 16, "grade": 14.8, "date": "2026-04-16"},
        # Bob
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-003", "subject_id": "MATH101", "cc": 8, "exam": 10, "grade": 9.2, "date": "2026-04-12"},
        {"id": str(uuid.uuid4()), "student_id": "MAT-2026-003", "subject_id": "CYB303", "cc": 10, "exam": 11, "grade": 10.6, "date": "2026-04-15"},
    ]
}

# ─────────────────────────────────────────────
#  MIDDLEWARE / SECURITY
# ─────────────────────────────────────────────
@app.before_request
def check_api_key():
    if request.path.startswith('/static'):
        return
    key = request.headers.get("X-API-Key")
    if key != EXPECTED_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

# ─────────────────────────────────────────────
#  ÉTUDIANTS
# ─────────────────────────────────────────────
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(list(db["students"].values())), 200

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    db["students"][data['id']] = data
    return jsonify({"status": "success"}), 201

@app.route('/students/<id>', methods=['PUT', 'PATCH'])
def update_student(id):
    if id not in db["students"]:
        return jsonify({"error": "Not found"}), 404
    db["students"][id].update(request.json)
    return jsonify({"status": "success"}), 200

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    if id in db["students"]:
        del db["students"][id]
        db["grades"] = [g for g in db["grades"] if g['student_id'] != id]
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Not found"}), 404

# ─────────────────────────────────────────────
#  MATIÈRES (SUBJECTS)
# ─────────────────────────────────────────────
@app.route('/subjects', methods=['GET'])
def get_subjects():
    return jsonify(list(db["subjects"].values())), 200

@app.route('/subjects', methods=['POST'])
def add_subject():
    data = request.json
    db["subjects"][data['id']] = data
    return jsonify({"status": "success"}), 201

@app.route('/subjects/<id>', methods=['PUT', 'PATCH'])
def update_subject(id):
    if id not in db["subjects"]:
        return jsonify({"error": "Not found"}), 404
    db["subjects"][id].update(request.json)
    return jsonify({"status": "success"}), 200

@app.route('/subjects/<id>', methods=['DELETE'])
def delete_subject(id):
    if id in db["subjects"]:
        del db["subjects"][id]
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Not found"}), 404

# ─────────────────────────────────────────────
#  NOTES / CRÉDITS (GRADES)
# ─────────────────────────────────────────────
def calculate_grade(data):
    cc = float(data.get('cc', 0))
    exam = float(data.get('exam', 0))
    # Formule standard: 40% CC + 60% Exam
    data['grade'] = round((cc * 0.4) + (exam * 0.6), 2)
    return data

@app.route('/grades', methods=['GET'])
def get_all_grades():
    return jsonify(db["grades"]), 200

@app.route('/grades', methods=['POST'])
def add_grade():
    data = request.json
    data['id'] = str(uuid.uuid4())
    calculate_grade(data)
    db["grades"].append(data)
    return jsonify({"status": "success", "id": data['id']}), 201

@app.route('/grades/<id>', methods=['PUT', 'PATCH'])
def update_grade(id):
    for i, g in enumerate(db["grades"]):
        if g.get('id') == id:
            db["grades"][i].update(request.json)
            calculate_grade(db["grades"][i])
            return jsonify({"status": "success"}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/students/<student_id>/grades', methods=['GET'])
def get_student_grades(student_id):
    return jsonify([g for g in db["grades"] if g['student_id'] == student_id]), 200

@app.route('/students/<student_id>/grades', methods=['POST'])
def add_student_grade(student_id):
    data = request.json
    data['id'] = str(uuid.uuid4())
    data['student_id'] = student_id
    calculate_grade(data)
    db["grades"].append(data)
    return jsonify({"status": "success", "id": data['id']}), 201

@app.route('/grades/<grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    initial_len = len(db["grades"])
    db["grades"] = [g for g in db["grades"] if g.get('id') != grade_id]
    if len(db["grades"]) < initial_len:
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)