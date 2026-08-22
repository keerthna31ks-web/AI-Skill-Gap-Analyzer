import streamlit as st

from models.skill import (
    get_roadmap_input,
    mark_skill_learned
)
from models.profile import get_target_role

from utils.ai_roadmp import generate_ai_roadmap
from utils.roadmap_storage import get_user_roadmaps

from utils.roadmap_progress import (
    get_roadmap_progress,
    save_topic_progress,
    is_phase_completed
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Roadmap",
    page_icon="🤖",
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
# Get CURRENT Target Career
# --------------------------------------------------

target_role = get_target_role(user_id)


if not target_role:

    st.warning(
        "Please complete your profile and select a target career first."
    )

    if st.button(
        "👤 Go to Profile",
        type="primary"
    ):

        st.switch_page(
            "pages/profile.py"
        )

    st.stop()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 Your AI Learning Roadmap")

st.write(
    f"Personalized learning journey for **{user_name}**."
)

st.divider()


# --------------------------------------------------
# CURRENT TARGET CAREER
# --------------------------------------------------

st.subheader("🎯 Your Selected Target Career")

st.success(
    target_role
)


# --------------------------------------------------
# Get Saved Roadmaps
# --------------------------------------------------

roadmaps = get_user_roadmaps(user_id)


# --------------------------------------------------
# IMPORTANT:
# Only use roadmap that belongs to CURRENT target career
# --------------------------------------------------

matching_roadmap = None


for saved_roadmap in roadmaps:

    saved_career = saved_roadmap.get(
        "career"
    )

    roadmap_json = saved_roadmap.get(
        "roadmap_json",
        {}
    )

    roadmap_career = roadmap_json.get(
        "career"
    )

    # Check both stored career and JSON career
    if (
        saved_career == target_role
        or roadmap_career == target_role
    ):

        matching_roadmap = saved_roadmap
        break


# --------------------------------------------------
# Generate Roadmap if Current Career Has No Roadmap
# --------------------------------------------------

if matching_roadmap is None:

    st.info(
        f"No AI roadmap exists yet for **{target_role}**."
    )

    st.write(
        """
        Your current profile, skills, proficiency levels,
        career requirements, and skill gaps will be used
        to generate a roadmap specifically for your
        selected target career.
        """
    )


    if st.button(
        f"🚀 Generate {target_role} Roadmap",
        type="primary",
        use_container_width=True
    ):

        roadmap_input = get_roadmap_input(
            user_id
        )


        if not roadmap_input:

            st.error(
                "Your roadmap information is not available. "
                "Please complete your profile and skills first."
            )

        else:

            # --------------------------------------------------
            # Force CURRENT target career
            # --------------------------------------------------

            roadmap_input["career"] = target_role

            roadmap_input["target_career"] = target_role


            with st.spinner(
                f"🤖 AI is creating your {target_role} roadmap..."
            ):

                try:

                    generate_ai_roadmap(
                        roadmap_input,
                        user_id
                    )

                    st.success(
                        f"🎉 Your {target_role} roadmap is ready!"
                    )

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"Unable to generate roadmap: {e}"
                    )

    st.stop()


# --------------------------------------------------
# Latest MATCHING Roadmap
# --------------------------------------------------

latest_roadmap = matching_roadmap

roadmap = latest_roadmap["roadmap_json"]

roadmap_id = latest_roadmap["roadmap_id"]


# --------------------------------------------------
# Target Career
# --------------------------------------------------

career = roadmap.get(
    "career",
    latest_roadmap["career"]
)


st.subheader("🎯 Target Career")

st.success(
    career
)


# --------------------------------------------------
# Roadmap Summary
# --------------------------------------------------

summary = roadmap.get(
    "roadmap_summary",
    ""
)


if summary:

    st.subheader(
        "📖 Roadmap Overview"
    )

    st.write(
        summary
    )


st.divider()


# --------------------------------------------------
# Learning Journey
# --------------------------------------------------

st.subheader(
    "🗺️ Your Learning Journey"
)

st.write(
    "Follow the phases in order. "
    "Complete each topic as you learn it."
)


phases = roadmap.get(
    "phases",
    []
)
st.write("DEBUG PHASES:")
st.write(phases)
st.write("PHASE TYPE:")
st.write(type(phases))

for p in phases:
    st.write("ITEM:", p)
    st.write("TYPE:", type(p))


# --------------------------------------------------
# Load Saved Progress
# --------------------------------------------------

saved_progress = get_roadmap_progress(
    user_id,
    roadmap_id
)


completed_topics = {}


for item in saved_progress:

    key = (
        item["phase"],
        item["topic"]
    )

    completed_topics[key] = bool(
        item["completed"]
    )


# --------------------------------------------------
# Calculate Progress
# --------------------------------------------------

total_topics = 0
completed_count = 0


for phase in phases:

    topics = phase.get(
        "topics",
        []
    )

    phase_number = phase.get(
        "phase",
        ""
    )


    for topic in topics:

        topic_name = topic.get(
            "topic",
            "Topic"
        )

        total_topics += 1


        if completed_topics.get(
            (phase_number, topic_name),
            False
        ):

            completed_count += 1


progress_percentage = (

    (completed_count / total_topics) * 100

    if total_topics > 0

    else 0

)


# --------------------------------------------------
# Progress Overview
# --------------------------------------------------

st.subheader(
    "📊 Learning Progress"
)


st.progress(
    progress_percentage / 100
)


st.write(
    f"**{progress_percentage:.0f}% completed** "
    f"({completed_count} / {total_topics} topics)"
)


if (
    total_topics > 0
    and completed_count == total_topics
):

    st.success(
        "🎉 Congratulations! You completed the entire learning roadmap!"
    )

elif completed_count > 0:

    st.info(
        "🔥 Keep going! Continue with the next topic."
    )

else:

    st.info(
        "🚀 Start learning by completing your first topic."
    )


st.divider()


# --------------------------------------------------
# Learning Phases
# --------------------------------------------------

# --------------------------------------------------
# Learning Phases
# --------------------------------------------------

for phase in phases:

    phase_number = phase.get(
        "phase",
        ""
    )

    phase_skill = phase.get(
        "skill",
        "Learning Phase"
    )

    topics = phase.get(
        "topics",
        []
    )

    mini_project = phase.get(
        "mini_project"
    )

    topic_count = len(topics)

    project_text = (
        "🛠️ Mini Project"
        if mini_project
        else "No Mini Project"
    )

    # --------------------------------------------------
    # Phase
    # --------------------------------------------------

    with st.expander(
        f"📚 Phase {phase_number} — {phase_skill}"
        f" • {topic_count} Topics • {project_text}"
    ):

        # --------------------------------------------------
        # Why this phase?
        # --------------------------------------------------

        reason = phase.get(
            "reason",
            ""
        )

        if reason:

            st.markdown(
                "### 💡 Why Learn This?"
            )

            st.write(
                reason
            )

        # --------------------------------------------------
        # Topics
        # --------------------------------------------------

        st.markdown(
            "### 📌 Topics to Learn"
        )

        for index, topic in enumerate(
            topics,
            start=1
        ):

            topic_name = topic.get(
                "topic",
                "Topic"
            )

            description = topic.get(
                "description",
                ""
            )

            # --------------------------------------------------
            # Completion Status
            # --------------------------------------------------

            already_completed = completed_topics.get(
                (
                    phase_number,
                    topic_name
                ),
                False
            )

            topic_key = (
                f"completed_"
                f"{roadmap_id}_"
                f"{phase_number}_"
                f"{index}"
            )

            completed = st.checkbox(
                f"{index}. {topic_name}",
                value=already_completed,
                key=topic_key
            )

            # --------------------------------------------------
            # Save Progress
            # --------------------------------------------------

            if completed != already_completed:

                save_topic_progress(
                    user_id=user_id,
                    roadmap_id=roadmap_id,
                    phase=phase_number,
                    topic=topic_name,
                    completed=completed
                )

            # --------------------------------------------------
            # Description
            # --------------------------------------------------

            if description:

                st.write(
                    description
                )

            # --------------------------------------------------
            # Practice Tasks
            # --------------------------------------------------

            practice = topic.get(
                "practice",
                []
            )

            if practice:

                st.markdown(
                    "##### 📝 Practice"
                )

                for task in practice:

                    st.write(
                        f"• {task}"
                    )

        # --------------------------------------------------
        # Check Phase Completion
        # --------------------------------------------------

        phase_completed = is_phase_completed(
            user_id=user_id,
            roadmap_id=roadmap_id,
            phase=phase_number,
            topics=topics
        )

        # --------------------------------------------------
        # Phase Completed
        # --------------------------------------------------

        if phase_completed:

            if phase_skill:

                mark_skill_learned(
                    user_id,
                    phase_skill
                )

                st.success(
                    f"🎉 {phase_skill} phase completed! "
                    f"Your skill profile has been updated."
                )

        # --------------------------------------------------
        # Mini Project
        # --------------------------------------------------

        if mini_project:

            st.divider()

            st.markdown(
                "### 🛠️ Mini Project"
            )

            project_title = mini_project.get(
                "title",
                "Mini Project"
            )

            project_description = mini_project.get(
                "description",
                ""
            )

            skills_used = mini_project.get(
                "skills_used",
                []
            )

            st.markdown(
                f"**{project_title}**"
            )

            if project_description:

                st.write(
                    project_description
                )

            if skills_used:

                st.write(
                    "**Skills:** "
                    + ", ".join(
                        skills_used
                    )
                )


# --------------------------------------------------
# Final Project
# --------------------------------------------------

final_project = roadmap.get(
    "final_project"
)


if final_project:

    st.divider()

    st.subheader(
        "🏆 Final Project"
    )


    st.write(
        "Use everything you learned to build this final project."
    )


    st.markdown(
        f"### {final_project.get(
            'title',
            'Capstone Project'
        )}"
    )


    description = final_project.get(
        "description",
        ""
    )


    if description:

        st.write(
            description
        )


    skills_used = final_project.get(
        "skills_used",
        []
    )


    if skills_used:

        st.write(
            "**Skills:** "
            + ", ".join(
                skills_used
            )
        )


    expected_outcome = final_project.get(
        "expected_outcome",
        ""
    )


    if expected_outcome:

        st.markdown(
            "### 🎯 Expected Outcome"
        )

        st.write(
            expected_outcome
        )


# --------------------------------------------------
# Roadmap Information
# --------------------------------------------------

st.divider()


st.caption(
    f"Roadmap generated on "
    f"{latest_roadmap['created_at']}"
)

st.divider()

st.subheader("🎉 Your Learning Journey is Ready!")

st.write(
    "Continue learning from your roadmap and track your progress "
    "as you complete each topic."
)

if st.button(
    "🏠 Go to Dashboard",
    type="primary",
    use_container_width=True
):
    st.switch_page(
        "pages/dashboard.py"
    )

