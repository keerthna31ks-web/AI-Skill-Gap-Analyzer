import streamlit as st
from models.profile import save_profile


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Complete Profile",
    page_icon="👤",
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
# Page Header
# --------------------------------------------------

st.title("👤 Complete Your Profile")

st.write(
    "Tell us about yourself so we can personalize "
    "your career recommendations and learning roadmap."
)

st.divider()


# --------------------------------------------------
# Basic Details
# --------------------------------------------------

st.subheader("📝 Basic Details")


name = st.text_input(
    "Full Name"
)


college = st.text_input(
    "College Name"
)


department = st.selectbox(
    "Department",
    [
        "Artificial Intelligence & Data Science",
        "Computer Science Engineering",
        "Information Technology",
        "Electronics and Communication Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Other"
    ]
)


year = st.selectbox(
    "Current Year",
    [
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year"
    ]
)


cgpa = st.number_input(
    "CGPA",
    min_value=0.0,
    max_value=10.0,
    step=0.1
)


st.divider()


# --------------------------------------------------
# Career Domain & Target Role
# --------------------------------------------------

st.subheader("🎯 Career Goal")


# --------------------------------------------------
# ALL CAREER DOMAINS
# Department does NOT restrict career choices
# --------------------------------------------------

career_roles = {

    # ==================================================
    # AI & MACHINE LEARNING
    # ==================================================

    "Artificial Intelligence & Machine Learning": [

        "AI Engineer",
        "Machine Learning Engineer",
        "Deep Learning Engineer",
        "Generative AI Engineer",
        "LLM Engineer",
        "Computer Vision Engineer",
        "NLP Engineer"

    ],


    # ==================================================
    # DATA SCIENCE & ANALYTICS
    # ==================================================

    "Data Science & Analytics": [

        "Data Scientist",
        "Data Analyst",
        "Data Engineer",
        "Business Analyst",
        "Analytics Engineer",
        "Big Data Engineer"

    ],


    # ==================================================
    # SOFTWARE DEVELOPMENT
    # ==================================================

    "Software Development": [

        "Software Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Mobile App Developer"

    ],


    # ==================================================
    # CLOUD & DEVOPS
    # ==================================================

    "Cloud & DevOps": [

        "Cloud Engineer",
        "Cloud Architect",
        "DevOps Engineer",
        "Site Reliability Engineer (SRE)"

    ],


    # ==================================================
    # CYBER SECURITY
    # ==================================================

    "Cyber Security": [

        "Cyber Security Analyst",
        "Security Engineer",
        "Ethical Hacker",
        "Penetration Tester"

    ],


    # ==================================================
    # DATABASE
    # ==================================================

    "Database": [

        "Database Administrator (DBA)",
        "Database Developer"

    ],


    # ==================================================
    # IOT & ROBOTICS
    # ==================================================

    "IoT & Robotics": [

        "IoT Engineer",
        "Robotics Engineer",
        "Embedded Systems Engineer"

    ],


    # ==================================================
    # TESTING & QA
    # ==================================================

    "Testing & Quality Assurance": [

        "QA Engineer",
        "Automation Test Engineer"

    ],


    # ==================================================
    # MANAGEMENT
    # ==================================================

    "Management": [

        "Product Manager",
        "Project Manager",
        "Technical Program Manager"

    ],


    # ==================================================
    # EMERGING TECHNOLOGIES
    # ==================================================

    "Emerging Technologies": [

        "MLOps Engineer",
        "AI Product Manager",
        "Prompt Engineer",
        "AI Research Engineer",
        "Blockchain Developer",
        "AR/VR Developer"

    ],


    # ==================================================
    # CIVIL ENGINEERING
    # ==================================================

    "Civil Engineering": [

        "Structural Engineer",
        "BIM Engineer",
        "Construction Engineer",
        "Transportation Engineer",
        "Environmental Engineer"

    ],


    # ==================================================
    # MECHANICAL ENGINEERING
    # ==================================================

    "Mechanical Engineering": [

        "Mechanical Design Engineer",
        "Manufacturing Engineer",
        "Automotive Engineer",
        "Thermal Engineer",
        "CAD Engineer"

    ],


    # ==================================================
    # ELECTRONICS & COMMUNICATION ENGINEERING
    # ==================================================

    "Electronics & Communication Engineering": [

        "Embedded Systems Engineer",
        "IoT Engineer",
        "Electronics Engineer",
        "VLSI Engineer",
        "Communication Engineer"

    ]

}


# --------------------------------------------------
# Career Domain
# --------------------------------------------------

career_domain = st.selectbox(
    "Career Domain",
    list(career_roles.keys())
)


# --------------------------------------------------
# Target Career
# --------------------------------------------------

target_role = st.selectbox(
    "Target Career",
    career_roles[career_domain]
)


st.divider()


# --------------------------------------------------
# Save Profile
# --------------------------------------------------

if st.button(
    "💾 Save Profile",
    type="primary",
    use_container_width=True
):

    if "user" not in st.session_state:

        st.error(
            "Please login first."
        )

    elif not name.strip():

        st.warning(
            "Please enter your full name."
        )

    elif not college.strip():

        st.warning(
            "Please enter your college name."
        )

    else:

        user_id = st.session_state["user"][0]


        # --------------------------------------------------
        # Save Profile to Database
        # --------------------------------------------------

        save_profile(
            user_id,
            name,
            college,
            department,
            year,
            cgpa,
            career_domain,
            target_role
        )


        # --------------------------------------------------
        # Session State
        # --------------------------------------------------

        st.session_state["profile_saved"] = True


        # --------------------------------------------------
        # Success Message
        # --------------------------------------------------

        st.success(
            "✅ Profile saved successfully!"
        )

        st.success(
            f"🎯 Target Career: {target_role}"
        )


# --------------------------------------------------
# Continue to Skills
# --------------------------------------------------

if st.session_state.get(
    "profile_saved",
    False
):

    st.info(
        "Your profile is complete. "
        "Now add your technical skills."
    )


    if st.button(
        "💻 Continue to Skills →",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/skill.py"
        )