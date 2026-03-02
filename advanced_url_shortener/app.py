from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, URL
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import random, string
import validators
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create tables
with app.app_context():
    db.create_all()


# Generate unique short code
def generate_short_code():
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not URL.query.filter_by(short_code=code).first():
            return code


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Username length validation (5–9 chars)
        if len(username) < 5 or len(username) > 9:
            flash("Username must be between 5 to 9 characters long")
            return redirect(url_for('signup'))

        # Unique username check
        if User.query.filter_by(username=username).first():
            flash("This username already exists")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Signup successful! Please login.")
        return redirect(url_for('login'))

    return render_template('signup.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()

        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------------- HOME (URL SHORTENER) ----------------
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('url')

        # URL validation
        if not validators.url(original_url):
            flash("Invalid URL")
            return redirect(url_for('index'))

        short_code = generate_short_code()

        new_url = URL(
            original_url=original_url,
            short_code=short_code,
            user_id=current_user.id
        )

        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + short_code

    return render_template('index.html', short_url=short_url)


# ---------------- HISTORY ----------------
@app.route('/history')
@login_required
def history():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', urls=urls)


# ---------------- REDIRECT SHORT URL ----------------
@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.original_url)
    return "URL not found"


if __name__ == '__main__':
    app.run(debug=True)