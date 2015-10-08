from .meta import db
from sqlalchemy.dialects import postgresql


class ReviewGroup(db.Model):
    __tablename__ = 'review_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class ReviewVote(db.Model):
    __tablename__ = 'review_vote'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('review_votes', lazy='dynamic')
    )

    review_group_id = db.Column(db.Integer, db.ForeignKey('review_group.id'))
    review_group = db.relationship(
        'ReviewGroup', backref=db.backref('review_votes', lazy='dynamic')
    )

    accept = db.Column(
        postgresql.ARRAY(db.Integer, db.ForeignKey('proposal.id'))
    )
