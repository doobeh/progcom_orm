from .meta import db
from sqlalchemy.dialects import postgresql


class Vote(db.Model):
    __tablename__ = 'proposal_votes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), primary_key=True)
    choice = db.Column(db.Integer, default=0, nullable=False)
    nominate = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref=db.backref('votes'))
    added_on = db.Column(db.DateTime(timezone=True), server_default="now()")


class Proposal(db.Model):
    __tablename__ = 'proposal'
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime(timezone=True), server_default="now()")
    added_on = db.Column(db.DateTime(timezone=True), server_default="now()")
    vote_count = db.Column(db.Integer, default=0)
    votes = db.relationship('Vote', backref='proposal')
    review_group_id = db.Column(db.Integer, db.ForeignKey('review_group.id'))
    review_group = db.relationship('ReviewGroup', backref='proposals')
    withdrawn = db.Column(db.Boolean, default=False)
    author_emails = db.Column(postgresql.ARRAY(db.String))
    author_names = db.Column(postgresql.ARRAY(db.String))
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    audience = db.Column(db.Text, nullable=False)
    python_level = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    outline = db.Column(db.Text, nullable=False)
    additional_notes = db.Column(db.Text, nullable=True)
    additional_requirements = db.Column(db.Text, nullable=True)


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='discussions')
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'))
    proposal = db.relationship('Proposal', backref='discussions')
    body = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Boolean, default=False)

