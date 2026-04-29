# 🛡️ Identity Security Framework for EdTech

A professional, hands-on demonstration of **Authentication** and **Authorization** concepts in Cybersecurity, built with Python, Flask, and modern web technologies — designed for EdTech learners.

---

## 📋 Project Overview

This project implements a complete **Secure Login System** for an EdTtech platform. It demonstrates real-world identity and access management (IAM) patterns that are foundational to cybersecurity.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 User Registration | Secure sign-up with validation and duplicate detection |
| 🔑 User Login | Email + password authentication with session management |
| 🔒 Password Hashing | PBKDF2-SHA256 via `werkzeug.security` — plain text never stored |
| 🍪 Session Management | Flask-Login with `remember me` support and strong session protection |
| 🚪 Logout | Proper session termination |
| 🛡️ Protected Dashboard | `@login_required` route protection |
| 👥 Role-Based Access Control | Student vs Admin roles with different permissions |
| 🔧 Admin Panel | Exclusive to Admin role — view all registered users |
| 💬 Flash Messages | Success/error feedback on all user actions |
| 📱 Responsive UI | Bootstrap 5 with custom dark theme |
| 🗄️ SQLite Database | Lightweight, file-based database via Flask-SQLAlchemy |
| ❌ Error Handling | Custom 404/403/500 pages |

---

## 🔐 Authentication vs Authorization

### Authentication — *Who are you?*
> Verifying the identity of a user.

- User provides email + password
- System checks if email exists in the database
- Password is compared against the stored **hash** (never plain text)
- On success → session is created with `login_user()`
- Implemented via: `Flask-Login`, `werkzeug.security.check_password_hash`

### Authorization — *What can you do?*
> Controlling what an authenticated user is allowed to access.

- All logged-in users can access `/dashboard`
- Only users with `role = 'admin'` can access `/admin`
- Unauthorized access → HTTP 403 (Access Denied)
- Implemented via: `@login_required` decorator + `current_user.is_admin()` check

```
Authentication: login_user() ─────────────────► Session Created
Authorization:  current_user.is_admin() ──────► Allow / Deny
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Clone or download the project
cd identity-security-edtech

# 2. (Optional but recommended) Create virtual environment
python -m venv myenv
source myenv/bin/activate      
Windows: myenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

### Access the app
Open your browser and go to: **http://127.0.0.1:5000**

---

## 🏃 How to Run

```bash
python app.py
```

On first run, the app will:
1. Create the SQLite database at `instance/database.db`
2. Create all tables automatically
3. Seed a default **Admin** account:
   - **Email:** `admin@edtech.com`
   - **Password:** `Admin@1234`

---

## 📁 Folder Structure

```
identity-security-edtech/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── instance/
│   └── database.db         # SQLite database (auto-created)
│
├── templates/
│   ├── base.html           # Base layout with navbar & flash messages
│   ├── index.html          # Landing / home page
│   ├── signup.html         # Registration form + password strength meter
│   ├── login.html          # Login form + remember me
│   ├── dashboard.html      # Protected user dashboard
│   ├── admin.html          # Admin panel (role-restricted)
│   └── 404.html            # Error page (404 / 403 / 500)
│
└── static/
    └── style.css           # Custom CSS (dark theme)
```

---

## 🔒 Security Features

| Feature | Implementation |
|---------|----------------|
| Password Hashing | `werkzeug.security.generate_password_hash` (PBKDF2-SHA256) |
| No Plain Text Storage | `password_hash` column, never `password` |
| Session Protection | `SESSION_PROTECTION = 'strong'` in Flask-Login |
| Anti-Enumeration | Same error for "bad email" and "bad password" |
| Route Protection | `@login_required` decorator |
| Role Enforcement | `current_user.is_admin()` check before admin routes |
| Input Validation | Server-side length, format, and duplicate checks |
| Safe ORM Queries | SQLAlchemy parameterized queries (no raw SQL injection) |

---

## 📸 Screenshots

> _Add screenshots here after running the app_

| Page | Description |
|------|-------------|
| `/` | Landing page with concept overview |
| `/signup` | Registration with password strength meter |
| `/login` | Login with Remember Me |
| `/dashboard` | Protected user dashboard with security info |
| `/admin` | Admin panel with user table (admin only) |
| `/admin` (student) | Access Denied — HTTP 403 |

---

## 🚀 Future Enhancements

- [ ] **Email Verification** — confirm email on registration
- [ ] **Forgot Password** — password reset via email token
- [ ] **Login Attempt Limiter** — block after N failed attempts (Flask-Limiter)
- [ ] **Audit Logs** — track all login/logout events with timestamps
- [ ] **Two-Factor Authentication (2FA)** — TOTP via pyotp
- [ ] **JWT Authentication** — stateless API auth
- [ ] **OAuth 2.0** — Login with Google / GitHub
- [ ] **Dark / Light Mode Toggle**
- [ ] **Admin: Delete / Edit Users**
- [ ] **Password History** — prevent reuse of last N passwords

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3 | Backend language |
| Flask | Web framework |
| Flask-Login | Session & authentication management |
| Flask-SQLAlchemy | ORM for database interaction |
| SQLite | Lightweight file-based database |
| Werkzeug | Password hashing utilities |
| Bootstrap 5 | Responsive UI framework |
| HTML5 / CSS3 | Frontend structure and styling |
| Google Fonts | Playfair Display + IBM Plex Mono + Lato |

---

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

*Built for educational purposes — Identity & Access Management (IAM) concepts in Cybersecurity.*
