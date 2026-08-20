import streamlit as st
from utils.auth import login_user

st.title("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if email == "" or password == "":
        st.warning("Please fill all fields.")

    else:

        user = login_user(email, password)

        if user:
            st.session_state["user"] = user

            st.success("Login Successful!")
            st.write(f"Welcome {user[1]}")

            # Go to dashboard
            st.switch_page("pages/dashboard.py")

        else:
            st.error("Invalid Email or Password")

            st.write("Don't have an account?")

            if st.button("📝 Register"):
                st.switch_page("pages/register.py")