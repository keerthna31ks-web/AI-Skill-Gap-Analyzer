import streamlit as st


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 52px;
        font-weight: 700;
        text-align: center;
        margin-top: 60px;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 21px;
        text-align: center;
        color: #666;
        margin-bottom: 40px;
    }

    .feature-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #ddd;
        min-height: 180px;
        font-size: 16px;
        color: #666;
        line-height: 1.6;
    }

    .feature-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 18px;
        color: #1f2937;
    }

    .section-title {
        text-align: center;
        font-size: 30px;
        font-weight: 600;
        margin-top: 50px;
        margin-bottom: 25px;
    }

    .hero-box {
        padding: 35px;
        border-radius: 20px;
        border: 1px solid #ddd;
        text-align: center;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Session Check
# --------------------------------------------------

logged_in = "user" in st.session_state


# --------------------------------------------------
# Hero Section
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 AI Skill Gap Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Discover your career path, identify your skill gaps,
        and build a personalized AI-powered learning roadmap.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Main Action
# --------------------------------------------------

if logged_in:

    user_name = st.session_state["user"][1]

    st.markdown(
        f"""
        <div class="hero-box">
            <h2>👋 Welcome back, {user_name}!</h2>
            <p>
                Continue your journey toward your dream career.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        if st.button(
            "🚀 Go to Dashboard",
            use_container_width=True,
            type="primary"
        ):

            st.switch_page(
                "pages/dashboard.py"
            )

else:

    st.markdown(
        """
        <div class="hero-box">
            <h2>🚀 Start Your Career Journey</h2>
            <p>
                Get personalized career recommendations
                and an AI-generated learning roadmap based
                on your skills and goals.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary"
        ):

            st.switch_page(
                "pages/login.py"
            )

    with col2:

        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):

            st.switch_page(
                "pages/register.py"
            )


# --------------------------------------------------
# How It Works
# --------------------------------------------------

st.markdown(
    '<div class="section-title">✨ How It Works</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">
                👤 01 — Your Profile
            </div>

            Tell us about your education, interests,
            and career goals.
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">
                💻 02 — Your Skills
            </div>

            Add your technical skills and
            proficiency levels.
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">
                📊 03 — Skill Gap
            </div>

            Discover what skills you need
            for your target career.
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">
                🤖 04 — AI Roadmap
            </div>

            Get a personalized learning journey
            generated by AI.
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Bottom Section
# --------------------------------------------------

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:60px;
        padding:25px;
        color:#777;
    ">
        <p>
            🎯 From your current skills to your dream career —
            one personalized journey.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)