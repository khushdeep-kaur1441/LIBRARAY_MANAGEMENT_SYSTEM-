# 📚 VIT Library Management System

A web-based **Library Management System** developed using **Python, Streamlit, and SQLite**. The system provides students with a simple interface to manage their library activities, including account creation, book exploration, book issuing, book returns, fine tracking, and profile management.

## 🌐 Live Demo

https://librarymanagementsyste.streamlit.app/

---

## 📌 Project Overview

The **VIT Library Management System** is designed to provide a student-friendly digital platform for managing library activities.

Instead of manually maintaining book issue and return records, the system stores student and book-related information in a **SQLite database** and provides an interactive web interface through **Streamlit**.

The system allows students to:

* Create a library account
* Login securely using their registered credentials
* Explore available books
* Search books by title or author
* Filter books by category
* Issue available books
* View currently issued books
* Return books
* Track due dates and fines
* View borrowing history
* Update their profile
* View library rules and settings

---

## 🎯 Objectives

The main objectives of this project are:

* To provide a simple digital library management system.
* To reduce manual book issue and return record keeping.
* To allow students to easily search and explore available books.
* To maintain student borrowing records using a database.
* To automatically calculate fines for late returns.
* To provide students with their own dashboard and borrowing information.

---

## ✨ Features

### 🔐 Student Authentication

* Student registration
* Student login
* Email and enrollment number validation
* Password hashing
* Profile photo support
* Logout functionality

### 📊 Student Dashboard

The dashboard provides an overview of:

* Total books/issues
* Currently active books
* Returned books
* Total fine
* Library rules
* Student account information

### 📖 Explore Books

Students can:

* Browse available books
* Search by title or author
* Filter books by category
* View author and ISBN
* Check available copies
* Issue an available book

### 📚 My Books

Students can:

* View currently issued books
* Check issue dates
* Check due dates
* See remaining days
* Identify overdue books
* Return books
* View return history
* View applicable fines

### 💰 Fine Calculation

The system automatically calculates late-return fines.

**Library Rule:**

* Issue period: **10 days**
* Late fine: **₹5 per day**

### 👤 Profile Management

Students can view and update:

* Name
* Course
* Semester
* Profile photo
* Enrollment number
* Email

### ⚙️ Settings

The settings section provides information about:

* Library rules
* Storage system
* Database
* Password handling

---

## 🛠️ Technologies Used

| Technology   | Purpose                             |
| ------------ | ----------------------------------- |
| Python       | Application logic                   |
| Streamlit    | Web application interface           |
| SQLite       | Database management                 |
| Pillow       | Image/profile photo handling        |
| Git & GitHub | Version control and project hosting |

---

## 🏗️ Project Structure

```text
VIT-Library-Management-System/
│
├── app.py
├── auth.py
├── database.py
├── library.py
├── VIT management system.py
│
├── requirements.txt
├── .gitignore
├── README.md
│
└── library.db
```

### File Description

| File               | Description                                                     |
| ------------------ | --------------------------------------------------------------- |
| `app.py`           | Main Streamlit application and navigation                       |
| `auth.py`          | Login and student registration functionality                    |
| `database.py`      | SQLite database operations                                      |
| `library.py`       | Dashboard, books, borrowing, profile and settings functionality |
| `requirements.txt` | Required Python packages                                        |
| `.gitignore`       | Files excluded from Git tracking                                |

---

## 🗄️ Database Design

The application uses **SQLite** for local data storage.

The main tables are:

### Students

Stores student information such as:

* Student ID
* Name
* Enrollment number
* Email
* Password hash
* Course
* Semester
* Profile photo
* Account creation date

### Books

Stores:

* Book ID
* Title
* Author
* Category
* ISBN
* Total copies
* Available copies

### Issued Books

Stores:

* Issue ID
* Student ID
* Book ID
* Issue date
* Due date
* Return date
* Status
* Fine

---

## 🔄 Application Workflow

```text
                ┌───────────────┐
                │     Student   │
                └───────┬───────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Login / Register │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    Dashboard     │
              └────────┬─────────┘
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
    Explore Books   My Books      Profile
          │            │
          ▼            ▼
      Issue Book   Return Book
                       │
                       ▼
                 Fine Calculation
```

---

## 🔒 Security

The project includes basic security measures such as:

* Passwords are stored using hashing rather than plain-text storage.
* Login requires valid registered credentials.
* Student records are associated with unique email and enrollment numbers.
* Database operations validate book availability and borrowing status.

> Note: This project is intended as an academic/student project and does not claim enterprise-level security.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

### 2. Open the Project Folder

```bash
cd YOUR-REPOSITORY
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Testing

The following scenarios can be tested in the application:

| Test Case                         | Expected Result                     |
| --------------------------------- | ----------------------------------- |
| Create a new account              | Account should be created           |
| Enter incorrect login credentials | Login should be rejected            |
| Search for a book                 | Matching books should be displayed  |
| Issue an available book           | Book should be issued successfully  |
| Issue an unavailable book         | Issue should not be allowed         |
| Return an issued book             | Book should be marked as returned   |
| Return a book late                | Fine should be calculated           |
| Update profile                    | Updated information should be saved |
| Try duplicate active issue        | Duplicate issue should be prevented |

---

## 📸 Screenshots

Add screenshots of the following application pages to this section:

* Login / Registration page
* Student Dashboard
* Explore Books
* My Books
* Profile
* Settings

Example:

```text
screenshots/
├── login.png
├── dashboard.png
├── books.png
├── my-books.png
└── profile.png
```

---

## 🚀 Future Enhancements

Possible future improvements include:

* Admin dashboard
* Librarian management panel
* Add/edit/delete books
* Student management for administrators
* Email notifications for due dates
* Online book reservation
* Advanced search and filtering
* Book cover images
* Cloud database integration
* Automated testing
* Deployment with a production database

---

## 🎓 Learning Outcomes

Through this project, the following concepts were applied:

* Python programming
* Streamlit web application development
* SQLite database management
* CRUD-style database operations
* Authentication and validation
* Session-state based navigation
* Data processing
* Error handling
* Git and GitHub project management

---

## 📋 Project Information

**Project:** VIT Library Management System
**Platform:** Streamlit
**Language:** Python
**Database:** SQLite
**Project Type:** Academic Project

---

## 👨‍💻 Author

**Student Project**

Developed as an academic project for demonstrating practical application development and database management concepts.

---

## 📄 License

This project is developed for academic and educational purposes.
