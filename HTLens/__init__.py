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
        ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff', 'tif', 'heic', 'heif',
            'mp4', 'mov', 'webm', 'mkv', 'avi' },
        EXTENSIONS_MIME_DICT = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'bmp': 'image/bmp',
            'tiff': 'image/tiff',
            'tif': 'image/tiff',
            'heic': 'image/heic',
            'heif': 'image/heif',
            'mp4': 'video/mp4',
            'mov': 'video/quicktime',
            'webm': 'video/webm',
            'mkv': 'video/x-matroska',
            'avi': 'video/x-msvideo'
        },
        MAX_CONTENT_LENGTH = 1 * 1000 * 1000 * 10000,    # 1GB
        LDAP_SERVER = 'ldaps://ldaps.htlwy.at',
        LDAP_BIND_DN='cn=ldap-ro,ou=services,dc=schule,dc=local',
        LDAP_BIND_PASSWORD=os.getenv('LDAP_BIND_PASSWORD'),
        LDAP_BASE_DN = 'dc=schule,dc=local',
        LDAP_USER_FILTER = '(uid={})',
        KLASSEN = ['1ahit', '2ahit', '3ahit', '4ahit']
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

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
