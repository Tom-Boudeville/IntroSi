# Bienvenue aux Nouveaux Habitants – API

## Description du Projet

Ce projet est une **API REST** développée avec **Flask**.  
Elle permet de **gérer les résidents d'une ville** et de **distribuer des cadeaux** aux nouveaux arrivants célébrant leur première année dans la commune.

L’application :
- Sélectionne les habitants **éligibles** (installés depuis plus d’un an).
- Trouve le **cadeau approprié** selon leur **tranche d’âge**.
- Stocke les données **en mémoire** à l’aide de listes Python.

---

## Livrables Attendus (Rappel du TP)

- `server.py` → Code Python du serveur Flask  
- `index.html` → Interface HTML/JS de test  
- `README.md` → Ce fichier de documentation

---

## Lancer l’API et la Tester

### 1️⃣ Prérequis
- **Python 3.x** installé sur votre machine.

### 2️⃣ Installation des Dépendances
Installez Flask avec la commande :

```bash
pip install flask
```

### 3️⃣ Lancement du Serveur
Exécutez le fichier Python principal :

```bash
python server.py
```

L’API sera accessible à l’adresse :  
👉 [http://127.0.0.1:5050](http://127.0.0.1:5050)

---

## Tester l’API

Vous pouvez tester les routes avec **cURL**, **Postman** ou directement via l’interface web (`index.html`).

### 🔹 Exemple avec cURL

**Lister tous les habitants :**
```bash
curl -X GET http://127.0.0.1:5050/api/v1/residents
```

**Ajouter un habitant :**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"id": 6, "prenom": "Alice", "age": 35, "date_arrivee": "2025-01-01"}' http://127.0.0.1:5050/api/v1/residents
```

---

## 📚 Endpoints Disponibles

### 1️⃣ Gestion des Résidents (`/api/v1/residents`)

| Méthode | Endpoint | Description |
|----------|-----------|-------------|
| **GET** | `/api/v1/residents` | Liste de tous les habitants |
| **GET** | `/api/v1/residents/<id>` | Détails d’un habitant |
| **POST** | `/api/v1/residents` | Ajoute un nouvel habitant |
| **PUT** | `/api/v1/residents/<id>` | Modifie un habitant |
| **DELETE** | `/api/v1/residents/<id>` | Supprime un habitant |

---

### 2️⃣ Attribution des Cadeaux

| Méthode | Endpoint | Description |
|----------|-----------|-------------|
| **GET** | `/api/v1/eligible` | Liste des habitants éligibles et cadeaux correspondants |
| **POST** | `/api/v1/attributions` | Génère les attributions de cadeaux du jour (aléatoirement) |

---

## Logique Métier

### Éligibilité
Un résident est **éligible** s’il a emménagé **depuis plus de 365 jours**.

### Attribution des Cadeaux
- Chaque cadeau correspond à une **tranche d’âge** (`age_min`, `age_max`).
- Lors de la création des attributions, un **cadeau aléatoire** est choisi parmi ceux disponibles pour le résident.
- Un résident **ne peut recevoir qu’un seul cadeau**.