from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cle_secrete_super_securisee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/astronomie_db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) 
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    score = db.Column(db.Integer, nullable=False) # 
    resume = db.Column(db.Text, nullable=True) 

class Telescope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) 
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    score = db.Column(db.Integer, nullable=False) 
    resume = db.Column(db.Text, nullable=True) 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Inscription réussie. Connectez-vous !')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('appareils_photo'))
        else:
            flash('Identifiants incorrects.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/appareils-photo')
@login_required
def appareils_photo():
    cameras = Camera.query.all()
    return render_template('appareils.html', cameras=cameras)

@app.route('/telescopes')
@login_required
def telescopes():
    telescopes = Telescope.query.all()
    return render_template('telescopes.html', telescopes=telescopes)

@app.route('/photographies')
@login_required
def photographies():
    return render_template('photographies.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True, host='0.0.0.0')