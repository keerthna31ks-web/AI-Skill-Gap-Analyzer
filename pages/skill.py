import streamlit as st
from data.skills_data import skills
from models.skill import save_skills


st.set_page_config(
    page_title="Skills",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Add Your Skills")

st.write("Select the skills you currently have and choose your proficiency level.")

st.divider()


# Store skill → proficiency
selected_skills = {}


proficiency_levels = [
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert"
]


for category, skill_list in skills.items():

    st.subheader(category)

    cols = st.columns(2)

    for index, skill in enumerate(skill_list):

        with cols[index % 2]:

            selected = st.checkbox(
                skill,
                key=f"skill_{skill}"
            )

            if selected:

                proficiency = st.selectbox(
                    f"{skill} proficiency",
                    proficiency_levels,
                    key=f"proficiency_{skill}"
                )

                selected_skills[skill] = proficiency

    st.divider()


# Display selected skills

st.write("### Selected Skills")

if selected_skills:

    for skill, proficiency in selected_skills.items():

        st.write(
            f"✅ **{skill}** — {proficiency}"
        )

else:

    st.info("No skills selected yet.")




## --------------------------------------------------
# Save Skills
# --------------------------------------------------

if st.button(
    "💾 Save Skills",
    type="primary",
    use_container_width=True
):

    if "user" not in st.session_state:

        st.error("Please login first.")

    elif len(selected_skills) == 0:

        st.warning(
            "Please select at least one skill."
        )

    else:

        user = st.session_state["user"]
        user_id = user[0]

        save_skills(
            user_id,
            selected_skills
        )

        st.session_state["skills_saved"] = True

        st.success(
            "✅ Skills and proficiency saved successfully!"
        )


# --------------------------------------------------
# Continue to Skill Gap
# --------------------------------------------------

if st.session_state.get("skills_saved", False):

    st.info(
        "Your skills are ready. "
        "Now let's analyze your career skill gap."
    )

    if st.button(
        "📊 Continue to Skill Gap →",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/skill_gap_analyser.py"
        )