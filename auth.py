import streamlit as st
from database import create_student, authenticate_student


def login_page():

    st.markdown(
        """
        <div class="auth-title">
            <h1>📚 VIT LIBRARY MANAGEMENT SYSTEM</h1>
            <p>Library Management System</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(["🔐 Login", "📝 Create Account"])

    # ==========================
    # LOGIN
    # ==========================

    with login_tab:

        st.subheader("Student Login")

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if not email or not password:

                st.error("Please enter email and password.")

            else:

                student = authenticate_student(
                    email,
                    password
                )

                if student:

                    st.session_state.logged_in = True
                    st.session_state.student_id = student["student_id"]
                    st.session_state.page = "Dashboard"

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

    # ==========================
    # SIGN UP
    # ==========================

    with signup_tab:

        st.subheader("Create Student Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        enrollment_no = st.text_input(
            "Enrollment Number",
            placeholder="Enter enrollment number"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter email",
            key="signup_email"
        )

        password = st.text_input(
            "Create Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        course = st.selectbox(
            "Course",
            [
                "B.Tech CSE",
                "B.Tech AI & ML",
                "B.Tech IT",
                "BCA",
                "MCA",
                "MBA",
                "BBA",
                "Other"
            ]
        )

        semester = st.selectbox(
            "Semester",
            [
                "1st",
                "2nd",
                "3rd",
                "4th",
                "5th",
                "6th",
                "7th",
                "8th"
            ]
        )

        profile_photo = st.file_uploader(
            "Profile Photo (Optional)",
            type=["jpg", "jpeg", "png"]
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if not name.strip():
                st.error("Please enter your name.")

            elif not enrollment_no.strip():
                st.error("Please enter enrollment number.")

            elif not email.strip():
                st.error("Please enter email.")

            elif not password:
                st.error("Please create a password.")

            elif len(password) < 6:
                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                photo_bytes = None

                if profile_photo is not None:
                    photo_bytes = profile_photo.getvalue()

                success, student_id, message = create_student(
                    name=name.strip(),
                    enrollment_no=enrollment_no.strip(),
                    email=email.strip().lower(),
                    password=password,
                    course=course,
                    semester=semester,
                    profile_photo=photo_bytes
                )

                if success:

                    st.success(message)

                    st.info(
                        "Account created successfully. "
                        "Now open the Login tab and login."
                    )

                else:

                    st.error(message)