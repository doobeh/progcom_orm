from flask.ext.script import Manager, Shell
from progcom.models import (
    User, Role, ReviewGroup, ReviewVote,
    Vote, Proposal, Discussion, db
)
from flask.ext.migrate import Migrate, MigrateCommand
from progcom.core import app
from mixer.backend.flask import mixer

mixer.init_app(app)

def _make_context():
    return dict(
        app=app, db=db,
        User=User, Role=Role,
        ReviewGroup=ReviewGroup, ReviewVote=ReviewVote,
        Vote=Vote, Proposal=Proposal, Discussion=Discussion
    )

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=_make_context))
migrate = Migrate(app, db)



@manager.command
def nuke():
    db.reflect()
    db.drop_all()
    db.create_all()


@manager.command
def test_data():
    mixer.cycle(30).blend(User, password='yeck')
    mixer.cycle(50).blend(ReviewGroup)
    mixer.cycle(100).blend(Proposal, review_group=mixer.SELECT)
    mixer.cycle(200).blend(ReviewVote, review_group=mixer.SELECT, user=mixer.SELECT)
    mixer.cycle(30).blend(Vote, user=mixer.SELECT, proposal=mixer.SELECT)


@manager.command
def blank_slate():
    nuke()
    roles = [
        Role(name='admin'),
    ]

    db.session.add_all(roles)
    db.session.commit()

    admin = roles[0]
    user = User(username='anthony', password='password', roles=[admin])
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()