import streamlit as st
from datetime import date

from database import (
    get_all_books,
    get_categories,
    issue_book,
    get_student_books,
    return_book,
    get_student_statistics,
    update_profile
)


# ==========================================
# DASHBOARD
# ==========================================

def show_dashboard(student):

    st.title("🏠 Student Dashboard")

    st.write(
        f"Welcome back, **{student['name']}** 👋"
    )

    stats = get_student_statistics(
        student["student_id"]
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Total Issues",
            stats["total_issues"]
        )

    with col2:
        st.metric(
            "📖 Active Books",
            stats["active_books"]
        )

    with col3:
        st.metric(
            "🔄 Returned",
            stats["returned_books"]
        )

    with col4:
        st.metric(
            "💰 Total Fine",
            f"₹{stats['total_fine']}"
        )

    st.markdown("---")

    st.subheader("📚 Library Information")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            ### 📖 Issue Rules

            • Book issue period: **10 days**

            • Late return fine: **₹5 per day**

            • Return your books before the due date.
            """
        )

    with col2:

        st.success(
            """
            ### 🎓 Student Account

            **Name:** {}

            **Enrollment:** {}

            **Course:** {}

            **Semester:** {}
            """.format(
                student["name"],
                student["enrollment_no"],
                student["course"],
                student["semester"]
            )
        )


# ==========================================
# EXPLORE BOOKS
# ==========================================

def show_books(student):

    st.title("📚 Explore Books")

    books = get_all_books()

    if not books:
        st.warning("No books available.")
        return

    search = st.text_input(
        "🔍 Search Book",
        placeholder="Search by title or author..."
    )

    categories = ["All"] + get_categories()

    category = st.selectbox(
        "📂 Category",
        categories
    )

    filtered_books = []

    for book in books:

        title_match = (
            search.lower() in
            book["title"].lower()
        )

        author_match = (
            search.lower() in
            book["author"].lower()
        )

        category_match = (
            category == "All"
            or book["category"] == category
        )

        if (title_match or author_match) and category_match:
            filtered_books.append(book)

    st.markdown("---")

    if not filtered_books:

        st.warning("No matching books found.")
        return

    for book in filtered_books:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.subheader(
                    f"📖 {book['title']}"
                )

                st.write(
                    f"**Author:** {book['author']}"
                )

                st.write(
                    f"**Category:** {book['category']}"
                )

                st.write(
                    f"**ISBN:** {book['isbn']}"
                )

                st.write(
                    f"Available: "
                    f"**{book['available_copies']} / "
                    f"{book['total_copies']}**"
                )

            with col2:

                if book["available_copies"] > 0:

                    if st.button(
                        "Issue Book",
                        key=f"issue_{book['book_id']}",
                        use_container_width=True
                    ):

                        success, message = issue_book(
                            student["student_id"],
                            book["book_id"]
                        )

                        if success:
                            st.success(message)
                            st.rerun()

                        else:
                            st.error(message)

                else:

                    st.error("Unavailable")


# ==========================================
# MY BOOKS
# ==========================================

def show_my_books(student):

    st.title("📖 My Books")

    records = get_student_books(
        student["student_id"]
    )

    if not records:

        st.info(
            "You have not issued any book yet."
        )
        return

    active_books = [
        book for book in records
        if book["status"] == "Issued"
    ]

    returned_books = [
        book for book in records
        if book["status"] == "Returned"
    ]

    # ======================================
    # ACTIVE BOOKS
    # ======================================

    st.subheader(
        f"📚 Currently Issued ({len(active_books)})"
    )

    if not active_books:

        st.info("No active books.")

    for book in active_books:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.subheader(
                    f"📖 {book['title']}"
                )

                st.write(
                    f"Author: **{book['author']}**"
                )

                st.write(
                    f"Issue Date: **{book['issue_date']}**"
                )

                st.write(
                    f"Due Date: **{book['due_date']}**"
                )

                due_date = date.fromisoformat(
                    book["due_date"]
                )

                today = date.today()

                if today > due_date:

                    late_days = (
                        today - due_date
                    ).days

                    st.error(
                        f"⚠️ {late_days} day(s) late"
                    )

                else:

                    remaining = (
                        due_date - today
                    ).days

                    if remaining <= 1:

                        st.warning(
                            "⚠️ Book is due very soon!"
                        )

                    else:

                        st.success(
                            f"✓ {remaining} days remaining"
                        )

            with col2:

                if st.button(
                    "Return Book",
                    key=f"return_{book['issue_id']}",
                    use_container_width=True
                ):

                    success, message = return_book(
                        book["issue_id"],
                        student["student_id"]
                    )

                    if success:

                        st.success(message)
                        st.rerun()

                    else:

                        st.error(message)

    # ======================================
    # RETURN HISTORY
    # ======================================

    st.markdown("---")

    st.subheader("📜 Return History")

    if not returned_books:

        st.info("No returned books yet.")

    else:

        for book in returned_books:

            with st.container(border=True):

                st.write(
                    f"📖 **{book['title']}**"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"Issue: {book['issue_date']}"
                    )

                with col2:

                    st.write(
                        f"Returned: {book['return_date']}"
                    )

                with col3:

                    if book["fine"] > 0:

                        st.error(
                            f"Fine: ₹{book['fine']}"
                        )

                    else:

                        st.success("Fine: ₹0")


# ==========================================
# PROFILE
# ==========================================

def show_profile(student):

    st.title("👤 My Profile")

    col1, col2 = st.columns([1, 2])

    with col1:

        if student["profile_photo"]:

            st.image(
                student["profile_photo"],
                width=180
            )

        else:

            st.markdown(
                """
                <div style="
                    font-size:90px;
                    text-align:center;
                ">
                👤
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:

        st.subheader(student["name"])

        st.write(
            f"📧 **Email:** {student['email']}"
        )

        st.write(
            f"🎓 **Enrollment:** "
            f"{student['enrollment_no']}"
        )

        st.write(
            f"💻 **Course:** {student['course']}"
        )

        st.write(
            f"📚 **Semester:** {student['semester']}"
        )

    st.markdown("---")

    st.subheader("✏️ Edit Profile")

    name = st.text_input(
        "Name",
        value=student["name"]
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
        ],
        index=(
            [
                "B.Tech CSE",
                "B.Tech AI & ML",
                "B.Tech IT",
                "BCA",
                "MCA",
                "MBA",
                "BBA",
                "Other"
            ].index(student["course"])
            if student["course"] in [
                "B.Tech CSE",
                "B.Tech AI & ML",
                "B.Tech IT",
                "BCA",
                "MCA",
                "MBA",
                "BBA",
                "Other"
            ]
            else 0
        )
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
        ],
        index=(
            [
                "1st",
                "2nd",
                "3rd",
                "4th",
                "5th",
                "6th",
                "7th",
                "8th"
            ].index(student["semester"])
            if student["semester"] in [
                "1st",
                "2nd",
                "3rd",
                "4th",
                "5th",
                "6th",
                "7th",
                "8th"
            ]
            else 0
        )
    )

    new_photo = st.file_uploader(
        "Change Profile Photo",
        type=["jpg", "jpeg", "png"]
    )

    if st.button(
        "💾 Save Profile",
        type="primary"
    ):

        photo_bytes = None

        if new_photo:

            photo_bytes = new_photo.getvalue()

        update_profile(
            student["student_id"],
            name,
            course,
            semester,
            photo_bytes
        )

        st.success(
            "Profile updated successfully!"
        )

        st.rerun()


# ==========================================
# SETTINGS
# ==========================================

def show_settings():

    st.title("⚙️ Settings")

    st.subheader("📚 Library Rules")

    st.write(
        "• Maximum issue period: 10 days"
    )

    st.write(
        "• Late fine: ₹5 per day"
    )

    st.write(
        "• Student data is stored locally."
    )

    st.write(
        "• Library database: SQLite"
    )

    st.markdown("---")

    st.subheader("🔐 Privacy")

    st.info(
        "Your password is stored as a secure hash "
        "instead of plain text."
    )


# ==========================================
# MAIN LIBRARY ROUTER
# ==========================================

def run_library(student):

    page = st.session_state.get(
        "page",
        "Dashboard"
    )

    if page == "Dashboard":

        show_dashboard(student)

    elif page == "Explore Books":

        show_books(student)

    elif page == "My Books":

        show_my_books(student)

    elif page == "Profile":

        show_profile(student)

    elif page == "Settings":

        show_settings()

    else:

        show_dashboard(student) 