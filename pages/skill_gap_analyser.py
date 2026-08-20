import streamlit as st

from models.skill import get_roadmap_input


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Skill Gap Analysis",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Check Login
# --------------------------------------------------

if "user" not in st.session_state:

    st.warning("Please login first.")

    if st.button("🔐 Go to Login"):

        st.switch_page(
            "pages/login.py"
        )

    st.stop()


# --------------------------------------------------
# User
# --------------------------------------------------

user_id = st.session_state["user"][0]
user_name = st.session_state["user"][1]


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 Skill Gap Analysis")

st.write(
    f"Let's understand your career readiness, **{user_name}**."
)

st.divider()


# --------------------------------------------------
# Get Roadmap Input
# --------------------------------------------------

roadmap_input = get_roadmap_input(user_id)


# --------------------------------------------------
# Check Data
# --------------------------------------------------

if not roadmap_input:

    st.warning(
        "We couldn't generate your skill analysis yet."
    )

    st.info(
        "Please make sure you have completed your profile "
        "and added your skills."
    )

    if st.button("💻 Go to Skills"):

        st.switch_page(
            "pages/skill.py"
        )

    st.stop()


# --------------------------------------------------
# Career Information
# --------------------------------------------------

target_career = roadmap_input.get(
    "target_career"
)

career_recommendations = roadmap_input.get(
    "career_recommendations",
    []
)

if career_recommendations:

    recommended_career = career_recommendations[0]["career_name"]

    recommended_readiness = career_recommendations[0]["readiness_score"]

else:

    recommended_career = None

    recommended_readiness = None

# --------------------------------------------------
# Target Career
# --------------------------------------------------

st.subheader("🎯 Your Target Career")

st.success(
    target_career
)


# --------------------------------------------------
# AI Recommended Career
# --------------------------------------------------

st.subheader("🤖 AI Career Recommendation")

if recommended_career:

    if recommended_career == target_career:

        st.success(
            f"Your current skills strongly align with "
            f"your target career: **{recommended_career}**"
        )

    else:

        st.info(
            f"Based on your current skills and proficiency, "
            f"your strongest career match is **{recommended_career}**."
        )

    if recommended_readiness is not None:

        st.metric(
            "Recommended Career Readiness",
            f"{recommended_readiness}%"
        )

else:

    st.warning(
        "No career recommendation is available yet."
    )


st.divider()


# --------------------------------------------------
# Career Ranking
# --------------------------------------------------

st.subheader("🏆 Career Readiness Ranking")



if career_recommendations:

    for index, career in enumerate(
        career_recommendations[:10],
        start=1
    ):

        career_name = career["career_name"]
        readiness = career["readiness_score"]
        gap = career["skill_gap_percentage"]

        if index == 1:
            label = "🥇"

        elif index == 2:
            label = "🥈"

        elif index == 3:
            label = "🥉"

        else:
            label = f"{index}."

        st.write(
            f"**{label} {career_name}**"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Readiness",
                f"{readiness}%"
            )

        with col2:

            st.metric(
                "Skill Gap",
                f"{gap}%"
            )

        st.progress(
            readiness / 100
        )

else:

    st.info(
        "No career recommendations available."
    )


st.divider()


# --------------------------------------------------
# Target Career Readiness
# --------------------------------------------------

st.subheader(
    f"📊 Readiness for {target_career}"
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Career Readiness",
        f'{roadmap_input["readiness_score"]}%'
    )


with col2:

    st.metric(
        "Skill Gap",
        f'{roadmap_input["skill_gap_percentage"]}%'
    )


st.progress(
    roadmap_input["readiness_score"] / 100
)


st.divider()


# --------------------------------------------------
# Current Skills
# --------------------------------------------------

st.subheader("✅ Skills You Already Have")


current_skills = roadmap_input.get(
    "current_skills",
    []
)


if current_skills:

    for skill in current_skills:

        st.write(
            f"**{skill['skill']}** "
            f"— {skill['proficiency']}"
        )

else:

    st.info(
        "No skills found."
    )


st.divider()


# --------------------------------------------------
# Partial Skills
# --------------------------------------------------

partial_skills = roadmap_input.get(
    "partial_skills",
    []
)


if partial_skills:

    st.subheader(
        "⚠️ Skills You Have But Need to Improve"
    )

    for skill in partial_skills:

        st.write(
            f"**{skill['skill']}**"
        )

        st.caption(
            f"{skill['importance']} • "
            f"Current: {skill['user_proficiency']} • "
            f"Required: {skill['required_proficiency']} • "
            f"Priority: {skill['priority']}"
        )

    st.divider()


# --------------------------------------------------
# Skill Gaps
# --------------------------------------------------

st.subheader("❌ Skills You Need to Learn")


skill_gaps = roadmap_input.get(
    "skill_gaps",
    []
)


if skill_gaps:

    for skill in skill_gaps:

        importance = skill.get(
            "importance",
            ""
        )

        required = skill.get(
            "required_proficiency",
            ""
        )

        priority = skill.get(
            "priority",
            ""
        )

        st.write(
            f"**{skill['skill']}**"
        )

        st.caption(
            f"{importance} • "
            f"Required: {required} • "
            f"Priority: {priority}"
        )

else:

    st.success(
        "🎉 You currently have no identified skill gaps!"
    )


st.divider()


# --------------------------------------------------
# Learning Priority
# --------------------------------------------------

st.subheader(
    "📚 Recommended Learning Order"
)


learning_priority = roadmap_input.get(
    "learning_priority",
    []
)


if learning_priority:

    for index, skill in enumerate(
        learning_priority,
        start=1
    ):

        st.write(
            f"**{index}. {skill}**"
        )

else:

    st.info(
        "No learning priority available."
    )


st.divider()


# --------------------------------------------------
# Continue to AI Roadmap
# --------------------------------------------------

st.subheader(
    "🤖 Ready for Your Personalized Roadmap?"
)

st.write(
    """
    Your skill analysis is complete.
    The next step is to generate a personalized
    learning roadmap based on your current skills,
    proficiency, target career, and skill gaps.
    """
)


if st.button(
    "🚀 Continue to AI Roadmap →",
    type="primary",
    use_container_width=True
):

    st.switch_page(
        "pages/ai_roadmap.py"
    )