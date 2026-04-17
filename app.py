from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cle_TP_astro'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/astronomie_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    score = db.Column(db.Integer, nullable=False)
    resume = db.Column(db.Text, nullable=True)

class Telescope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    score = db.Column(db.Integer, nullable=False)
    resume = db.Column(db.Text, nullable=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password_hash, request.form.get('password')):
            login_user(user)
            return redirect(url_for('appareils_photo'))
        flash('Identifiants incorrects.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
        new_user = User(username=request.form.get('username'), password_hash=hashed)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/appareils-photo')
@login_required
def appareils_photo():
    return render_template('appareils.html', cameras=Camera.query.all())

@app.route('/telescopes')
@login_required
def telescopes():
    return render_template('telescopes.html', telescopes=Telescope.query.all())

@app.route('/photographies')
@login_required
def photographies():
    return render_template('photographies.html', photos=Photo.query.all())

def seed_data():
    db.drop_all() 
    db.create_all()

    photos = [
        Photo(
            title="Aurore Boréale Polaire", 
            url="images/aurore.jpg", 
            description="Les vents solaires interagissant avec l'atmosphère terrestre, créant un voile émeraude."
        ),
        Photo(
            title="L'Étincelle Cosmique", 
            url="images/nebuleuse.jpg", 
            description="Une nébuleuse gazeuse rougeoyante où naissent de nouvelles étoiles."
        ),
        Photo(
            title="Le Cœur Galactique", 
            url="images/galaxie.jpg",  
            description="Notre propre galaxie, la Voie Lactée, vue dans un ciel d'une pureté absolue."
        )
    ]
    
    appareils = [
        Camera(category='Amateur', brand='Sony', model='a6400', release_date=date(2019, 1, 15), score=4, resume='Compact, léger et très performant en basse lumière. Parfait pour les panoramas nocturnes.'),
        Camera(category='Amateur sérieux', brand='Nikon', model='D810A', release_date=date(2015, 2, 10), score=5, resume='Une édition spéciale Astro. Son filtre infrarouge modifié permet de capter la couleur rouge des nébuleuses.'),
        Camera(category='Professionnel', brand='Hasselblad', model='X1D II 50C', release_date=date(2019, 6, 19), score=5, resume='Appareil hybride moyen-format. Une dynamique d\'image époustouflante pour des clichés stellaires sans aucun grain.')
    ]

    telescopes = [
        Telescope(category='Téléscopes pour enfants', brand='Bresser', model='Messier AR-90', release_date=date(2014, 1, 1), score=4, resume='Une lunette classique au look rétro, idéale et robuste pour admirer les cratères de la Lune.'),
        Telescope(category='Automatisés', brand='ZWO', model='Seestar S50', release_date=date(2023, 7, 1), score=5, resume='Le futur de l\'astro : un robot compact de la taille d\'un livre qui s\'aligne et photographie les galaxies tout seul.'),
        Telescope(category='Téléscopes complets', brand='Meade', model='LX200-ACF 14"', release_date=date(2012, 1, 1), score=5, resume='Un véritable monstre d\'observatoire miniature (plus de 50kg) pour explorer le ciel très profond.')
    ]

    db.session.add_all(photos)
    db.session.add_all(appareils)
    db.session.add_all(telescopes)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
    app.run(debug=True, host='0.0.0.0')