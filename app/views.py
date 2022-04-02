from flask import render_template, flash, redirect, url_for, request, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Movie
from .schemas import VideoSchema
from flask_apispec import marshal_with, use_kwargs
from .service import save_image
from settings import Config


@app.route('/api', methods=['GET'])
@marshal_with(VideoSchema(many=True))
@login_required
def get_list():
    user_id = current_user.id
    return Movie.query.filter(Movie.user_id == user_id).all()


@app.route('/api', methods=['POST'])
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
@login_required
def update_list(**kwargs):
    user_id = current_user.id
    new = Movie(user_id=user_id, **kwargs)
    db.session.add(new)
    db.session.commit()

    return new


@app.route('/api/<int:tutorial_id>', methods=['PUT'])
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
@login_required
def update_tutorial(tutorial_id, **kwargs):
    user_id = current_user.id
    item = Movie.query.filter(Movie.id==tutorial_id, Movie.user_id == user_id).first()

    if not item:
        return {'message': 'No tutorials with this id'}, 400
    for key, value in kwargs.items():
        setattr(item, key, value)
    
    session.commit()

    return item


@app.route('/api/<int:tutorial_id>', methods=['DELETE'])
@marshal_with(VideoSchema)
@login_required
def delete_tutorial(tutorial_id):
    user_id = current_user.id
    item = Movie.query.filter(Movie.id==tutorial_id, Movie.user_id==user_id).first()
    
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    
    db.session.delete(item)
    db.session.commit()
    
    return '', 204




@app.route('/')
@login_required
def index():
    return render_template('index.html', title='index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        print('valid')
        user = User.query.filter_by(name=form.name.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid name or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, poster=save_image(form.poster.data, Config.FOLDER_USER))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<name>', methods=['GET', 'POST'])
@login_required
def user(name):
    user_id = current_user.id
    user = User.query.filter(User.id==user_id).first()
    movies = Movie.query.filter(Movie.user_id==user_id).all()
    return render_template('user.html', user=user, movies=movies)


@app.route('/movie', methods=['GET', 'POST'])
@login_required
def movie():
    movie_sorted = request.values.get('sorted')
    
    if movie_sorted:
        session['sorted'] = movie_sorted
    
    q = request.args.get('q')
    if q:
        if session['sorted']:
            if session['sorted'] == 'release_date.asc':
                movies = Movie.query.filter(Movie.title.contains(q) | Movie.body.contains(q)).order_by(Movie.release_date.asc())
            elif session['sorted'] == 'release_date.desc':
                movies = Movie.query.filter(Movie.title.contains(q) | Movie.body.contains(q)).order_by(Movie.release_date.desc())
        else:
            movies = Movie.query.filter(Movie.title.contains(q) | Movie.body.contains(q))
    else:
        if session['sorted']:
            if session['sorted'] == 'release_date.asc':
                print('release_date.asc')
                movies = Movie.query.order_by(Movie.release_date.asc())
            elif session['sorted'] == 'release_date.desc':
                print('release_date.desc')
                movies = Movie.query.order_by(Movie.release_date.desc())
        else:
            movies = Movie.query

    page = request.args.get('page', 1, type=int)
    pages = movies.paginate(page, 10, False)

    return render_template('movie_list.html', movies=movies, pages=pages, q=q)


@app.route('/movie/<slug>', methods=['GET'])
@login_required
def model_detail(slug):
    movie = Movie.query.filter(Movie.slug==slug).first()
    
    return render_template('movie_detail.html', movie=movie)
