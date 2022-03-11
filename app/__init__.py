from flask import Flask
from settings import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
# serialized
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec



# base aplication
app = Flask(__name__) #, static_url_path='', static_folder='static', template_folder='templates')
app.config.from_object(Config)
app.static_url_path = Config.ROOT_PATH
app.template_folder = Config.TEMPLATES_FOLDER
app.static_folder = Config.STATIC_FOLDER


# test client for unit test
client = app.test_client()


# create instance DataBase
db = SQLAlchemy(app)


# class instance Migrate
migrate = Migrate(app, db)


# docs api
docs = FlaskApiSpec()
docs.init_app(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})


# class instance Login
login = LoginManager(app)
login.login_view = 'login'


# class instance Admin panel flask
admin = Admin(app)



from app import views  # conect views
from app.models import User, Movie  # conect model for migrations

# add model in see admin panel
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Movie, db.session))


docs.register(views.get_list)
docs.register(views.update_list)
docs.register(views.update_tutorial)
docs.register(views.delete_tutorial)

# функцию обработчика flask shell, вы можете работать с объектами базы данных, не импортируя их
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie}


# python -m flask db init – делаем снимок приложения
# python -m flask db migrate – создаем миграцию   # flask db migrate -m "Тут текст коммита"
# python -m flask db upgrade - сохранить (мигрировать)
# python -m flask db revision -m  "Initial migration"