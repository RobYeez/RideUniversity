from flask import Flask, render_template, url_for, redirect, flash
# from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import SignUpForm, LoginForm
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import LoginManager
app = Flask(__name__)


# Secret key helps to keep the site secure
app.config['SECRET_KEY'] = 'RDSS2134C#++-ABC'
socketio = SocketIO(app)
login_manager = LoginManager()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@email.com' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/ride")
def ride():
    return render_template('ride.html', title='Ride')


@app.route("/drive")
def drive():
    return render_template('drive.html', title='Drive')


@app.route("/contacts")
def contacts():
    return render_template('contacts.html', title="Contacts")


# @login_manager.user_loader

# messages page


@app.route("/messages")
def messages():
    return render_template('messages.html', title='Messages')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received mye vent: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

# receiving messages
# @socketio.on('message')


# sending messages
# @socketio.on()

@app.route("/biography")
def bio():
    # {%%} <- at "bio.html" to change to non hardcode person
    return render_template('bio.html', title="Biography")


if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True)
    login_manager.init_app(app, debug=True)
