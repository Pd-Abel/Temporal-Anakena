from flask import render_template, request, flash, redirect, url_for
from app import app, login_manager
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user
from app.models import users, User, get_user
from flask_login import login_required
from werkzeug.urls import url_parse

@app.route("/logout")
def logout():
    logout_user()
    return redirect( url_for( "login" ) )

@app.route("/index")
def index():
    return render_template("index.html", title = "user")


@app.route( "/"  )
@app.route( "/login" , methods = [ 'GET' , 'POST' ] )
def login():
    
    if current_user.is_authenticated :
        return redirect( url_for( 'index' ) )

    form = LoginForm() 
    if form.validate_on_submit():
        user = get_user( form.email.data )
        password = form.password.data  

        if user is not None and user.check_password(password):
            login_user( user, remember = form.remember_me.data )
            next_page = request.args.get( "next" )

            if not next_page or url_parse( next_page ).netloc != "" :
                next_page = url_for( "index" )
        
            return redirect(next_page)

    return render_template ( "login.html" , title = "Ingreso", form = form )

@app.route("/signup", methods = [ 'GET', 'POST' ] )
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = SignUpForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
        rol = form.rol.data

        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, email, password, rol)
        print (user)
        users.append(user)
        print (users)

        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template("signup.html", form=form)

@login_manager.user_loader
def load_user( user_id ) :
    for user in users:
        if user.id == int ( user_id ) :
            return user
        
    return None
    


