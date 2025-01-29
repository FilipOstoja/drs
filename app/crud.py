from mysql.connector import Error

def create_user(db, username, email, hashed_password):
    cursor = db.cursor()
    try:
        # Provjera postoji li već korisnik s tim emailom ili korisničkim imenom
        cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (email, username))
        existing_user = cursor.fetchone()

        if existing_user:
            raise Exception("User with this email or username already exists")

        # Ako ne postoji, ubacivanje novog korisnika
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password)
            VALUES (%s, %s, %s)
        """, (username, email, hashed_password))
        db.commit()

    except Error as e:
        db.rollback()
        raise Exception(f"Error inserting user: {e}")
    finally:
        cursor.close()

def authenticate_user(db, username, password, pwd_context):
    cursor = db.cursor(dictionary=True)  # dictionary=True za dobivanje rezultata kao dict
    try:
        # Dohvat korisnika po username
        cursor.execute("SELECT id, username, email, hashed_password, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user or not pwd_context.verify(password, user["hashed_password"]):
            return None  # Pogrešno korisničko ime ili lozinka

        # Vraćanje korisničkog podatka s rolom
        return {"id": user["id"], "username": user["username"], "role": user["role"]}

    except Error as e:
        raise Exception(f"Error authenticating user: {e}")
    finally:
        cursor.close()
