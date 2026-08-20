import bcrypt
from database.db import get_connection


def register_user(name,email,password):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO users(name,email,password)
    VALUES(%s,%s,%s)
    """

    hashed_password = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
)


    values = (
    name,
    email,
    hashed_password.decode("utf-8")
)
    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()
    
    
    

    
    
    
def login_user(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT * FROM users
    WHERE email=%s
    """

    values = (email,)

    cursor.execute(query, values)

    user = cursor.fetchone()

    if user:
        stored_password = user[3]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        ):
            cursor.close()
            connection.close()
            return user

    cursor.close()
    connection.close()

    return None