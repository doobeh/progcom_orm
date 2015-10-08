# -*- coding: utf-8 -*-
"""
    progcom.core
    ~~~~~~~~~~~~~
    the gears to get the machine turning.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from progcom.models import User, Role
from datetime import datetime
from jinja2 import Markup
import bleach
import markdown


def create_app(config_filename):
    factory_app = Flask(__name__)
    factory_app.config.from_pyfile(config_filename)
    return factory_app


app = create_app('../config.py')

# We use this to ease our pagination work.
app.jinja_env.add_extension('jinja2.ext.do')

from progcom.default import mod

app.register_blueprint(mod)

#: Flask-SQLAlchemy extension instance
db = SQLAlchemy()
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


def set_nofollow(attrs, new=False):
    attrs['target'] = '_blank'
    return attrs


@app.template_filter('date')
def date_filter(d):
    return d.strftime('%b-%-d %I:%M')


@app.template_filter('markdown')
def markdown_filter(s):
    raw = bleach.clean(markdown.markdown(s),
                       tags=bleach.ALLOWED_TAGS + ['p', 'h1', 'h2'])
    raw = bleach.linkify(raw, callbacks=[set_nofollow])
    return Markup(raw)


# Context:
@app.context_processor
def inject_data():
    return {
        'now': datetime.now()
    }
