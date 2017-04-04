#!venv/bin/python
from flask import redirect, url_for, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from mentors import app, db
from models import Mentor
from collections import defaultdict
import os, json, requests, pprint
from datetime import timedelta


pp = pprint.PrettyPrinter(indent=4)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('500.html'), 500
