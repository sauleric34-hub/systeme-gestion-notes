from new_specification_sdk import NewSpecificationSdk
from new_specification_sdk.models import Student, Grade

# 1. Initialisation
sdk = NewSpecificationSdk(api_key="GROUPE10-KEY")
sdk.set_base_url("http://127.0.0.1:5000")

try:
    # 2. Test Étudiant
    nouveau_etudiant = Student(
        id="MAT-2026-001",
        name="Saul Eric",
        email="sauleric34@gmail.com"
    )
    
    print("Envoi de l'étudiant via create_students...")
    # Le nom exact trouvé dans StudentsService
    sdk.students.create_students(nouveau_etudiant) 
    print("Succès : Étudiant envoyé.")

    # 3. Test Note
    nouvelle_note = Grade(
        student_id="MAT-2026-001",
        subject="Architecture API",
        score=18.5
    )
    
    print("\nEnvoi de la note via create_grades...")
    # On suit la même logique de nommage pour le service grades
    sdk.grades.create_grades(nouvelle_note)
    print("Succès : Note envoyée.")

    # 4. Vérification : Récupérer la liste
    print("\nRécupération de la liste des étudiants...")
    liste = sdk.students.get_students()
    print(f"Liste actuelle : {liste}")

except Exception as e:
    print(f"Erreur : {e}")