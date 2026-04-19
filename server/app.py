from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de données temporaire en mémoire
db = {
    "students": [],
    "grades": []
}

@app.route('/students', methods=['GET'])
def list_students():
    return jsonify(db["students"]), 200

@app.route('/students', methods=['POST'])
def add_student():
    student = request.json
    # On vérifie si les champs requis sont là
    if not student.get("id") or not student.get("name"):
        return jsonify({"error": "Données incomplètes"}), 400
    
    db["students"].append(student)
    return jsonify({"message": "Étudiant créé avec succès"}), 201

@app.route('/grades', methods=['POST'])
def add_grade():
    grade = request.json
    db["grades"].append(grade)
    return jsonify({"message": "Note enregistrée avec succès"}), 201

if __name__ == '__main__':
    # On lance sur le port 5000 comme défini dans ta spec Postman
    print("Serveur de Gestion des Notes démarré sur http://localhost:5000")
    app.run(port=5000, debug=True)