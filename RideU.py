from flask import Flask, render_template, url_for, redirect, flash
from forms import SignUpForm, LoginForm
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import LoginManager
app = Flask(__name__)


# Secret key helps to keep the site secure
app.config['SECRET_KEY'] = 'RDSS2134C#++-ABC'
socketio = SocketIO(app)
login_manager = LoginManager();


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

# @login_manager.user_loader

# messages page
@app.route("/messages")
def messages():
    return render_template('messages.html', title='Messages')
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

# receiving messages
# @socketio.on('message')


# sending messages
# @socketio.on()

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True)
    login_manager.init_app(app, debug=True)
