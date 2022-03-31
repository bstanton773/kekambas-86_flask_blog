from app import app
from flask import redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import SignUpForm, RegisterAddressForm, LoginForm
from app.models import User, Post, Address

@app.route('/')
def index():
    title = 'Home'
    posts = Post.query.all()
    return render_template('index.html', title=title, posts=posts)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    title = 'Sign Up'
    form = SignUpForm()
    # check if a post request and that the form is valid
    if form.validate_on_submit():
        # Get data from the validated form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Create a new user instance with form data
        new_user = User(email=email, username=username, password=password)
        return redirect(url_for('index'))

    return render_template('signup.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Log In'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            print('User has been logged in')
            return redirect(url_for('index'))
    return render_template('login.html', title=title, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register-address', methods=['GET', 'POST'])
@login_required
def register_address():
    title = 'Register Address'
    form = RegisterAddressForm()
    addresses = current_user.addresses.all()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        phone = form.phone_number.data
        Address(name=name, address=address, phone_number=phone, user_id=current_user.id)
        return redirect(url_for('index'))
    return render_template('register_address.html', title=title, form=form, addresses=addresses)