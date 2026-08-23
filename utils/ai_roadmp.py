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

    # ======================================================
    # TARGET CAREER
    # ======================================================

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
    # USER SKILLS
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

        "readiness_score":
            roadmap_input.get("readiness_score"),

        "skill_gap_percentage":
            roadmap_input.get("skill_gap_percentage"),

        "current_skills":
            current_skills,

        "partial_skills":
            partial_skills,

        "skill_gaps":
            skill_gaps,

        "learning_priority":
            learning_priority
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
6. Create exactly 4 progressive phases numbered 1, 2, 3, and 4.
7. Every phase MUST be a complete JSON object.
8. Never place phase fields directly inside the phases array.
9. Each phase must contain exactly 2 topics.
10. Each topic must contain a short description.
11. Each topic must contain exactly 1 practice task.
12. Each phase must contain exactly 1 mini project.
13. Include exactly 1 final project specifically for {target_career}.
14. Keep descriptions short.
15. Return ONLY valid JSON.
16. Do not use markdown.
17. Do not include explanations outside JSON.

OUTPUT STRUCTURE:

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
                        "one practical task"
                    ]
                }},

                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "one practical task"
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
        }},

        {{
            "phase": 2,
            "skill": "skill",
            "reason": "short reason",

            "topics": [

                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "one practical task"
                    ]
                }},

                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "one practical task"
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
        }},

        {{
            "phase": 3,
            "skill": "skill",
            "reason": "short reason",

            "topics": [

                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "one practical task"
                    ]
                }},

                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "one practical task"
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
        }},

        {{
            "phase": 4,
            "skill": "skill",
            "reason": "short reason",

            "topics": [

                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "one practical task"
                    ]
                }},

                {{
                    "topic": "topic",
                    "description": "short description",
                    "practice": [
                        "one practical task"
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
    # JSON SCHEMA
    # ======================================================

    roadmap_schema = {

        "type": "object",

        "properties": {

            "career": {
                "type": "string"
            },

            "roadmap_summary": {
                "type": "string"
            },

            "phases": {

                "type": "array",

                "minItems": 4,
                "maxItems": 4,

                "items": {

                    "type": "object",

                    "properties": {

                        "phase": {
                            "type": "integer"
                        },

                        "skill": {
                            "type": "string"
                        },

                        "reason": {
                            "type": "string"
                        },

                        "topics": {

                            "type": "array",

                            "minItems": 2,
                            "maxItems": 2,

                            "items": {

                                "type": "object",

                                "properties": {

                                    "topic": {
                                        "type": "string"
                                    },

                                    "description": {
                                        "type": "string"
                                    },

                                    "practice": {

                                        "type": "array",

                                        "minItems": 1,
                                        "maxItems": 1,

                                        "items": {
                                            "type": "string"
                                        }
                                    }
                                },

                                "required": [
                                    "topic",
                                    "description",
                                    "practice"
                                ],

                                "additionalProperties": False
                            }
                        },

                        "mini_project": {

                            "type": "object",

                            "properties": {

                                "title": {
                                    "type": "string"
                                },

                                "description": {
                                    "type": "string"
                                },

                                "skills_used": {

                                    "type": "array",

                                    "items": {
                                        "type": "string"
                                    }
                                }
                            },

                            "required": [
                                "title",
                                "description",
                                "skills_used"
                            ],

                            "additionalProperties": False
                        }
                    },

                    "required": [
                        "phase",
                        "skill",
                        "reason",
                        "topics",
                        "mini_project"
                    ],

                    "additionalProperties": False
                }
            },

            "final_project": {

                "type": "object",

                "properties": {

                    "title": {
                        "type": "string"
                    },

                    "description": {
                        "type": "string"
                    },

                    "skills_used": {

                        "type": "array",

                        "items": {
                            "type": "string"
                        }
                    },

                    "expected_outcome": {
                        "type": "string"
                    }
                },

                "required": [
                    "title",
                    "description",
                    "skills_used",
                    "expected_outcome"
                ],

                "additionalProperties": False
            }
        },

        "required": [
            "career",
            "roadmap_summary",
            "phases",
            "final_project"
        ],

        "additionalProperties": False
    }


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
                        "Return ONLY JSON that follows "
                        "the provided schema."
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
                "type": "json_object",

                
            }
        )

    except Exception as e:

        raise ValueError(
            f"Groq API error: {str(e)}"
        )


    # ======================================================
    # GET RESPONSE
    # ======================================================

    content = response.choices[0].message.content

    if not content:

        raise ValueError(
            "Groq returned an empty response."
        )

    content = content.strip()


    # ======================================================
    # PARSE JSON
    # ======================================================

    try:

        roadmap = json.loads(content)

    except json.JSONDecodeError:

        raise ValueError(
            "AI returned invalid JSON."
        )


    # ======================================================
    # VALIDATE ROOT
    # ======================================================

    if not isinstance(roadmap, dict):

        raise ValueError(
            "AI roadmap must be a JSON object."
        )


    # ======================================================
    # FORCE CORRECT CAREER
    # ======================================================

    roadmap["career"] = target_career


    # ======================================================
    # VALIDATE PHASES
    # ======================================================

    phases = roadmap.get("phases")

    if not isinstance(phases, list):

        raise ValueError(
            "AI roadmap phases must be a list."
        )


    if len(phases) != 4:

        raise ValueError(
            f"AI roadmap must contain exactly 4 phases. "
            f"Received {len(phases)}."
        )


    # ======================================================
    # VALIDATE EACH PHASE
    # ======================================================

    for index, phase in enumerate(
        phases,
        start=1
    ):

        if not isinstance(phase, dict):

            raise ValueError(
                f"Phase {index} is invalid. "
                f"Each phase must be a JSON object."
            )


        # Force correct phase number

        phase["phase"] = index


        # --------------------------------------------------
        # Topics
        # --------------------------------------------------

        topics = phase.get("topics")

        if not isinstance(topics, list):

            raise ValueError(
                f"Phase {index} topics must be a list."
            )


        if len(topics) != 2:

            raise ValueError(
                f"Phase {index} must contain exactly 2 topics."
            )


        # --------------------------------------------------
        # Validate Topics
        # --------------------------------------------------

        for topic in topics:

            if not isinstance(topic, dict):

                raise ValueError(
                    f"Invalid topic in phase {index}."
                )


            practice = topic.get("practice")

            if not isinstance(practice, list):

                raise ValueError(
                    f"Practice must be a list "
                    f"in phase {index}."
                )


            if len(practice) != 1:

                raise ValueError(
                    "Each topic must contain "
                    "exactly 1 practice task."
                )


        # --------------------------------------------------
        # Mini Project
        # --------------------------------------------------

        mini_project = phase.get(
            "mini_project"
        )

        if not isinstance(
            mini_project,
            dict
        ):

            raise ValueError(
                f"Phase {index} must contain "
                "a valid mini project."
            )


    # ======================================================
    # VALIDATE FINAL PROJECT
    # ======================================================

    final_project = roadmap.get(
        "final_project"
    )

    if not isinstance(
        final_project,
        dict
    ):

        raise ValueError(
            "Final project is missing or invalid."
        )


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
    # RETURN ROADMAP
    # ======================================================

    return roadmap