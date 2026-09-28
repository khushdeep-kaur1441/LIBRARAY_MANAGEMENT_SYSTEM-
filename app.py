import streamlit as st
from datetime import datetime

from database import init_database, get_student
from auth import login_page
from library import run_library


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="VIT LIBRARY MANAGEMENT SYSTEM",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0f172a,
            #1e3a8a
        );
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .auth-title {
        text-align: center;
        padding: 35px 10px;
        margin-bottom: 25px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );
        color: white;
    }

    .auth-title h1 {
        margin-bottom: 5px;
    }

    .auth-title p {
        font-size: 18px;
        margin: 0;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(
            0,
            0,
            0,
            0.08
        );
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

init_database()


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "student_id" not in st.session_state:

    st.session_state.student_id = None


if "page" not in st.session_state:

    st.session_state.page = "Dashboard"


# ==========================================
# LOGIN PAGE
# ==========================================

if not st.session_state.logged_in:

    login_page()

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:40px;
            color:#64748b;
        ">
            © 2026 SAM Global University
            Library Management System
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ==========================================
# GET CURRENT STUDENT
# ==========================================

student = get_student(
    st.session_state.student_id
)


if student is None:

    st.session_state.logged_in = False
    st.session_state.student_id = None

    st.rerun()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px;
        ">
            <h2>📚 Library</h2>
            <p>Student Portal</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Profile section

    if student["profile_photo"]:

        st.image(
            student["profile_photo"],
            width=100
        )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            margin-bottom:15px;
        ">
            <h3>{student["name"]}</h3>
            <p>{student["enrollment_no"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Navigation

    st.subheader("Navigation")

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):

        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button(
        "📚 Explore Books",
        use_container_width=True
    ):

        st.session_state.page = "Explore Books"
        st.rerun()

    if st.button(
        "📖 My Books",
        use_container_width=True
    ):

        st.session_state.page = "My Books"
        st.rerun()

    if st.button(
        "👤 My Profile",
        use_container_width=True
    ):

        st.session_state.page = "Profile"
        st.rerun()

    if st.button(
        "⚙️ Settings",
        use_container_width=True
    ):

        st.session_state.page = "Settings"
        st.rerun()

    st.markdown("---")

    # Date and time

    now = datetime.now()

    st.caption(
        f"📅 {now.strftime('%d %B %Y')}"
    )

    st.caption(
        f"🕐 {now.strftime('%I:%M:%S %p')}"
    )

    st.markdown("---")

    # Logout

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.student_id = None
        st.session_state.page = "Dashboard"

        st.rerun()


# ==========================================
# MAIN APPLICATION
# ==========================================

run_library(student)


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <hr>

    <div style="
        text-align:center;
        color:#64748b;
        padding:15px;
    ">

        📚 <b>VIT Library Management System</b>
        <br>
        Student Library Portal • Local Database

    </div>
    """,
    unsafe_allow_html=True
) 