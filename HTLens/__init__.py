import os

from flask import Flask

from dotenv import load_dotenv
load_dotenv()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.urandom(512)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'HTLens.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'image_uploads'),
        PROFILEPICS_FOLDER=os.path.join(app.instance_path, 'profile_pictures'),
        ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff', 'tif', 'heic', 'heif' },
        MAX_CONTENT_LENGTH = 10 * 1000 * 1000,    # 10MB
        LDAP_SERVER = 'ldaps://ldaps.htlwy.at',
        LDAP_BIND_DN='cn=ldap-ro,ou=services,dc=schule,dc=local',
        LDAP_BIND_PASSWORD=os.getenv('LDAP_BIND_PASSWORD'),
        LDAP_BASE_DN = 'dc=schule,dc=local',
        LDAP_USER_FILTER = '(uid={})',
        KLASSEN = [
            '1ahet', '2ahet', '3ahet', '4ahet', '5ahet',
            '1ahmba', '1bhmba', '2ahmba', '2bhmba', '3ahmba', '3bhmba',
            '4ahmba', '4bhmba', '5ahmba', '5bhmba',
            '1ahwim', '1bhwim', '2ahwim', '2bhwim', '3ahwim', '3bhwim',
            '4ahwim', '4bhwim', '5ahwim', '5bhwim',
            '1ahit', '2ahit', '3ahit', '4ahit', '5ahit',
            '1afme', '2afme', '3afme', '4afme',
            '1aame/2akme', '2aame/2akme', '3aame/3akme',
            '4aame/4akme', '5aame/5akme', '6aame/6akme'
        ]
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import media
    app.register_blueprint(media.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
