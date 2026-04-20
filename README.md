# 🎓 Keyce Grading Pro - Système de Gestion Académique (V1.0)
**Expertise : Architecture REST & Développement d'Interfaces Graphiques**

## 📖 Introduction Globale
Ce projet représente l'aboutissement d'un travail sur la séparation des préoccupations (Separation of Concerns). Nous avons conçu une application capable de gérer l'intégralité du cycle de vie des données académiques d'un établissement, en s'appuyant sur une communication Client-Serveur robuste.

---

## 🛠 Analyse de l'Architecture Logicielle

### 1. Le choix stratégique du SDK (Software Development Kit)
Contrairement à une approche directe par requêtes HTTP éparpillées dans le code, nous avons opté pour la génération d'un **SDK**. 
- **Abstraction de Couche :** L'interface graphique n'a aucune connaissance du protocole HTTP. Elle appelle des méthodes Python natives. Si nous passons de REST à GraphQL demain, seule la couche SDK change, pas l'application visuelle.
- **Robustesse :** Le SDK utilise des modèles de données (Pydantic) qui garantissent que chaque champ (ID, Nom, Note) est au bon format avant d'être envoyé sur le réseau.
- **Productivité :** Pour un développeur tiers, intégrer nos services devient un jeu d'enfant : il suffit d'importer la bibliothèque et d'utiliser l'autocomplétion.

### 2. Sémantique HTTP : Pourquoi POST et non GET pour les actions ?
Nous avons appliqué les standards de l'industrie :
- **Sécurité des données :** Le GET expose les données dans les logs du serveur et l'historique du navigateur via l'URL. Pour enregistrer un étudiant, le **POST** est impératif car il transporte les informations dans le corps (Body) chiffré.
- **Intégrité :** Le POST est non-idempotent par nature dans ce contexte (ajouter deux fois le même étudiant crée une erreur contrôlée), ce qui est idéal pour la gestion de base de données.

### 3. Le rôle pivot de Postman en phase de R&D
Postman n'a pas été un simple outil de test, mais notre **référence de documentation**. 
- **Contrat API :** Il nous a permis de définir que le serveur doit répondre un code `201 Created` en cas de succès et un `400 Bad Request` en cas d'erreur de format.
- **Débogage isolé :** En cas de bug dans l'application visuelle, Postman nous permet de vérifier si le problème vient du serveur ou de l'interface.

---

## 💻 Fonctionnalités Avancées (CRUD & UX)
L'interface graphique, développée avec **CustomTkinter**, offre une expérience utilisateur fluide :
- **Dashboard Dynamique :** Une vue d'ensemble qui se rafraîchit sans rechargement de page grâce à une gestion d'état interne.
- **Gestion du Cycle de Vie (CRUD) :**
    - *Create* : Formulaire d'inscription intelligent.
    - *Read* : Consultation fluide via une liste scrollable.
    - *Delete* : Suppression sécurisée avec cascade sur les données liées.
    - *Update* : Possibilité de modifier les informations via le SDK.

---

## 🚀 Guide de Déploiement Rapide
1. **Démarrage du Cerveau (Serveur) :** ```bash
   python server/app.py
   ```
2. **Liaison du SDK (Mode Éditable) :**
   ```bash
   pip install -e sdk/
   ```
3. **Lancement du Frontend :**
   ```bash
   python main_app.py
   ```
EOFcat <<EOF > README.md
# 🎓 Keyce Grading Pro - Système de Gestion Académique (V1.0)
**Expertise : Architecture REST & Développement d'Interfaces Graphiques**

## 📖 Introduction Globale
Ce projet représente l'aboutissement d'un travail sur la séparation des préoccupations (Separation of Concerns). Nous avons conçu une application capable de gérer l'intégralité du cycle de vie des données académiques d'un établissement, en s'appuyant sur une communication Client-Serveur robuste.

---

## 🛠 Analyse de l'Architecture Logicielle

### 1. Le choix stratégique du SDK (Software Development Kit)
Contrairement à une approche directe par requêtes HTTP éparpillées dans le code, nous avons opté pour la génération d'un **SDK**. 
- **Abstraction de Couche :** L'interface graphique n'a aucune connaissance du protocole HTTP. Elle appelle des méthodes Python natives. Si nous passons de REST à GraphQL demain, seule la couche SDK change, pas l'application visuelle.
- **Robustesse :** Le SDK utilise des modèles de données (Pydantic) qui garantissent que chaque champ (ID, Nom, Note) est au bon format avant d'être envoyé sur le réseau.
- **Productivité :** Pour un développeur tiers, intégrer nos services devient un jeu d'enfant : il suffit d'importer la bibliothèque et d'utiliser l'autocomplétion.

### 2. Sémantique HTTP : Pourquoi POST et non GET pour les actions ?
Nous avons appliqué les standards de l'industrie :
- **Sécurité des données :** Le GET expose les données dans les logs du serveur et l'historique du navigateur via l'URL. Pour enregistrer un étudiant, le **POST** est impératif car il transporte les informations dans le corps (Body) chiffré.
- **Intégrité :** Le POST est non-idempotent par nature dans ce contexte (ajouter deux fois le même étudiant crée une erreur contrôlée), ce qui est idéal pour la gestion de base de données.

### 3. Le rôle pivot de Postman en phase de R&D
Postman n'a pas été un simple outil de test, mais notre **référence de documentation**. 
- **Contrat API :** Il nous a permis de définir que le serveur doit répondre un code `201 Created` en cas de succès et un `400 Bad Request` en cas d'erreur de format.
- **Débogage isolé :** En cas de bug dans l'application visuelle, Postman nous permet de vérifier si le problème vient du serveur ou de l'interface.

---

## 💻 Fonctionnalités Avancées (CRUD & UX)
L'interface graphique, développée avec **CustomTkinter**, offre une expérience utilisateur fluide :
- **Dashboard Dynamique :** Une vue d'ensemble qui se rafraîchit sans rechargement de page grâce à une gestion d'état interne.
- **Gestion du Cycle de Vie (CRUD) :**
    - *Create* : Formulaire d'inscription intelligent.
    - *Read* : Consultation fluide via une liste scrollable.
    - *Delete* : Suppression sécurisée avec cascade sur les données liées.
    - *Update* : Possibilité de modifier les informations via le SDK.

---

## 🚀 Guide de Déploiement Rapide
1. **Démarrage du Cerveau (Serveur) :** ```bash
   python server/app.py
   ```
2. **Liaison du SDK (Mode Éditable) :**
   ```bash
   pip install -e sdk/
   ```
3. **Lancement du Frontend :**
   ```bash
   python main_app.py
   ```
