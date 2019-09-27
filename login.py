from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin ,login_user,login_required,logout_user , current_user,fresh_login_required
from urllib.parse import urlparse,urljoin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/C:/Users/user/Desktop/Recommendation/login.db'
app.config['SECRET_KEY'] = 'thisissecret'
app.config['USE_SESSION_FOR_NEXT'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Login would be better'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = 'You need to re-login to access this page '

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#@app.route('/')
#def index():
 #   user = User.query.filter_by(username='Anthony').first()
 #   login_user(user)
 #   return 'You are now logged in'

@app.route('/login')
def login():
    session['next'] = request.args.get('next')
    return render_template('login.html')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/logmein', methods=['POST'])

def logmein():
    username = request.form['username']

    user = User.query.filter_by(username=username).first()

    if not user:
        return '<h1>User not found!</h1>'

    login_user(user,remember=True)

    if 'next' in session:
        next = session['next']

        if is_safe_url(next):
            return redirect(next)

    return '<h1>You are now logged in!</h1> '


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out'

@app.route('/home')
@login_required
def home():
    return 'The current user is' + current_user.username

@app.route('/fresh')
@fresh_login_required
def fresh():
    return '<h1> You have a fresh login!</h1>'

if __name__ == '__main__':
    app.run(debug=True)   