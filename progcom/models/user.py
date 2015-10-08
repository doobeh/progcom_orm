from flask_security import UserMixin, RoleMixin
from flask_security.utils import encrypt_password
from sqlalchemy.ext.hybrid import hybrid_property
from .meta import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), index=True),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), index=True)
)

bookmarks = db.Table(
    'bookmarks',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), index=True),
    db.Column('proposal_id', db.Integer(), db.ForeignKey('proposal.id'), index=True)
)

class User(db.Model, UserMixin):
    """ User Representation
    Relationships:
    -   A user can have potentially many bookmarked Proposals
    -   Can vote once on each ReviewGroup (Aka: Thunderdome)
    -   Can vote on each proposal.
    -   Has potentially many roles.
    """

    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), index=True, nullable=False)
    _password = db.Column('password', db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    confirmed_at = db.Column(db.DateTime())

    bookmarks = db.relationship('Proposal', secondary=bookmarks,
                                backref=db.backref('users', lazy='dynamic'))

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = encrypt_password(value)

    def __repr__(self):
        return self.username


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True)

    def __repr__(self):
        return self.name