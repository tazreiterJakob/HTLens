from flask import send_from_directory, Blueprint, current_app
from HTLens.db import get_db, get_user
from werkzeug.exceptions import abort

bp = Blueprint('media', __name__, url_prefix='/media')

@bp.route('/<int:id>')
def download_media(id):
    db = get_db()
    media = db.execute('SELECT * FROM media WHERE id = ?', (id,)).fetchone()
    if media is None:
        abort(404, f"Media id {id} doesn't exist.")

    return send_from_directory(current_app.config["UPLOAD_FOLDER"], media['filename'])

@bp.route('/profile_pic/<string:uid>')
def download_profile_pic(uid):
    db = get_db()
    user = get_user(uid)
    if user is None:
        abort(404, f"User id {uid} doesn't exist.")

    if user['profilePicFilename'] is None:
        return send_from_directory(current_app.config["PROFILEPICS_FOLDER"], 'default.svg')

    return send_from_directory(current_app.config["PROFILEPICS_FOLDER"], user['profilePicFilename'])