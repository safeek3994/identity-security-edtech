"""
Identity Security Framework for EdTech
=======================================
Demonstrates Authentication & Authorization concepts using Flask.

Author: Security Demo Project
Tech Stack: Python, Flask, Flask-Login, Flask-SQLAlchemy, SQLite
"""

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ─────────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────────
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'edtech-identity-secret-key-2024-change-in-prod')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PROTECTION'] = 'strong'  # Security: strong session protection

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# Flask-Login Setup
# ─────────────────────────────────────────────
login_manager = LoginManager(app)
login_manager.login_view = 'login'          # Redirect here if @login_required fails
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    """Tell Flask-Login how to reload user from session."""
    return User.query.get(int(user_id))


# ─────────────────────────────────────────────
# Database Model
# ─────────────────────────────────────────────
class User(db.Model, UserMixin):
    """
    User model — stores credentials and role.
    SECURITY: Passwords are NEVER stored in plain text.
               Only the bcrypt/werkzeug hash is stored.
    """
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True,  nullable=False)
    email         = db.Column(db.String(120), unique=True,  nullable=False)
    password_hash = db.Column(db.String(256),               nullable=False)
    role          = db.Column(db.String(20),  default='student', nullable=False)

    def set_password(self, password):
        """Hash and store password. Never saves raw password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a candidate password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Convenience check for admin role."""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username} [{self.role}]>'


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route('/')
def index():
    """Landing / home page."""
    return render_template('index.html')


# ── SIGNUP ──────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    AUTHENTICATION CONCEPT: Registration
    - Collect credentials
    - Validate input
    - Hash password before storing
    - Prevent duplicate accounts
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')
        role     = request.form.get('role', 'student')

        # ── Input Validation ─────────────────
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('signup.html')

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'danger')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('signup.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')

        if role not in ('student', 'admin'):
            role = 'student'

        # ── Duplicate Check ───────────────────
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'danger')
            return render_template('signup.html')

        if User.query.filter_by(username=username).first():
            flash('That username is already taken.', 'danger')
            return render_template('signup.html')

        # ── Create User (password hashed automatically) ───
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)   # ← HASHING happens here
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created for {username}! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# ── LOGIN ────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    AUTHENTICATION CONCEPT: Login
    - Verify email exists
    - Compare password hash (never compares plain text)
    - Start session via login_user()
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email       = request.form.get('email', '').strip().lower()
        password    = request.form.get('password', '')
        remember_me = 'remember' in request.form

        if not email or not password:
            flash('Please enter your email and password.', 'danger')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        # SECURITY: Same vague error for both "no user" and "wrong password"
        # This prevents user-enumeration attacks.
        if user is None or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')

        # ── Start Session ─────────────────────
        login_user(user, remember=remember_me)
        flash(f'Welcome back, {user.username}!', 'success')

        # Redirect to the page they originally tried to access
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard'))

    return render_template('login.html')


# ── DASHBOARD ────────────────────────────────
@app.route('/dashboard')
@login_required   # AUTHORIZATION: Must be logged in
def dashboard():
    """
    Protected page — requires active session.
    @login_required enforces AUTHENTICATION.
    """
    return render_template('dashboard.html', user=current_user)


# ── ADMIN PANEL ──────────────────────────────
@app.route('/admin')
@login_required   # Step 1: Must be authenticated
def admin():
    """
    AUTHORIZATION CONCEPT: Role-Based Access Control (RBAC)
    - @login_required → user must be logged in
    - role check       → user must have 'admin' role
    Two-layer protection: Authentication + Authorization
    """
    if not current_user.is_admin():
        # AUTHORIZATION DENIED — wrong role
        flash('Access Denied. Admin privileges required.', 'danger')
        return render_template('admin.html', access_denied=True), 403

    # Fetch all users to display in the admin panel
    all_users = User.query.order_by(User.role, User.username).all()
    return render_template('admin.html', users=all_users, access_denied=False)


# ── LOGOUT ───────────────────────────────────
@app.route('/logout')
@login_required
def logout():
    """End the user session."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ─────────────────────────────────────────────
# Error Handlers
# ─────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('404.html', error_code=403,
                           error_msg="Access Forbidden"), 403

@app.errorhandler(500)
def server_error(e):
    return render_template('404.html', error_code=500,
                           error_msg="Internal Server Error"), 500


# ─────────────────────────────────────────────
# Database Initialization
# ─────────────────────────────────────────────
def init_db():
    """Create tables and seed a default admin account."""
    with app.app_context():
        db.create_all()
        # Create a default admin if none exists
        if not User.query.filter_by(role='admin').first():
            admin = User(username='admin', email='admin@edtech.com', role='admin')
            admin.set_password('Admin@1234')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created → email: admin@edtech.com | password: Admin@1234")
        print("✅ Database initialized.")


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print("🚀 Identity Security Framework for EdTech is running...")
    print("   Visit: http://127.0.0.1:5000")
    app.run(debug=True)
