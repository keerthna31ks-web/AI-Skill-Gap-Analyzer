import streamlit as st
from utils.auth import register_user


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📝 Create Your Account")

st.write(
    "Create an account to start your personalized "
    "AI career journey."
)

st.divider()


# --------------------------------------------------
# Registration Form
# --------------------------------------------------

st.subheader("👤 Registration Details")

name = st.text_input(
    "Full Name",
    placeholder="Enter your full name"
)

email = st.text_input(
    "Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Create a password"
)


st.divider()


# --------------------------------------------------
# Register Button
# --------------------------------------------------

if st.button(
    "📝 Register",
    type="primary",
    use_container_width=True
):

    if not name.strip():

        st.warning("Please enter your full name.")

    elif not email.strip():

        st.warning("Please enter your email.")

    elif not password.strip():

        st.warning("Please enter your password.")

    else:

        try:

            register_user(
                name,
                email,
                password
            )

            st.success(
                "🎉 Registration successful!"
            )

            st.info(
                "Your account has been created. "
                "Please login to continue."
            )

            st.session_state["registration_success"] = True

        except Exception as e:

            st.error(
                f"Registration failed: {e}"
            )


# --------------------------------------------------
# Login Navigation
# --------------------------------------------------

st.divider()

st.subheader("Already have an account?")

if st.button(
    "🔐 Go to Login →",
    use_container_width=True
):

    st.switch_page(
        "pages/login.py"
    )