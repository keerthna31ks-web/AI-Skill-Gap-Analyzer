from database.db import get_connection


def save_profile(
    user_id,
    full_name,
    college,
    department,
    current_year,
    cgpa,
    career_domain,
    target_role
):

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether this user already has a profile
    check_query = """
        SELECT profile_id
        FROM user_profile
        WHERE user_id = %s
        LIMIT 1
    """

    cursor.execute(check_query, (user_id,))

    existing_profile = cursor.fetchone()

    if existing_profile:

        # Update existing profile
        update_query = """
            UPDATE user_profile
            SET
                full_name = %s,
                college = %s,
                department = %s,
                current_year = %s,
                cgpa = %s,
                career_domain = %s,
                target_role = %s
            WHERE user_id = %s
        """

        values = (
            full_name,
            college,
            department,
            current_year,
            cgpa,
            career_domain,
            target_role,
            user_id
        )

        cursor.execute(update_query, values)

    else:

        # Create profile for first time
        insert_query = """
            INSERT INTO user_profile(
                user_id,
                full_name,
                college,
                department,
                current_year,
                cgpa,
                career_domain,
                target_role
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            user_id,
            full_name,
            college,
            department,
            current_year,
            cgpa,
            career_domain,
            target_role
        )

        cursor.execute(insert_query, values)

    connection.commit()

    cursor.close()
    connection.close()
    
    
    
def get_target_role(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT target_role
        FROM user_profile
        WHERE user_id = %s
        ORDER BY profile_id DESC
        LIMIT 1
    """

    cursor.execute(query, (user_id,))

    profile = cursor.fetchone()

    cursor.close()
    connection.close()

    if profile:
        return profile["target_role"]

    return None



def get_user_profile(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            full_name,
            college,
            department,
            current_year,
            cgpa,
            career_domain,
            target_role
        FROM user_profile
        WHERE user_id = %s
        ORDER BY profile_id DESC
        LIMIT 1
    """

    cursor.execute(query, (user_id,))

    profile = cursor.fetchone()

    cursor.close()
    connection.close()

    return profile