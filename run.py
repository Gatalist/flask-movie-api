from app import app
from settings import Config
from admin import bp_admin


app.register_blueprint(bp_admin, url_prefix='/admin')


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    