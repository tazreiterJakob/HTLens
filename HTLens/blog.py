from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, current_app
)
from werkzeug.exceptions import abort

from HTLens.db import get_db

from PIL import Image

import os

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    #db = get_db()
    #posts = db.execute(
    #    'SELECT p.id, title, body, created, author_id, username'
    #    ' FROM post p JOIN user u ON p.author_id = u.id'
    #    ' ORDER BY created DESC'
    #).fetchall()
    #return render_template('blog/index.html', posts=posts)
    return render_template('blog/index.html')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        db = get_db()
        curser = db.cursor()

        if 'images' not in request.files:
            flash("Images are required.")
            return redirect(request.url)

        title = request.form['title']
        description = request.form['description']
        tags = request.form['tags']
        files = request.files.getlist('images')

        if not title:
            flash("Titel is required.")
            return redirect(request.url)
        
        curser.execute(
            'INSERT INTO post (title, description, tags, user_id)'
            ' VALUES (?, ?, ?, ?)',
            (title, description, tags, session['uid'])
        )
        postId = curser.lastrowid


        for index, file in enumerate(files):
            filename = str(postId)+'_'+str(index)+'.webp'
            curser.execute(
                'INSERT INTO media (post_id, mime_type, filename)'
                ' VALUES (?, ?, ?)',
                (postId, "image/webp", filename)
            )

            try:
                # Open image and convert to RGB
                image = Image.open(file).convert('RGB')
                save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                # Save as WEBP
                image.save(save_path, format='WEBP')
            except Exception as e:
                print(e)
                flash('Error while saving images.')
                return redirect(request.url)
        

        db.commit()

        return redirect(url_for('blog.index'))

    return render_template('blog/create_test.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/search')
def search():
    return render_template('blog/search.html')

@bp.route('/profile')
def profile():
    return render_template('blog/profile.html')

@bp.route('/post')
def post():
    return render_template('blog/post.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config('ALLOWED_EXTENSIONS')