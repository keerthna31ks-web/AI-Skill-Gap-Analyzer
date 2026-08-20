from database.db import get_connection
import json


def save_roadmap(user_id, career, roadmap):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO ai_roadmaps (user_id, career, roadmap_json)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (user_id, career, json.dumps(roadmap))
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_user_roadmaps(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT roadmap_id, user_id, career, roadmap_json, created_at
        FROM ai_roadmaps
        WHERE user_id = %s
        ORDER BY created_at DESC
    """

    cursor.execute(query, (user_id,))

    roadmaps = cursor.fetchall()

    cursor.close()
    connection.close()

    for roadmap in roadmaps:
        roadmap["roadmap_json"] = json.loads(roadmap["roadmap_json"])

    return roadmaps