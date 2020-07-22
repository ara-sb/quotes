import os

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import logging

from quotes.auth import login_required
from quotes.db import get_db

UPLOAD_FOLDER = '/Users/ara/Documents/python/Ex_Files_Flask_Tutorial/quotes/static/user_files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('blog', __name__)

language = ['Spanish', 'English']


@bp.route('/')
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        'SELECT p.id, author, body, lang, tags, img_url, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    print(posts)
    logging.info(posts)
    return render_template('blog/index.html', posts=posts)


@bp.route('/filter', methods=('GET', 'POST'))
def filter_post():
    """Show filtered posts."""
    if request.method == 'POST':
        search_query = request.form['search_query']
        if not search_query:
            return redirect(url_for('blog.index'))

        db = get_db()
        filtered_posts = db.execute(
            'SELECT p.id, author, body, lang, tags, img_url, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE author LIKE ?'
            ' ORDER BY created DESC',
            ('%'+search_query+'%',)
        ).fetchall()
        return render_template('blog/index.html', posts=filtered_posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        author = request.form['author']
        body = request.form['body']
        lang = request.form['lang']
        tags = request.form['tags']
        error = None

        if not author:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                img_url = filename
                db.execute('INSERT INTO post (author, body, lang, tags, img_url, author_id)'
                           'VALUES (?, ?, ?, ?, ?, ?)',
                           (author, body, lang, tags, img_url, g.user['id']))
            else:
                db.execute('INSERT INTO post (author, body, lang, tags, author_id)'
                           'VALUES (?, ?, ?, ?, ?)',
                           (author, body, lang, tags, g.user['id']))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html', language=language)


def get_post(id, check_author=True):
    """Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = get_db().execute(
        'SELECT p.id, author, body, lang, tags, img_url, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        author = request.form['author']
        body = request.form['body']
        lang = request.form['lang']
        tags = request.form['tags']

        error = None

        if not author:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                img_url = filename
                db.execute('UPDATE post SET author = ?, body = ?, lang = ?, tags = ?, img_url = ?'
                           'WHERE id = ?',
                           (author, body, lang, tags, img_url, id)
                           )
            else:
                db.execute('UPDATE post SET author = ?, body = ?, lang = ?, tags = ?'
                           'WHERE id = ?',
                           (author, body, lang, tags, id)
                           )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post, language=language)


@ bp.route('/<int:id>/delete', methods=('POST',))
@ login_required
def delete(id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('blog.index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
