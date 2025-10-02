import sqlite3

def connect_db(db_name):
    """bah ca se connecte quoi."""
    conn = sqlite3.connect(db_name)
    print(f"Connecté à : {db_name}")
    return conn





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
        cursor.execute("DELETE FROM Clients WHERE id = ?", (user_id,))
        conn.commit()
        print(f"User {user_id} supprimé de Clients")
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")





conn = connect_db("testprojet")
if conn:
    add_user(conn, "testuser", "testuser@gmqil.com2")
    conn.close()

