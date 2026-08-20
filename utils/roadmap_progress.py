from database.db import get_connection


# ==========================================================
# GET USER ROADMAP
# ==========================================================

def get_user_roadmap(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            roadmap_id,
            user_id,
            career,
            roadmap_json,
            created_at
        FROM ai_roadmaps
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """

    cursor.execute(
        query,
        (user_id,)
    )

    roadmap = cursor.fetchone()

    cursor.close()
    connection.close()

    return roadmap


# ==========================================================
# GET SINGLE TOPIC PROGRESS
# ==========================================================

def get_topic_progress(
    user_id,
    roadmap_id,
    phase,
    topic
):

    connection = get_connection()
    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT completed
        FROM roadmap_progress
        WHERE user_id = %s
        AND roadmap_id = %s
        AND phase = %s
        AND topic = %s
    """

    cursor.execute(
        query,
        (
            user_id,
            roadmap_id,
            phase,
            topic
        )
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:

        return bool(
            result["completed"]
        )

    return False


# ==========================================================
# SAVE TOPIC PROGRESS
# ==========================================================

def save_topic_progress(
    user_id,
    roadmap_id,
    phase,
    topic,
    completed
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO roadmap_progress
        (
            user_id,
            roadmap_id,
            phase,
            topic,
            completed,
            completed_at
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,

            CASE
                WHEN %s = TRUE
                THEN CURRENT_TIMESTAMP
                ELSE NULL
            END
        )

        ON DUPLICATE KEY UPDATE

            completed = VALUES(completed),

            completed_at =
                CASE
                    WHEN VALUES(completed) = TRUE
                    THEN CURRENT_TIMESTAMP
                    ELSE NULL
                END
    """

    cursor.execute(
        query,
        (
            user_id,
            roadmap_id,
            phase,
            topic,
            completed,
            completed
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================================
# GET ALL ROADMAP PROGRESS
# ==========================================================

def get_roadmap_progress(
    user_id,
    roadmap_id
):

    connection = get_connection()
    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            phase,
            topic,
            completed
        FROM roadmap_progress
        WHERE user_id = %s
        AND roadmap_id = %s
    """

    cursor.execute(
        query,
        (
            user_id,
            roadmap_id
        )
    )

    progress = cursor.fetchall()

    cursor.close()
    connection.close()

    return progress


# ==========================================================
# CHECK WHETHER A COMPLETE PHASE IS FINISHED
# ==========================================================

def is_phase_completed(
    user_id,
    roadmap_id,
    phase,
    topics
):

    progress = get_roadmap_progress(
        user_id,
        roadmap_id
    )

    completed_topics = {
        item["topic"]
        for item in progress
        if (
            item["phase"] == phase
            and item["completed"]
        )
    }

    for topic in topics:

        topic_name = topic.get(
            "topic",
            "Topic"
        )

        if topic_name not in completed_topics:

            return False

    return True