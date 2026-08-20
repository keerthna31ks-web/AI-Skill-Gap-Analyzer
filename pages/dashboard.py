import streamlit as st

from utils.roadmap_storage import get_user_roadmaps
from utils.roadmap_progress import get_roadmap_progress
from models.skill import get_roadmap_input


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# CHECK LOGIN
# ==================================================

if "user" not in st.session_state:

    st.warning("Please login first.")

    if st.button("🔐 Go to Login"):

        st.switch_page(
            "pages/login.py"
        )

    st.stop()


# ==================================================
# USER
# ==================================================

user_id = st.session_state["user"][0]
user_name = st.session_state["user"][1]


# ==================================================
# HEADER
# ==================================================

st.title("📊 AI Skill Gap Analyzer Dashboard")

st.success(
    f"Welcome, {user_name}!"
)

st.divider()


# ==================================================
# PROFILE & SKILLS
# ==================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("👤 Profile")

    st.write(
        "Complete or update your profile."
    )

    if st.button(
        "Complete Profile",
        key="profile_button",
        use_container_width=True
    ):

        st.switch_page(
            "pages/profile.py"
        )


with col2:

    st.subheader("💻 Skills")

    st.write(
        "Add or update your technical skills."
    )

    if st.button(
        "Add Skills",
        key="skills_button",
        use_container_width=True
    ):

        st.switch_page(
            "pages/skill.py"
        )


st.divider()


# ==================================================
# SKILL GAP & ROADMAP
# ==================================================

col3, col4 = st.columns(2)


with col3:

    st.subheader("📊 Skill Gap Analysis")

    st.write(
        "Compare your current skills with your target career."
    )

    if st.button(
        "Analyze",
        key="analyze_button",
        use_container_width=True
    ):

        st.switch_page(
            "pages/skill_gap_analyser.py"
        )


with col4:

    st.subheader("📚 Learning Roadmap")

    st.write(
        "View your personalized AI learning roadmap."
    )

    if st.button(
        "View Roadmap",
        key="roadmap_button",
        use_container_width=True
    ):

        st.switch_page(
            "pages/ai_roadmap.py"
        )


st.divider()


# --------------------------------------------------
# Career Readiness
# --------------------------------------------------

st.divider()

st.subheader("🎯 Career Readiness")

roadmap_input = get_roadmap_input(
    st.session_state["user"][0]
)

if roadmap_input:

    target_career = roadmap_input.get(
        "target_career",
        "Not selected"
    )

    readiness = roadmap_input.get(
        "readiness_score",
        0
    )

    skill_gap = roadmap_input.get(
        "skill_gap_percentage",
        0
    )

    st.markdown(
        f"### 🤖 {target_career}"
    )

    st.write(
        "Your current readiness based on your skills "
        "and the requirements of your target career."
    )

    st.progress(
        readiness / 100
    )

    st.write(
        f"**{readiness:.0f}% Career Ready**"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎯 Career Readiness",
            f"{readiness:.0f}%"
        )

    with col2:

        st.metric(
            "📉 Skill Gap",
            f"{skill_gap:.0f}%"
        )

else:

    st.info(
        "Complete your profile and add your skills "
        "to see your career readiness."
    )


# ==================================================
# LEARNING PROGRESS
# ==================================================

st.subheader("📊 Your Learning Progress")


# --------------------------------------------------
# Get User Roadmaps
# --------------------------------------------------

roadmaps = get_user_roadmaps(
    user_id
)


if roadmaps:

    # --------------------------------------------------
    # Latest Roadmap
    # --------------------------------------------------

    latest_roadmap = roadmaps[0]

    roadmap_id = latest_roadmap["roadmap_id"]

    roadmap = latest_roadmap["roadmap_json"]

    career = roadmap.get(
        "career",
        latest_roadmap["career"]
    )


    # --------------------------------------------------
    # Get Phases
    # --------------------------------------------------

    phases = roadmap.get(
        "phases",
        []
    )


    # --------------------------------------------------
    # Count Total Topics
    # --------------------------------------------------

    total_topics = 0

    for phase in phases:

        topics = phase.get(
            "topics",
            []
        )

        total_topics += len(
            topics
        )


    # --------------------------------------------------
    # Get Saved Progress
    # --------------------------------------------------

    progress = get_roadmap_progress(
        user_id,
        roadmap_id
    )


    # --------------------------------------------------
    # Count Completed Topics
    # --------------------------------------------------

    completed_count = 0

    for item in progress:

        if item["completed"]:

            completed_count += 1


    # --------------------------------------------------
    # Calculate Progress
    # --------------------------------------------------

    if total_topics > 0:

        progress_percentage = (
            completed_count /
            total_topics
        ) * 100

    else:

        progress_percentage = 0


    remaining_topics = (
        total_topics -
        completed_count
    )


    # --------------------------------------------------
    # Progress Card
    # --------------------------------------------------

    with st.container(border=True):

        st.markdown(
            f"### 🤖 {career} Learning Roadmap"
        )

        st.write(
            "Track your learning progress."
        )

        st.progress(
            progress_percentage / 100
        )

        st.write(
            f"**{progress_percentage:.0f}% completed**"
        )


        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "✅ Completed",
                completed_count
            )


        with col2:

            st.metric(
                "📌 Remaining",
                remaining_topics
            )


        with col3:

            st.metric(
                "📚 Total Topics",
                total_topics
            )


    # --------------------------------------------------
    # Continue Learning
    # --------------------------------------------------

    if st.button(
        "📚 Continue Learning →",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/ai_roadmap.py"
        )


else:

    # --------------------------------------------------
    # No Roadmap Yet
    # --------------------------------------------------

    with st.container(border=True):

        st.info(
            "You haven't generated an AI roadmap yet."
        )

        st.write(
            "Complete your profile, add your skills, "
            "analyze your skill gap, and generate your "
            "personalized AI roadmap."
        )


    if st.button(
        "🤖 Create My AI Roadmap →",
        use_container_width=True
    ):

        st.switch_page(
            "pages/ai_roadmap.py"
        )


st.divider()


# ==================================================
# LOGOUT
# ==================================================

if st.button(
    "🚪 Logout",
    key="logout_button",
    use_container_width=True
):

    # Clear login session
    st.session_state.pop(
        "user",
        None
    )

    st.session_state.pop(
        "skills_saved",
        None
    )

    st.success(
        "Logged out successfully!"
    )

    # Go to main app/login page
    st.switch_page(
        "app.py"
    )