from database.db import get_connection
from models.profile import get_target_role

def save_skills(user_id, selected_skills):

    connection = get_connection()
    cursor = connection.cursor()

    # Remove old skills
    delete_query = """
    DELETE FROM user_skills
    WHERE user_id = %s
    """

    cursor.execute(delete_query, (user_id,))

    # Insert new skills with proficiency
    insert_query = """
    INSERT INTO user_skills(user_id, skill_name, proficiency)
    VALUES(%s, %s, %s)
    """

    for skill, proficiency in selected_skills.items():

        cursor.execute(
            insert_query,
            (user_id, skill, proficiency)
        )

    connection.commit()

    cursor.close()
    connection.close()
    
def analyze_skill_gap (user_skills, required_skills):


    # Normalize skills
    user_skills = [
        skill.strip().lower()
        for skill in user_skills
    ]

    required_skills = [
        skill.strip().lower()
        for skill in required_skills
    ]

    # Create aliases for common skill names
    aliases = {
        "scikit learn": "scikit-learn",
        "scikit_learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "reactjs": "react"
    }

    # Apply aliases
    user_skills = [
        aliases.get(skill, skill)
        for skill in user_skills
    ]

    required_skills = [
        aliases.get(skill, skill)
        for skill in required_skills
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in user_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Calculate percentage
    if len(required_skills) > 0:
        match_percentage = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        match_percentage = 0

    skill_gap_percentage = round(100 - match_percentage, 2)

    return {
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,
    "match_percentage": round(match_percentage, 2),
    "skill_gap_percentage": skill_gap_percentage
}
    
    
    
    
def get_user_skills(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT skill_name, proficiency
    FROM user_skills
    WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results



def get_career_required_skills(career_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT s.skill_name
    FROM career_skills cs
    JOIN skills s
        ON cs.skill_id = s.skill_id
    WHERE cs.career_id = %s
    ORDER BY cs.priority ASC
    """

    cursor.execute(query, (career_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [row[0] for row in results]

def get_career_skill_details(career_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            s.skill_name,
            cs.importance,
            cs.required_proficiency,
            cs.priority
        FROM career_skills cs
        JOIN skills s
            ON cs.skill_id = s.skill_id
        WHERE cs.career_id = %s
        ORDER BY cs.priority ASC
    """

    cursor.execute(query, (career_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def analyze_weighted_skill_gap(user_skills, career_skill_details):

    # Normalize user skills
    user_skills = [
        skill.strip().lower()
        for skill in user_skills
    ]

    # Aliases
    aliases = {
        "scikit learn": "scikit-learn",
        "scikit_learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "reactjs": "react"
    }

    user_skills = [
        aliases.get(skill, skill)
        for skill in user_skills
    ]

    matched_skills = []
    missing_skills = []

    total_weight = 0
    matched_weight = 0

    essential_missing = []
    important_missing = []

    for skill_name, importance, proficiency, priority in career_skill_details:

        skill = skill_name.strip().lower()

        # Assign weight
        if importance.lower() == "essential":
            weight = 3
        elif importance.lower() == "important":
            weight = 2
        else:
            weight = 1

        total_weight += weight

        if skill in user_skills:

            matched_skills.append({
                "skill": skill_name,
                "importance": importance,
                "proficiency": proficiency,
                "priority": priority
            })

            matched_weight += weight

        else:

            missing_skills.append({
                "skill": skill_name,
                "importance": importance,
                "proficiency": proficiency,
                "priority": priority
            })

            if importance.lower() == "essential":
                essential_missing.append(skill_name)

            elif importance.lower() == "important":
                important_missing.append(skill_name)

    # Calculate weighted readiness
    if total_weight > 0:
        readiness_score = (
            matched_weight / total_weight
        ) * 100
    else:
        readiness_score = 0

    skill_gap_percentage = 100 - readiness_score

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "essential_missing": essential_missing,
        "important_missing": important_missing,
        "readiness_score": round(readiness_score, 2),
        "skill_gap_percentage": round(skill_gap_percentage, 2)
    }
    
def get_all_careers():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        c.career_id,
        c.career_name
    FROM careers c
    INNER JOIN career_skills cs
        ON c.career_id = cs.career_id
    WHERE c.status = 1
    GROUP BY
        c.career_id,
        c.career_name
    HAVING COUNT(cs.skill_id) > 0
    ORDER BY c.career_id
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def recommend_careers(user_id):

    # Get user's skills with proficiency
    user_skills = get_user_skills(user_id)

    # Get all available careers
    careers = get_all_careers()

    recommendations = []

    for career_id, career_name in careers:

        # Get career skill requirements
        career_skill_details = get_career_skill_details(
            career_id
        )

        # Calculate proficiency-aware readiness
        result = calculate_proficiency_readiness(
            user_skills,
            career_skill_details
        )

        recommendations.append({
            "career_id": career_id,
            "career_name": career_name,
            "readiness_score": result["readiness_score"],
            "skill_gap_percentage": result["skill_gap_percentage"],
            "matched_skills": result["matched_skills"],
            "partial_skills": result["partial_skills"],
            "missing_skills": result["missing_skills"]
        })

    # Highest readiness first
    recommendations.sort(
        key=lambda x: x["readiness_score"],
        reverse=True
    )

    return recommendations

def get_career_recommendation_details(user_id):

    connection = get_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        # --------------------------------------------------
        # Get user's skills and proficiency
        # --------------------------------------------------
        cursor.execute("""
                    SELECT
                    s.skill_id,
                    s.skill_name,
                    us.proficiency
                    FROM user_skills us
                    JOIN skills s
                    ON us.skill_name = s.skill_name
                    WHERE us.user_id = %s
                        """, (user_id,))

        user_skills = cursor.fetchall()
        

        if not user_skills:
            return []


        # --------------------------------------------------
        # Convert proficiency to numeric value
        # --------------------------------------------------

        proficiency_map = {
            "Beginner": 1,
            "Intermediate": 2,
            "Advanced": 3
        }


        user_skill_map = {}

        for skill in user_skills:

            user_skill_map[
                skill["skill_id"]
            ] = proficiency_map.get(
                skill["proficiency"],
                0
            )


        # --------------------------------------------------
        # Get career skill requirements
        # --------------------------------------------------

        cursor.execute("""
            SELECT
                c.career_id,
                c.career_name,
                cs.skill_id,
                s.skill_name,
                cs.importance,
                cs.required_proficiency,
                cs.priority
            FROM careers c
            JOIN career_skills cs
                ON c.career_id = cs.career_id
            JOIN skills s
                ON cs.skill_id = s.skill_id
            WHERE c.status = 1
            ORDER BY
                c.career_id,
                cs.priority
        """)

        career_skills = cursor.fetchall()
        


        if not career_skills:
            return []


        # --------------------------------------------------
        # Group skills by career
        # --------------------------------------------------

        careers = {}

        for row in career_skills:

            career_id = row["career_id"]

            if career_id not in careers:

                careers[career_id] = {
                    "career_id": career_id,
                    "career": row["career_name"],
                    "skills": []
                }

            careers[career_id]["skills"].append(row)


        # --------------------------------------------------
        # Calculate career readiness
        # --------------------------------------------------

        recommendations = []


        for career in careers.values():

            total_weight = 0
            achieved_weight = 0

            matched_skills = []
            partial_skills = []
            missing_skills = []


            for requirement in career["skills"]:

                skill_id = requirement["skill_id"]

                required_level = proficiency_map.get(
                    requirement["required_proficiency"],
                    1
                )

                importance = requirement["importance"]


                # ------------------------------------------
                # Importance weight
                # ------------------------------------------

                if importance == "Essential":
                    weight = 3

                elif importance == "Important":
                    weight = 2

                else:
                    weight = 1


                total_weight += weight


                # ------------------------------------------
                # User proficiency
                # ------------------------------------------

                user_level = user_skill_map.get(
                    skill_id,
                    0
                )


                # ------------------------------------------
                # Calculate achievement
                # ------------------------------------------

                if user_level >= required_level:

                    achieved_weight += weight

                    matched_skills.append(
                        requirement["skill_name"]
                    )

                elif user_level > 0:

                    # Partial skill
                    achievement_ratio = (
                        user_level / required_level
                    )

                    achieved_weight += (
                        weight * achievement_ratio
                    )

                    partial_skills.append({
                        "skill": requirement["skill_name"],
                        "current_proficiency":
                            next(
                                (
                                    p
                                    for p, v
                                    in proficiency_map.items()
                                    if v == user_level
                                ),
                                "Unknown"
                            ),
                        "required_proficiency":
                            requirement[
                                "required_proficiency"
                            ]
                    })

                else:

                    missing_skills.append({
                        "skill": requirement["skill_name"],
                        "required_proficiency":
                            requirement[
                                "required_proficiency"
                            ],
                        "importance": importance,
                        "priority":
                            requirement["priority"]
                    })


            # --------------------------------------------------
            # Readiness score
            # --------------------------------------------------

            if total_weight > 0:

                readiness_score = (
                    achieved_weight /
                    total_weight
                ) * 100

            else:

                readiness_score = 0


            skill_gap_percentage = (
                100 - readiness_score
            )


            # --------------------------------------------------
            # Sort missing skills by priority
            # --------------------------------------------------

            missing_skills.sort(
                key=lambda x: x["priority"]
            )


            # --------------------------------------------------
            # Learning priority
            # --------------------------------------------------

            learning_priority = [
                skill["skill"]
                for skill in missing_skills
                if skill["importance"] == "Essential"
            ]

            learning_priority += [
                skill["skill"]
                for skill in missing_skills
                if skill["importance"] == "Important"
            ]


            recommendations.append({

                "career_id":
                    career["career_id"],

                "career_name":
                    career["career"],

                "readiness_score":
                    round(readiness_score, 2),

                "skill_gap_percentage":
                    round(skill_gap_percentage, 2),

                "matched_skills":
                    matched_skills,

                "partial_skills":
                    partial_skills,

                "missing_skills":
                    missing_skills,

                "learning_priority":
                    learning_priority,

                "total_required_skills":
                    len(career["skills"]),

                "matched_skill_count":
                    len(matched_skills),

                "missing_skill_count":
                    len(missing_skills)
            })


        # --------------------------------------------------
        # Rank careers
        # --------------------------------------------------

        recommendations.sort(
            key=lambda x: x["readiness_score"],
            reverse=True
        )


        return recommendations


    finally:

        cursor.close()
        connection.close()
        
        
def analyze_proficiency_skill_gap(user_skills, career_skill_details):

    # Proficiency levels
    proficiency_levels = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
        "expert": 4
    }

    # Skill aliases
    aliases = {
        "scikit learn": "scikit-learn",
        "scikit_learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "reactjs": "react"
    }

    # Convert user's skills into dictionary
    user_skill_map = {}

    for skill, proficiency in user_skills:

        normalized_skill = skill.strip().lower()

        normalized_skill = aliases.get(
            normalized_skill,
            normalized_skill
        )

        user_skill_map[normalized_skill] = (
            proficiency.strip().lower()
        )

    matched_skills = []
    partial_skills = []
    missing_skills = []

    for skill_name, importance, required_proficiency, priority in career_skill_details:

        skill = skill_name.strip().lower()

        required_level = proficiency_levels.get(
            required_proficiency.strip().lower(),
            1
        )

        # User does not have skill
        if skill not in user_skill_map:

            missing_skills.append({
                "skill": skill_name,
                "importance": importance,
                "user_proficiency": None,
                "required_proficiency": required_proficiency,
                "priority": priority
            })

        else:

            user_proficiency = user_skill_map[skill]

            user_level = proficiency_levels.get(
                user_proficiency,
                1
            )

            # User meets requirement
            if user_level >= required_level:

                matched_skills.append({
                    "skill": skill_name,
                    "importance": importance,
                    "user_proficiency": user_proficiency,
                    "required_proficiency": required_proficiency,
                    "priority": priority
                })

            # User has skill but needs improvement
            else:

                partial_skills.append({
                    "skill": skill_name,
                    "importance": importance,
                    "user_proficiency": user_proficiency,
                    "required_proficiency": required_proficiency,
                    "priority": priority
                })

    return {
        "matched_skills": matched_skills,
        "partial_skills": partial_skills,
        "missing_skills": missing_skills
    }
    
def calculate_proficiency_readiness(
    user_skills,
    career_skill_details
):

    proficiency_levels = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
        "expert": 4
    }

    aliases = {
        "scikit learn": "scikit-learn",
        "scikit_learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "reactjs": "react"
    }

    # --------------------------------------------------
    # User Skill Map
    # --------------------------------------------------

    user_skill_map = {}

    for item in user_skills:

        if isinstance(item, dict):

            skill = (
                item.get("skill")
                or item.get("skill_name")
                or item.get("name")
            )

            proficiency = (
                item.get("proficiency")
                or item.get("level")
                or "beginner"
            )

        else:

            try:
                skill, proficiency = item
            except (TypeError, ValueError):
                continue

        if not skill:
            continue

        normalized_skill = (
            str(skill)
            .strip()
            .lower()
        )

        normalized_skill = aliases.get(
            normalized_skill,
            normalized_skill
        )

        user_skill_map[normalized_skill] = (
            str(proficiency)
            .strip()
            .lower()
        )

    # --------------------------------------------------
    # Scores
    # --------------------------------------------------

    total_weight = 0
    achieved_weight = 0

    matched_skills = []
    partial_skills = []
    missing_skills = []

    # --------------------------------------------------
    # Career Requirements
    # --------------------------------------------------

    for item in career_skill_details:

        # Support dictionary format
        if isinstance(item, dict):

            skill_name = item.get(
                "skill_name",
                ""
            )

            importance = item.get(
                "importance",
                "Important"
            )

            required_proficiency = item.get(
                "required_proficiency",
                "Beginner"
            )

            priority = item.get(
                "priority",
                0
            )

        # Support tuple format too
        else:

            try:

                (
                    skill_name,
                    importance,
                    required_proficiency,
                    priority
                ) = item

            except (TypeError, ValueError):

                continue

        if not skill_name:
            continue

        skill = (
            str(skill_name)
            .strip()
            .lower()
        )

        importance = (
            str(importance)
            .strip()
        )

        required_proficiency = (
            str(required_proficiency)
            .strip()
        )

        # --------------------------------------------------
        # Importance Weight
        # --------------------------------------------------

        importance_lower = importance.lower()

        if importance_lower == "essential":

            weight = 3

        elif importance_lower == "important":

            weight = 2

        else:

            weight = 1

        total_weight += weight

        # --------------------------------------------------
        # Required Proficiency
        # --------------------------------------------------

        required_level = proficiency_levels.get(
            required_proficiency.lower(),
            1
        )

        # --------------------------------------------------
        # Missing Skill
        # --------------------------------------------------

        if skill not in user_skill_map:

            missing_skills.append({

                "skill": skill_name,

                "importance": importance,

                "required_proficiency":
                    required_proficiency,

                "priority": priority

            })

            credit = 0

        # --------------------------------------------------
        # Existing Skill
        # --------------------------------------------------

        else:

            user_proficiency = user_skill_map[skill]

            user_level = proficiency_levels.get(
                user_proficiency,
                1
            )

            # --------------------------------------------------
            # Full Match
            # --------------------------------------------------

            if user_level >= required_level:

                matched_skills.append({

                    "skill": skill_name,

                    "importance": importance,

                    "user_proficiency":
                        user_proficiency,

                    "required_proficiency":
                        required_proficiency,

                    "priority": priority

                })

                credit = 1

            # --------------------------------------------------
            # Partial Match
            # --------------------------------------------------

            else:

                partial_skills.append({

                    "skill": skill_name,

                    "importance": importance,

                    "user_proficiency":
                        user_proficiency,

                    "required_proficiency":
                        required_proficiency,

                    "priority": priority

                })

                credit = 0.5

        achieved_weight += (
            weight * credit
        )

    # --------------------------------------------------
    # Readiness
    # --------------------------------------------------

    if total_weight > 0:

        readiness_score = (
            achieved_weight /
            total_weight
        ) * 100

    else:

        readiness_score = 0

    skill_gap_percentage = (
        100 - readiness_score
    )

    # --------------------------------------------------
    # Final Result
    # --------------------------------------------------

    return {

        "matched_skills":
            matched_skills,

        "partial_skills":
            partial_skills,

        "missing_skills":
            missing_skills,

        "readiness_score":
            round(
                readiness_score,
                2
            ),

        "skill_gap_percentage":
            round(
                skill_gap_percentage,
                2
            )
    }
def get_roadmap_input(user_id):

    # --------------------------------------------------
    # 1. Get selected target career
    # --------------------------------------------------

    target_role = get_target_role(user_id)

    print("DEBUG USER ID:", user_id)
    print("DEBUG TARGET ROLE:", target_role)

    if not target_role:
        raise ValueError(
            "No target career found for this user."
        )


    # --------------------------------------------------
    # 2. Find career in careers table
    # --------------------------------------------------

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT career_id, career_name
        FROM careers
        WHERE LOWER(TRIM(career_name)) = LOWER(TRIM(%s))
        LIMIT 1
    """

    cursor.execute(
        query,
        (target_role,)
    )

    career = cursor.fetchone()

    cursor.close()
    connection.close()

    print("DEBUG CAREER:", career)

    if not career:
        raise ValueError(
            f"Target career '{target_role}' "
            f"was not found in careers table."
        )

    career_id = career["career_id"]


    # --------------------------------------------------
    # 3. Get user's skills
    # --------------------------------------------------

    user_skills = get_user_skills(user_id)

    print("DEBUG USER SKILLS:", user_skills)

    if user_skills is None:
        user_skills = []


    # --------------------------------------------------
    # 4. Get selected career requirements
    # --------------------------------------------------

    career_skill_details = get_career_skill_details(
        career_id
    )

    print(
        "DEBUG CAREER SKILL DETAILS:",
        career_skill_details
    )

    if not career_skill_details:
        raise ValueError(
            f"No skill requirements found for "
            f"career '{target_role}' "
            f"(career_id={career_id})."
        )


    # --------------------------------------------------
    # 5. Calculate readiness
    # --------------------------------------------------

    result = calculate_proficiency_readiness(
        user_skills,
        career_skill_details
    )

    print("DEBUG READINESS RESULT:", result)


    # --------------------------------------------------
    # 6. Current skills
    # --------------------------------------------------

    current_skills = []

    for skill, proficiency in user_skills:

        current_skills.append({
            "skill": skill,
            "proficiency": proficiency
        })


    # --------------------------------------------------
    # 7. Skill gaps
    # --------------------------------------------------

    skill_gaps = []

    for skill in result.get(
        "missing_skills",
        []
    ):

        skill_gaps.append({
            "skill": skill["skill"],
            "importance": skill["importance"],
            "required_proficiency":
                skill["required_proficiency"],
            "priority": skill["priority"]
        })


    # --------------------------------------------------
    # 8. Partial skills
    # --------------------------------------------------

    partial_skills = []

    for skill in result.get(
        "partial_skills",
        []
    ):

        partial_skills.append({
            "skill": skill["skill"],
            "importance": skill["importance"],
            "user_proficiency":
                skill["user_proficiency"],
            "required_proficiency":
                skill["required_proficiency"],
            "priority": skill["priority"]
        })


    # --------------------------------------------------
    # 9. Learning priority
    # --------------------------------------------------

    learning_items = (
        skill_gaps +
        partial_skills
    )

    learning_items.sort(
        key=lambda x: (
            0 if str(
                x["importance"]
            ).lower() == "essential"

            else 1 if str(
                x["importance"]
            ).lower() == "important"

            else 2,

            x["priority"]
        )
    )

    learning_priority = [
        item["skill"]
        for item in learning_items
    ]


    # --------------------------------------------------
    # 10. Career recommendations
    # --------------------------------------------------

    career_recommendations = (
        get_career_recommendation_details(
            user_id
        )
    )

    if career_recommendations is None:
        career_recommendations = []


    # --------------------------------------------------
    # 11. FINAL ROADMAP INPUT
    # --------------------------------------------------

    roadmap_input = {

        "career": target_role,

        "target_career": target_role,

        "career_id": career_id,

        "readiness_score":
            result.get(
                "readiness_score",
                0
            ),

        "skill_gap_percentage":
            result.get(
                "skill_gap_percentage",
                100
            ),

        "current_skills":
            current_skills,

        "partial_skills":
            partial_skills,

        "skill_gaps":
            skill_gaps,

        "learning_priority":
            learning_priority,

        "career_recommendations":
            career_recommendations
    }


    print(
        "DEBUG FINAL ROADMAP INPUT:",
        roadmap_input
    )

    return roadmap_input
def mark_skill_learned(user_id, skill_name):
    """
    Upgrade a roadmap skill after the user completes
    the entire learning phase.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether the user already has this skill
    check_query = """
        SELECT skill_id, proficiency
        FROM user_skills
        WHERE user_id = %s
        AND skill_name = %s
        LIMIT 1
    """

    cursor.execute(
        check_query,
        (user_id, skill_name)
    )

    existing_skill = cursor.fetchone()

    if existing_skill:

        skill_id = existing_skill[0]
        current_proficiency = existing_skill[1]

        # Upgrade Beginner → Intermediate
        if current_proficiency == "Beginner":

            update_query = """
                UPDATE user_skills
                SET proficiency = 'Intermediate'
                WHERE skill_id = %s
                AND user_id = %s
            """

            cursor.execute(
                update_query,
                (skill_id, user_id)
            )

    else:

        # Skill was not previously added by the user
        insert_query = """
            INSERT INTO user_skills
            (user_id, skill_name, proficiency)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                user_id,
                skill_name,
                "Intermediate"
            )
        )

    connection.commit()

    cursor.close()
    connection.close()