import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'mentors'

SQLALCHEMY_DATABASE_URI = 'mysql://mentors:mentors@localhost/mentors'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
