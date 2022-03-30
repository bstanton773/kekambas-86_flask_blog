from app import app
from flask import redirect, render_template, url_for
from app.forms import SignUpForm, RegisterAddressForm
from app.models import User, Post, Address

@app.route('/')
def index():
    title = 'Home'
    user = {'id': 1, 'username': 'bstanton', 'email': 'brians@codingtemple.com'}
    posts = Post.query.all()
    return render_template('index.html', current_user=user, title=title, posts=posts)


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


@app.route('/login')
def login():
    title = 'Log In'
    return render_template('login.html', title=title)


@app.route('/register-address', methods=['GET', 'POST'])
def register_address():
    title = 'Register Address'
    form = RegisterAddressForm()
    addresses = Address.query.all()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        phone = form.phone_number.data
        Address(name=name, address=address, phone_number=phone)
        return redirect(url_for('index'))
    return render_template('register_address.html', title=title, form=form, addresses=addresses)