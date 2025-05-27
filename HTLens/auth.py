import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from ldap3 import Server, Connection, ALL, SUBTREE

from HTLens.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        server = Server(current_app.config['LDAP_SERVER'], get_info=ALL)
        
        # Step 1: Bind as read-only user to search for user's DN
        try:
            with Connection(server, current_app.config['LDAP_BIND_DN'], current_app.config['LDAP_BIND_PASSWORD'], auto_bind=True) as conn:
                conn.search(
                    search_base=current_app.config['LDAP_BASE_DN'],
                    search_filter=current_app.config['LDAP_USER_FILTER'].format(username),
                    search_scope=SUBTREE,
                    attributes=['uid', 'displayName', 'memberOf']
                )
                if not conn.entries:
                    flash('User not found')
                    return render_template('auth/login.html')

                entry = conn.entries[0]
                user_dn = entry.entry_dn
                uid = entry['uid'].value
                displayName = entry['displayName'].value
                memberOf = entry['memberOf'].value

        except Exception as e:
            flash(f'LDAP search failed: {e}')
            return render_template('auth/login.html')

        # Step 2: Try binding as the user
        try:
            user_conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        except Exception:
            flash('Invalid credentials')
            return render_template('auth/login.html')
        
        ensureUserExists(uid, displayName, memberOf)
        session['uid'] = uid
        session['displayName'] = displayName
        return redirect(url_for('index'))

    return render_template('auth/login.html')


def ensureUserExists(uid, displayName, memberOf):
    db = get_db()
    user = db.execute("SELECT 1 FROM user WHERE uid = ? LIMIT 1", (uid,)).fetchone()
    if user is None:
        accessLevel = 0
        # 0 none, 1 read only, 2 can post, 3 social media manager, 4 admin
        type = 'undefined'
        klasse = None
        if 'cn=lehrer,ou=groups,dc=schule,dc=local' in memberOf:
            type = 'teacher'
            accessLevel = 2
        elif 'cn=schueler,ou=groups,dc=schule,dc=local' in memberOf:
            type = 'student'
            accessLevel = 2
            for potKlasse in current_app.config['KLASSEN']:
                if 'cn=' + potKlasse + ',ou=groups,dc=schule,dc=local' in memberOf:
                    klasse = potKlasse
        
        db.execute("INSERT INTO user (uid, displayName, type, accessLevel, klasse) VALUES (?, ?, ?, ?, ?)", (uid, displayName, type, accessLevel, klasse))
        db.commit()

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
