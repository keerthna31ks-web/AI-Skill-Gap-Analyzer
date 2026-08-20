import json
import streamlit as st
from groq import Groq

from utils.roadmap_storage import save_roadmap


# ==========================================================
# GROQ CLIENT
# ==========================================================

api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    raise ValueError("GROQ_API_KEY not found in Streamlit Secrets")

client = Groq(api_key=api_key)


# ==========================================================
# GENERATE AI ROADMAP
# ==========================================================

def generate_ai_roadmap(roadmap_input, user_id):

    # ------------------------------------------------------
    # TARGET CAREER
    # ------------------------------------------------------

    target_career = roadmap_input.get("career")

    if not target_career:
        target_career = roadmap_input.get("target_career")

    if not target_career:
        raise ValueError("Target career not found")


    # ======================================================
    # COMPACT SKILL EXTRACTION
    # ======================================================

    def extract_skill_names(data, limit=12):

        result = []

        if not isinstance(data, list):
            return result

        for item in data:

            if isinstance(item, str):
                result.append(item)

            elif isinstance(item, dict):

                name = (
                    item.get("skill")
                    or item.get("skill_name")
                    or item.get("name")
                )

                if name:
                    result.append(name)

        return list(dict.fromkeys(result))[:limit]


    # ======================================================
    # SKILLS
    # ======================================================

    current_skills = extract_skill_names(
        roadmap_input.get("current_skills", []),
        10
    )

    partial_skills = extract_skill_names(
        roadmap_input.get("partial_skills", []),
        10
    )

    skill_gaps = extract_skill_names(
        roadmap_input.get("skill_gaps", []),
        12
    )

    learning_priority = extract_skill_names(
        roadmap_input.get("learning_priority", []),
        12
    )


    # ======================================================
    # AI INPUT
    # ======================================================

    ai_input = {
        "career": target_career,
        "readiness_score": roadmap_input.get("readiness_score"),
        "skill_gap_percentage": roadmap_input.get(
            "skill_gap_percentage"
        ),
        "current_skills": current_skills,
        "partial_skills": partial_skills,
        "skill_gaps": skill_gaps,
        "learning_priority": learning_priority
    }


    # ======================================================
    # PROMPT
    # ======================================================

    prompt = f"""
Create a concise personalized learning roadmap ONLY for:

TARGET CAREER: {target_career}

USER DATA:
{json.dumps(ai_input, separators=(",", ":"))}

RULES:

1. The roadmap MUST be specifically for {target_career}.
2. Never change or replace the target career.
3. Use the user's skill gaps and learning priorities.
4. Respect the user's current skills.
5. Do not invent user skills.
6. Create exactly 4 progressive phases.
7. Each phase must contain exactly 2 topics.
8. Each topic must have a short description and exactly 1 practice task.
9. Each phase must have exactly 1 mini project.
10. Include exactly 1 final project specifically for {target_career}.
11. Keep descriptions very short.
12. Return ONLY valid JSON.
13. Do not use markdown.
14. Do not include explanations outside JSON.

OUTPUT FORMAT:

{{
    "career": "{target_career}",
    "roadmap_summary": "short summary",
    "phases": [
        {{
            "phase": 1,
            "skill": "skill",
            "reason": "short reason",
            "topics": [
                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "practical task"
                    ]
                }},
                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "practical task"
                    ]
                }}
            ],
            "mini_project": {{
                "title": "project title",
                "description": "short description",
                "skills_used": [
                    "skill"
                ]
            }}
        }}
    ],
    "final_project": {{
        "title": "project title",
        "description": "short description",
        "skills_used": [
            "skill"
        ],
        "expected_outcome": "short outcome"
    }}
}}
"""


    # ======================================================
    # CALL GROQ
    # ======================================================

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate concise career-specific "
                        "learning roadmaps. "
                        "Return ONLY valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_completion_tokens=4096,

            response_format={
                "type": "json_object"
            }
        )

    except Exception as e:

        raise ValueError(
            f"Groq API error: {str(e)}"
        )


    # ======================================================
    # GET RESPONSE
    # ======================================================

    content = response.choices[0].message.content.strip()


    # ======================================================
    # PARSE JSON
    # ======================================================

    try:

        roadmap = json.loads(content)

    except json.JSONDecodeError:

        raise ValueError(
            "AI returned invalid JSON:\n"
            + content
        )


    # ======================================================
    # FORCE CORRECT CAREER
    # ======================================================

    roadmap["career"] = target_career


    # ======================================================
    # SAVE TO DATABASE
    # ======================================================

    try:

        save_roadmap(
            user_id=user_id,
            career=target_career,
            roadmap=roadmap
        )

    except Exception as e:

        raise ValueError(
            "Roadmap generated but database save failed: "
            + str(e)
        )


    # ======================================================
    # RETURN
    # ======================================================

    return roadmap