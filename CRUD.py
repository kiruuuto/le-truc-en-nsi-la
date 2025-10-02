import sqlite3



'''

faudrait faire 2 fonctions add delete + 3 fonctions modifier

au lieu de 3*3 fonctions 

on passe de 9 fonctions à 5 fonctions




pour les 3 tables faut pouvoir ajouter supprimer et modifier

soit on fait 3 fonctions add delete modify avec pour chaque tables

soit on fait 2 fonctions add delete ou on modifie juste la table, on la met en variable
et 3 fonctions modify pour chaque table


'''







def connect_db(db_name):
    """bah ca se connecte quoi."""
    conn = sqlite3.connect(db_name)
    print(f"Connecté à : {db_name}")
    return conn

#Fonctions pour manipuler la table Clients

def read_users(conn):
    """Lit et affiche tous les utilisateurs de la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

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

def modify_user(conn, idClient, new_username=None, new_email=None):
    """Modifie les détails d'un utilisateur dans la base de données."""
    cursor = conn.cursor()
    updates = []
    params = []

    if new_username:
        updates.append("username = ?")
        params.append(new_username)
    if new_email:
        updates.append("email = ?")
        params.append(new_email)

    params.append(idClient)
    sql = f"UPDATE Clients SET {', '.join(updates)} WHERE username = ?"
    
    cursor.execute(sql, params)
    conn.commit()
    print(f"User {idClient} updated successfully.")

# Fonctions pour manipuler la table Demandes

def read_demandes(conn):
    """Lit et affiche toutes les demandes de la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Demandes")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def add_demande(conn, idClient, description):
    """Ajoute une demande à la base de données Demandes."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Demandes (idClient, request_text) VALUES (?, ?)", (idClient, description))
    conn.commit()
    print(f"Request added for user {idClient}")

def delete_demande(conn, idProjet):
    """Supprime une demande de la base de données."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Demandes WHERE id = ?", (idProjet,))
    conn.commit()
    print(f"La demande {idProjet} supprimé de Demandes")

def modify_demande(conn, new_username=None, new_email=None, new_intitule=None, new_deadline=None, new_description=None):
    """Modifier une demande de la base de données"""
    cursor = conn.cursor()
    updates = []
    params = []

    if new_username:
        updates.append("username = ?")
        params.append(new_username)
    
    if new_email:
        updates.append("email = ?")
        params.append(new_email)

    if new_intitule:
        updates.append("intitule = ?")
        params.append(new_intitule)
    
    if new_deadline:
        updates.append("deadline = ?")
        params.append(new_deadline)
    
    if new_description:
        updates.append("description = ?")
        params.append(new_description)
    
    cursor.execute("UPDATE Demandes SET")
    pass

'''

FAUT UTILISER CE TEMPLATE 

def modify_user(conn, idClient, new_username=None, new_email=None):
    """Modifie les détails d'un utilisateur dans la base de données."""
    cursor = conn.cursor()
    updates = []
    params = []

    if new_username:
        updates.append("username = ?")
        params.append(new_username)
    if new_email:
        updates.append("email = ?")
        params.append(new_email)

    params.append(idClient)
    sql = f"UPDATE Clients SET {', '.join(updates)} WHERE username = ?"
    
    cursor.execute(sql, params)
    conn.commit()
    print(f"User {idClient} updated successfully.")
'''

# Fonctions pour manipuler la table Projets

def read_projets(conn):
    """Lit et affiche tous les projets de la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Projets")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def add_projet(conn, idClient, idProjet, intitule, deadline, commentaire):
    """Ajoute un projet à la base de données."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Projets (idClient, idProjet, intitule, deadline, description) VALUES (?, ?, ?, ?, ?)", (idClient, idProjet, intitule, deadline, commentaire))
    conn.commit()
    print(f"Project {intitule} added successfully.")

def delete_projet(conn, idProjet):
    """Supprime un projet de la base de données."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Projets WHERE idProjet = ?", (idProjet,))
    conn.commit()
    print(f"Project {idProjet} supprimé de Projets")

def modify_projet(conn, idProjet, new_intitule=None, new_deadline=None, new_description=None):
    """Modifie les détails d'un projet dans la base de données."""
    cursor = conn.cursor()
    updates = []
    params = []

    if new_intitule:
        updates.append("intitule = ?")
        params.append(new_intitule)
        
    if new_deadline:
        updates.append("deadline = ?")
        params.append(new_deadline)

    if new_description:
        updates.append("description = ?")
        params.append(new_description)

    params.append(idProjet)
    sql = f"UPDATE Projets SET {', '.join(updates)} WHERE idProjet = ?"
    
    cursor.execute(sql, params)
    conn.commit()
    print(f"Project {idProjet} updated successfully.")

conn = connect_db("testprojet")

""""""  
