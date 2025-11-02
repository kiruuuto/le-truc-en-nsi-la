import sqlite3

nom_bdd = "testprojet"

def debug(
    variable: bool, 
    message: str
):
    """
    Affiche un message de debug si le paramètre 'variable' est True.

    Paramètres :
    -----------
    variable : bool
        Contrôle si le message est affiché.
    message : str
        Le message à afficher.
    """

    if variable:
        print(f"[DEBUG] {message}")

def connect_db(
    db_name: str, 
    debug_variable=False
):
    """
    Connecte à une base de données SQLite et retourne la connexion.

    Paramètres :
    -----------
    db_name : str
        Le nom du fichier de la base de données.
    debug_variable : bool, optionnel
        Si True, affiche un message de debug (par defaut False).

    Retour :
    -------
    sqlite3.connect
        Objet de connexion à la base de données.
    """

    conn = sqlite3.connect(db_name)
    debug(debug_variable, f"Connecte a : {db_name}")
    return conn

#Fonctions pour manipuler la table Clients

def show_users(
):
    """
    Lit et affiche tous les utilisateurs de la table Clients.

    Parameters
    ----------
    Ne prends rien en paramètre.
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, email FROM Clients")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

def add_user(
    username: str, 
    email: str, 
    debug_variable=False
):
    """
    Ajoute un nouvel utilisateur à la table Clients.

    Parameters
    ----------
    username : str
        Nom d'utilisateur à ajouter.
    email : str
        Email de l'utilisateur.
    debug_variable : bool, optionel
        Si True, affiche un message de debug (par defaut False).
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()

        # Vérifier si l'utilisateur ou l'email existe déjà
        cursor.execute("SELECT 1 FROM Clients WHERE username = ? OR email = ?", (username, email))
        exists = cursor.fetchone()
        if exists:
            print(f"L'utilisateur '{username}' avec l'email '{email}' existe deja.")
            return False  
        else:
            cursor.execute("INSERT INTO Clients (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        debug(debug_variable, f"L'utilisateur {username} a ete ajoute dans Clients.")

def delete_user(
    username: str, 
    debug_variable=False
):
    """
    Supprime un utilisateur de la table Clients.

    Parameters
    ----------
    username : str
        Nom d'utilisateur à supprimer.
    debug_variable : bool, optional
        Si True, affiche un message de debug (par defaut False).
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Clients WHERE username = ?", (username,))
            conn.commit()
            debug(debug_variable,f"L'utilisateur {username} supprime de Clients")
        except sqlite3.Error as e:
            debug(debug_variable, f"Error deleting user: {e}")

def modify_user(
    username=None, 
    new_username=None, 
    new_email=None, 
    debug_variable=False
):
    """
    Modifie les informations d'un utilisateur dans la table Clients.

    Parameters
    ----------
    username : str
        Nom d'utilisateur à modifier.
    new_username : str, optional
        Nouveau nom d'utilisateur.
    new_email : str, optional
        Nouvel email.
    debug_variable : bool, optional
        Si True, affiche un message de debug (par defaut False).
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        updates = []
        params = []

        if new_username:
            updates.append("username = ?")
            params.append(new_username)
        if new_email:
            updates.append("email = ?")
            params.append(new_email)

        params.append(username)
        sql = f"UPDATE Clients SET {', '.join(updates)} WHERE username = ?"
        
        cursor.execute(sql, params)
        conn.commit()
        debug(debug_variable, f"L'utilisateur {username} a ete modifie.")

# Fonctions pour manipuler la table Demandes

def show_demandes(
):
    """
    Lit et affiche toutes les demandes de la table Demandes.

    Parameters
    ----------
    Ne prends rien en paramètre.
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT C.username, C.email, D.intitule, D.deadline, D.description, D.accepted
        FROM Demandes D
        JOIN Clients C ON D.idClient = C.id
        """)
        rows = cursor.fetchall()
        for row in rows:
            if row[5] == 1:
                print(row[:5] + ("Accepted",))
            elif row[5] == 0:
                print(row[:5] + ("Not Accepted",))
            elif row[5] is None or row[5] == '' or row[5].upper() == "NULL":
                print(row[:5] + ("Pending",))
    pass

def add_demande(
    username: str,
    email : str,
    intitule: str,
    deadline: str, 
    description: str, 
    debug_variable=False
):
    """
    Ajoute une demande dans la table Demandes.

    Parameters
    ----------
    username : str
        Nom d'utilisateur de la demande.
    email : str
        Email de l'utilisateur.
    intitule : str
        Titre de la demande.
    deadline : str
        Date limite de la demande (format 'YYYY-MM-DD').
    description : str
        Description de la demande.
    debug_variable : bool, optional
        Si True, affiche un message de debug (par defaut False).
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        idClient = int(cursor.execute("SELECT id FROM Clients WHERE username = ? AND email = ?", (username,email)).fetchone()[0])
        cursor.execute("INSERT INTO Demandes (idClient, intitule, deadline, description) VALUES (?, ?, ?, ?)", (idClient, intitule, deadline, description))
        conn.commit()
        debug(debug_variable, f"Request added for user {username}")

def delete_demande(
    intitule: str,
    username: str,
    debug_variable=False
):
    
    """
    Supprime une demande de la table Demandes.

    Parameters
    ----------
    intitule : str
        Titre de la demande à supprimer.
    username : str
        Nom d'utilisateur de la demande à supprimer.
    debug_variable : bool, optional
        Si True, affiche un message de debug (par defaut False).
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        idProjet = cursor.execute("SELECT D.idProjet FROM Demandes D JOIN Clients C ON D.idClient = C.id WHERE D.intitule = ? AND C.username = ?",(intitule, username)).fetchone()[0]
        cursor.execute("DELETE FROM Demandes WHERE idProjet = ?", (idProjet,))
        conn.commit()
        debug(debug_variable, f"La demande {intitule} supprime de Demandes")

def modify_demande(
    intitule: str,
    username: str,
    new_intitule=None, 
    new_deadline=None, 
    new_description=None, 
    debug_variable=False
):
    """
    Modifie les informations d'une demande dans la base de données.

    Cette fonction met à jour un ou plusieurs champs de la table 'Demandes'
    pour l'enregistrement identifié par `idProjet`.

    Paramètres :
    -----------
    intitule : str
        Titre de la demande à modifier.
    username : str
        Nom d'utilisateur de la demande à modifier.
    new_intitule : str, optionnel
        Nouveau titre/intitulé de la demande.
    new_deadline : str, optionnel
        Nouvelle date limite (format 'YYYY-MM-DD').
    new_description : str, optionnel
        Nouvelle description de la demande.
    debug_variable : bool, optionnel
        Si True, affiche des messages de debug (par defaut False).

    Retour :
    -------
    None
        La fonction ne retourne rien, elle modifie directement la base de données.

    Exemple d'utilisation :
    ----------------------
    modify_demande(conn, 1, new_description="Demande mise à jour", debug_variable=True)
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        updates = []
        params = []
        result = cursor.execute(
            "SELECT D.idProjet FROM Demandes D JOIN Clients C ON D.idClient = C.id WHERE D.intitule = ? AND C.username = ?",
            (intitule, username)
        ).fetchone()

        if result is None:
            debug(debug_variable, f"Aucune demande trouvée pour {username} avec l'intitulé '{intitule}'.")
            return  # ou raise Exception("Demande non trouvée")
        idProjet = result[0]

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
        debug(debug_variable, f"La demande {intitule} a ete modifiee.")

# Fonctions pour manipuler la table Projets

def show_projets(

):
    """
    Lit et affiche toutes les demandes de la table Projets.

    Parameters
    ----------
    Ne prends rien en paramètre.
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT C.username, C.email, D.intitule, D.deadline, D.description
        FROM Demandes D
        JOIN Clients C ON D.idClient = C.id
        WHERE D.accepted = 1
        """)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

def accept_projet(
        intitule: str,
        username: str,
        email: str,
        bool_variable=False,
        debug_variable=False
):
    """
    Accepte ou refuse un projet dans la table Demandes

    Parameters
    ----------
    intitule : str
        Titre du projet.
    username : str
        Nom d'utilisateur de la demande.
    bool_variable : bool
        True pour accepter, False pour refuser.
    debug_variable : bool, optional
        Si True, affiche un message de debug (par defaut False).
    """
    with connect_db(nom_bdd, debug_variable=False) as conn:
        cursor = conn.cursor()
        idClient = int(cursor.execute("SELECT id FROM Clients WHERE username = ? AND email = ?", (username, email)).fetchone()[0])
        if not bool_variable:
            cursor.execute("UPDATE Demandes SET accepted = ? WHERE intitule = ? AND idClient = ?", ("0", intitule,  idClient))
            conn.commit()
            debug(debug_variable, f"Project {intitule} rejected.")
        else:
            cursor.execute("UPDATE Demandes SET accepted = ? WHERE intitule = ? AND idClient = ?", ("1", intitule,  idClient))
            conn.commit()
            debug(debug_variable, f"Project {intitule} accepted successfully.")



#------------------------------- Point d'entrée : Programme principal de test des fonctions CRUD -------------------------------------------------------------------------------

if __name__ == "__main__":
#------------------------------------ Test de l'ajout a la base de donnée dans les différentes tables -----------------------------------------------------------
    print("\n=== Ajout d'enregistrements de test ===")
    try:
        add_user("test_user", "test@example.com", debug_variable=True)
        add_demande("test_user", "test@example.com", "moteur python", "2025-11-03", "Il faut une fonction debug...", debug_variable=True)
        accept_projet("moteur python", "test_user", "test@example.com", True, debug_variable=True)
    except Exception as e:
        print(f"Erreur lors de l'ajout : {e}")
#-------------------------------------- Première lecture des tables : Les enregistrements ont bien été ajoutés ----------------------------------------------------------------------------
    print("\n=== Lecture des tables existantes ===")
    try:
        print("\n--- Clients ---")
        show_users()

        print("\n--- Demandes ---")
        show_demandes()

        print("\n--- Projets ---")
        show_projets()
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
#-------------------------------------- Test de modifiaction d'enregistrements des différentes tables de la bdd -----------------------------------------------------------------------
    print("\n=== Modifications ===")
    try:
        modify_user("test_user", new_username="new_name", new_email="newmail@example.com", debug_variable=True)
        modify_demande("moteur python", "new_name", new_description="Demande mise a jour", debug_variable=True)
        accept_projet("moteur python", "new_name", "newmail@example.com", False, debug_variable=True)
    except Exception as e:
        print(f"Erreur lors de la modification : {e}")
#-------------------------------------- Seconde lecture des tables : Les enregistrements ont bien été modifiés----------------------------------------------------------------------------
    print("\n=== Lecture des tables existantes ===")
    try:
        print("\n--- Clients ---")
        show_users()

        print("\n--- Demandes ---")
        show_demandes()

        print("\n--- Projets ---")
        show_projets()
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
#------------------------------------- Suppression d'enregistrements dans les tables de la bdd -----------------------------------------------------------------------------
    print("\n=== Suppressions ===")
    try:
        delete_demande("moteur python", "new_name", debug_variable=True)
        delete_user("new_name", debug_variable=True)
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")
#--------------------------------------- Derniere lecture : tous les enregistrements test ont bien été supprimés ---------------------------------------------------------------------------      
    print("\n=== Lecture des tables existantes ===")
    try:
        print("\n--- Clients ---")
        show_users()

        print("\n--- Demandes ---")
        show_demandes()

        print("\n--- Projets ---")
        show_projets()
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")  
#------------------------------------------------------------------------------------------------------------------
    print("\n=== Fin des tests ===")
