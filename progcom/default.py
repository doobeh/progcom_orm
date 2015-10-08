from flask import Blueprint, redirect, url_for, flash, request
from flask import current_app as app

mod = Blueprint('default', __name__)


"""
Homepage
"""
@mod.route('/')
def pick():
    if app.config["THIS_IS_THUNDERDOME"]:
        return redirect(url_for('thunder.thunder_splash_page'))

    id = l.needs_votes(request.user.email, request.user.id)
    if not id:
        flash("You have voted on every proposal!")
        return redirect(url_for('show_votes'))
    return redirect(url_for('kitten', id=id))