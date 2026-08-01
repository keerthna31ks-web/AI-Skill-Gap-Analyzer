import streamlit as st

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🤖 AI Skill Gap Analyzer")

st.markdown("""
Bridge the gap between your skills and your dream job.
""")
st.sidebar.title("📌 Navigation")

st.sidebar.info("""
Welcome to AI Skill Gap Analyzer!

This application helps you:
- Analyze your resume
- Identify missing skills
- Get a personalized learning roadmap
""")
st.sidebar.success("Ready to analyze your resume!")
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.header("📂 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose your resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:
        st.success("Resume uploaded successfully!")

with col2:
    st.header("🎯 Target Job")
    role = st.selectbox(
        "Select Your Dream Role",
        [
            "Data Engineer",
            "AI Engineer",
            "Machine Learning Engineer",
            "Data Scientist",
            "Backend Developer"
        ]
    )

    st.info(f"Selected Role: {role}")
    if st.button("🔍 Analyze Resume"):
        st.success("Resume analysis will start in the next module!")
st.divider()
st.subheader("📊 Features")

st.markdown("""
- ✅ Skill Gap Analysis
- 📚 Personalized Learning Roadmap
- 📄 ATS Resume Check
- 💼 Project Recommendations
- 🤖 AI Career Guidance
""")


st.divider()

st.caption(
    "© 2026 AI Skill Gap Analyzer | Developed by Keerthana K S"
)