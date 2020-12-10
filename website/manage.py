# -*- coding: utf-8 -*-
# @Author  : LG

from app import create_app, db
from app.models import User, Article, Comment, Content_record, Manage_record, Side_Bar, Carousel, Recommendation, Experiment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import schedule

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Article=Article, Comment=Comment, Content_record=Content_record,
                Manage_record=Manage_record, Side_Bar=Side_Bar, Carousel=Carousel, Recommendation=Recommendation,
                Experiment=Experiment)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    manager.run()

    # app.run()
