from flask import Blueprint,request, render_template
from flask import current_app as app

mod = Blueprint('thunderdome', __name__, url_prefix='/thunder')


@app.route('/')
def thunder_splash_page():
    return render_template('thunderdome.html',
                            groups=l.list_groups(request.user.id))