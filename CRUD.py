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






def debug(variable, message):
    """Fonction de debug pour afficher des messages conditionnellement."""
    if variable:
        print(f"[DEBUG] {message}")

def connect_db(db_name, debug_variable=False):
    """Connection a la base de donnée sqlite."""
    conn = sqlite3.connect(db_name)
    debug(debug_variable, f"Connecté à : {db_name}")
    return conn

#Fonctions pour manipuler la table Clients

def read_users(conn):
    """Lit et affiche tous les utilisateurs de la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def add_user(conn, username, email, debug_variable=False):
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
    debug(debug_variable, f"L'utilisateur {username} a été ajouté dans Clients.")

def delete_user(conn, user_id, debug_variable=False):
    """Supprime un utilisateur de la base de données."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clients WHERE username = ?", (user_id,))
        conn.commit()
        debug(debug_variable,f"L'utilisateur {user_id} supprimé de Clients")
    except sqlite3.Error as e:
        debug(debug_variable, f"Error deleting user: {e}")

def modify_user(conn, idClient, new_username=None, new_email=None, debug_variable=False):
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
    debug(debug_variable, f"L'utilisateur {idClient} a été modifié.")

# Fonctions pour manipuler la table Demandes

def read_demandes(conn, debug_variable=False):
    """Lit et affiche toutes les demandes de la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Demandes")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def add_demande(conn, idClient, description, debug_variable=False):
    """Ajoute une demande à la base de données Demandes."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Demandes (idClient, description) VALUES (?, ?)", (idClient, description))
    conn.commit()
    debug(debug_variable, f"Request added for user {idClient}")

def delete_demande(conn, idProjet, debug_variable=False):
    """Supprime une demande de la base de données."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Demandes WHERE idProjet = ?", (idProjet,))
    conn.commit()
    debug(debug_variable, f"La demande {idProjet} supprimé de Demandes")

def modify_demande(conn, idProjet, new_username=None, new_email=None, new_intitule=None, new_deadline=None, new_description=None, debug_variable=False):
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
    params.append(idProjet)
    sql = f"UPDATE Demandes SET {', '.join(updates)} WHERE idProjet = ?"
    cursor.execute(sql, params)
    conn.commit()
    debug(debug_variable, f"La demande {idProjet} a été modifiée.")

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
    print(f"User {idClient} A éTé AHOUTé.")
'''

# Fonctions pour manipuler la table Projets

def read_projets(conn, debug_variable=False):
    """Lit et affiche tous les projets de la base de données."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Projets")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def add_projet(conn, idClient, idProjet, intitule, deadline, commentaire, debug_variable=False):
    """Ajoute un projet à la base de données."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Projets (idClient, idProjet, intitule, deadline, description) VALUES (?, ?, ?, ?, ?)", (idClient, idProjet, intitule, deadline, commentaire))
    conn.commit()
    debug(debug_variable, f"Project {intitule} added successfully.")

def delete_projet(conn, idProjet, debug_variable=False):
    """Supprime un projet de la base de données."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Projets WHERE idProjet = ?", (idProjet,))
    conn.commit()
    debug(debug_variable, f"Project {idProjet} supprimé de Projets")

def modify_projet(conn, idProjet, new_intitule=None, new_deadline=None, new_description=None, debug_variable=False):
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
    debug(debug_variable, f"Project {idProjet} a été ajouté.")


"""def add_record(conn, table_name, entetes, [entetes][valeurs]

"""  

if __name__ == "__main__":
    # Nom de la base de données
    db_name = "testprojet"

    # Connexion à la base de données
    conn = connect_db(db_name, debug_variable=True)
#------------------------------------ Test de l'ajout a la base de donnée dans les différentes tables -----------------------------------------------------------
    print("\n=== Ajout de données de test ===")
    try:
        add_user(conn, "test_user", "test@example.com", debug_variable=True)
        add_demande(conn, 1, "Nouvelle demande de test", debug_variable=True)
        add_projet(conn, 1, 99, "Projet test", "2025-12-31", "Description du projet test", debug_variable=True)
    except Exception as e:
        print(f"Erreur lors de l'ajout : {e}")
#-------------------------------------- Première lecture des tables : Les enregistrements ont bien été ajoutés ----------------------------------------------------------------------------
    print("\n=== Lecture des tables existantes ===")
    try:
        print("\n--- Clients ---")
        read_users(conn)

        print("\n--- Demandes ---")
        read_demandes(conn)

        print("\n--- Projets ---")
        read_projets(conn)
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
#-------------------------------------- Test de modifiaction d'enregistrements des différentes tables de la bdd -----------------------------------------------------------------------
    print("\n=== Modifications ===")
    try:
        modify_user(conn, "test_user", new_email="newmail@example.com", debug_variable=True)
        modify_demande(conn, 1, new_description="Demande mise à jour", debug_variable=True)
        modify_projet(conn, 99, new_description="Projet mis à jour", debug_variable=True)
    except Exception as e:
        print(f"Erreur lors de la modification : {e}")
#-------------------------------------- Seconde lecture des tables : Les enregistrements ont bien été modifiés----------------------------------------------------------------------------
    print("\n=== Lecture des tables existantes ===")
    try:
        print("\n--- Clients ---")
        read_users(conn)

        print("\n--- Demandes ---")
        read_demandes(conn)

        print("\n--- Projets ---")
        read_projets(conn)
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
#------------------------------------- Suppression d'enregistrements dans les tables de la bdd -----------------------------------------------------------------------------
    print("\n=== Suppressions ===")
    try:
        delete_user(conn, "test_user", debug_variable=True)
        delete_demande(conn, 1, debug_variable=True)
        delete_projet(conn, 99, debug_variable=True)
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")
#--------------------------------------- Derniere lecture : tous les enregistrements test ont bien été supprimés ---------------------------------------------------------------------------      
    print("\n=== Lecture des tables existantes ===")
    try:
        print("\n--- Clients ---")
        read_users(conn)

        print("\n--- Demandes ---")
        read_demandes(conn)

        print("\n--- Projets ---")
        read_projets(conn)
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")  
#------------------------------------------------------------------------------------------------------------------
    # Fermeture propre
    conn.close()
    print("\nConnexion fermée proprement")
