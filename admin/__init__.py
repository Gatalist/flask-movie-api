from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Movie, Genre, Producer, Star, Rating
from app import db
from app.service import save_image
from .forms import MovieForm, GenreForm, ProducerForm, StarForm
from settings import Config


bp_admin = Blueprint('admin', __name__, template_folder='templates')


@bp_admin.route('/', methods=['GET'])
def admin_home():
    genre = '/admin/genre/'
    movie = '/admin/movie/'
    producer = "/admin/producer/"
    rating = "/admin/rating"
    return render_template('admin/index.html', title='index', genre=genre,
                                            movie=movie, producer=producer, rating=rating)


@bp_admin.route('movie/', methods=['GET'])
def admin_movie():
    movies = Movie.query.all()
    link='/admin/movie/'
    return render_template('admin/admin_movie_list.html', title='index', url=link,
                                            movies=movies)


@bp_admin.route('movie/add', methods=['GET', 'POST'])
def admin_movie_add():

    def add_movie_genre_all(idd, genres_list):
        for i in genres_list:
            sql = f"INSERT INTO movie_genre (movie_id, genre_id) VALUES ({idd},{int(i)})"
            db.engine.execute(sql)
            db.session.commit()
        print('add:')


    genre = Genre.query.all()
    producer = Producer.query.all()
    star = Star.query.all()

    form = MovieForm()

    if genre:
        form.genres_id.choices = [(str(i.id), i.name) for i in genre]
    if producer:
        form.producer_id.choices = [(str(i.id), i.name) for i in producer]
    if star:
        form.rating_id.choices = [(str(i.id), i.value) for i in star]

    if form.validate_on_submit():
        form_image = save_image(form.poster.data, Config.FOLDER_MOVIE)
        print(form_image)

        movie = Movie(title=form.title.data, slug=form.slug.data,
                        release_date=form.release_date.data, rating_id=form.rating_id.data, 
                        producer_id=int(form.producer_id.data),
                        body=form.body.data, poster=form_image, user_id=current_user.id,
                        publication=form.publication.data)
        
        db.session.add(movie)
        db.session.commit()
        print('id', movie.id)
        if form.genres_id.data:
            add_movie_genre_all(movie.id, form.genres_id.data)
        return redirect(url_for('admin.admin_movie'))

    link='/admin/movie/'

    return render_template('admin/movie_change.html', title='index', url=link, form=form)


@bp_admin.route('movie/del/<idd>', methods=['GET'])
def admin_movie_dell(idd):
    print("movie dell")
    movie = Movie.query.filter(Movie.id==idd).first()
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('admin.admin_movie'))


@bp_admin.route('movie/<idd>', methods=['GET', 'POST'])
def admin_movie_change(idd):

    def get_movie_genre_all(idd):
        sql = f"SELECT genre_id FROM movie_genre WHERE movie_id={idd}"
        get_data = db.engine.execute(sql).fetchall()
        result = []
        if get_data:
            for i in get_data:
                result.append(f'{i[0]}')
            print('get:', result)
            return result
        return None
    
    def del_movie_genre_all(idd):
        sql = f"SELECT genre_id FROM movie_genre WHERE movie_id={idd}"
        get_data = db.engine.execute(sql).fetchall()
        if get_data:
            for i in get_data:
                sql = f"DELETE FROM movie_genre WHERE movie_id={idd} AND genre_id={i[0]}"
                db.engine.execute(sql)
            db.session.commit()
        print('del:')

    def add_movie_genre_all(idd, genres_list):
        for i in genres_list:
            sql = f"INSERT INTO movie_genre (movie_id, genre_id) VALUES ({idd},{int(i)})"
            db.engine.execute(sql)
            db.session.commit()
        print('add:')

    movie = Movie.query.filter(Movie.id==idd).first()
    genre = Genre.query.all()
    producer = Producer.query.all()
    star = Star.query.all()

    form = MovieForm(obj=movie)

    form.genres_id.choices = [(str(i.id), i.name) for i in genre]
    if get_movie_genre_all(idd):
        form.genres_id.data = get_movie_genre_all(idd)

    form.rating_id.choices = [(str(i.id), i.value) for i in star]
    form.producer_id.choices = [(str(i.id), i.name) for i in producer]

    if form.validate_on_submit():
        movie.title=form.title.data
        movie.slug=form.slug.data

        if form.genres_id.data:
            del_movie_genre_all(idd)
            add_movie_genre_all(idd, form.genres_id.data)

        movie.release_date=form.release_date.data
        # movie.rating_id=int(form.rating.data)
        movie.producer_id=int(form.producer_id.data)
        movie.body=form.body.data

        if form.poster.data:
            form_image = save_image(form.poster.data, Config.FOLDER_MOVIE)
            movie.poster=form_image
        movie.user_id = current_user.id
        movie.publication=form.publication.data
        db.session.commit()

        return redirect(url_for('admin.admin_movie'))

    link='/admin/movie/'

    return render_template('admin/movie_change.html', title='index', url=link,
                                                    movie=movie, form=form)


@bp_admin.route('genre/', methods=['GET'])
def admin_genre():
    genres = Genre.query.all()
    link='/admin/genre/'
    return render_template('admin/admin_genre_list.html', title='index', url=link, genres=genres)


@bp_admin.route('genre/add', methods=['GET', 'POST'])
def admin_genre_add():
    form = GenreForm()

    if form.validate_on_submit():
        genre = Genre(name=form.name.data)
        
        db.session.add(genre)
        db.session.commit()

        return redirect(url_for('admin.admin_genre'))

    link='/admin/genre/'
    return render_template('admin/genre_change.html', title='index', url=link, form=form)


@bp_admin.route('genre/del/<idd>', methods=['GET'])
def admin_genre_dell(idd):
    print("genre dell")
    genre = Genre.query.filter(Genre.id==idd).first()
    db.session.delete(genre)
    db.session.commit()

    return redirect(url_for('admin.admin_genre'))


@bp_admin.route('genre/<idd>', methods=['GET', 'POST'])
def admin_genre_change(idd):
    genre = Genre.query.filter(Genre.id==idd).first()

    form = GenreForm(obj=genre)

    if form.validate_on_submit():
        idd = current_user.id
        genre.name = form.name.data
       
        db.session.commit()

        return redirect(url_for('admin.admin_genre'))

    link='/admin/genre/'
    return render_template('admin/genre_change.html', title='index', url=link, genre=genre, form=form)


@bp_admin.route('producer/', methods=['GET'])
def admin_producer():
    producers = Producer.query.all()
    link='/admin/producer/'
    return render_template('admin/admin_producer_list.html', title='index', url=link, producers=producers)


@bp_admin.route('producer/add', methods=['GET', 'POST'])
def admin_producer_add():
    form = ProducerForm()

    if form.validate_on_submit():
        form_image = save_image(form.poster.data, Config.FOLDER_PRODUCER)
        producer = Producer(name=form.name.data, poster=form_image)
        
        db.session.add(producer)
        db.session.commit()

        return redirect(url_for('admin.admin_producer'))

    link='/admin/producer/'
    return render_template('admin/producer_change.html', title='index', url=link, form=form)


@bp_admin.route('producer/del/<idd>', methods=['GET'])
def admin_producer_dell(idd):
    print("product dell")
    producer = Producer.query.filter(Producer.id==idd).first()
    db.session.delete(producer)
    db.session.commit()

    return redirect(url_for('admin.admin_producer'))


@bp_admin.route('producer/<idd>', methods=['GET', 'POST'])
def admin_producer_change(idd):
    producer = Producer.query.filter(Producer.id==idd).first()
    form = ProducerForm(obj=producer)

    if form.validate_on_submit():
        form_image = save_image(form.poster.data, Config.FOLDER_PRODUCER)
        producer.name=form.name.data
        if form.poster.data:
            producer.poster=form_image

        db.session.commit()

        return redirect(url_for('admin.admin_producer'))

    link='/admin/producer/'
    return render_template('admin/producer_change.html', title='index', url=link, producer=producer, form=form)


@bp_admin.route('rating/', methods=['GET'])
def admin_rating():
    rating = Star.query.all()
    link='/admin/rating/'
    return render_template('admin/admin_rating_list.html', title='index', url=link, ratings=rating)


@bp_admin.route('rating/add', methods=['GET', 'POST'])
def admin_rating_add():
    form = StarForm()

    if form.validate_on_submit():
        star = Star(value=form.star.data)
        
        db.session.add(star)
        db.session.commit()

        return redirect(url_for('admin.admin_rating'))

    link='/admin/rating/'
    return render_template('admin/rating_change.html', title='index', url=link, form=form)


@bp_admin.route('rating/del/<idd>', methods=['GET'])
def admin_rating_dell(idd):
    print("rating dell")
    star = Star.query.filter(Star.id==idd).first()
    db.session.delete(star)
    db.session.commit()

    return redirect(url_for('admin.admin_rating'))


@bp_admin.route('rating/<idd>', methods=['GET', 'POST'])
def admin_rating_change(idd):
    star = Star.query.filter(Star.id==idd).first()
    form = StarForm(obj=star)

    if form.validate_on_submit():
        star.value=form.star.data
        db.session.commit()

        return redirect(url_for('admin.admin_rating'))

    link='/admin/rating/'
    return render_template('admin/rating_change.html', title='index', url=link, ratings=star, form=form)


