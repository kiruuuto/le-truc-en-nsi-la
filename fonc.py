import sqlite3

def connect_db(db_name):
    """bah ca se connecte quoi."""
    conn = sqlite3.connect(db_name)
    print(f"Connecté à : {db_name}")
    return conn

#Fonctions pour manipuler la table Clients

def add_user(conn, username, email):
    """Ajoute un utilisateur à la base de données."""

    cursor = conn.cursor()

    # Vérifier si l'utilisateur ou l'email existe déjà
    cursor.execute("SELECT 1 FROM Clients WHERE username = ? OR email = ?", (username, email))
    exists = cursor.fetchone()
    if exists:
        print(f"L'utilisateur '{username}' avec l'email '{email}' existe déjà.")
        return False  
    else:
        cursor.execute("INSERT INTO Clients (username, email) VALUES (?, ?)", (username, email))
    conn.commit()
    print(f"User {username} added successfully.")

def delete_user(conn, user_id):
    """Supprime un utilisateur de la base de données."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clients WHERE username = ?", (user_id,))
        conn.commit()
        print(f"User {user_id} supprimé de Clients")
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")

# Fonctions pour manipuler la table Demandes
def add_demande(conn, user_id, request_text):
    """Ajoute une demande à la base de données."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Demandes (user_id, request_text) VALUES (?, ?)", (user_id, request_text))
    conn.commit()
    print(f"Request added for user {user_id}")

# Fonctions pour manipuler la table Projets
def add_projet(conn, idClient, idProjet, intitule, deadline, commentaire):
    """Ajoute un projet à la base de données."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Projets (idClient, idProjet, intitule, deadline, description) VALUES (?, ?, ?, ?, ?)", (idClient, idProjet, intitule, deadline, commentaire))
    conn.commit()
    print(f"Project {intitule} added successfully.")

conn = connect_db("testprojet")

with conn:
    add_projet(conn, 1, 1, "Projet Alpha", "2024-12-31", "Premier projet important")