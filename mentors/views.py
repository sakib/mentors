#!venv/bin/python
from flask import redirect, url_for, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from mentors import app, db
from models import *
from collections import defaultdict
import os, json, requests, pprint
from datetime import timedelta


pp = pprint.PrettyPrinter(indent=4)


@app.route('/')
def index():
    # display mentors and allow searches by skill
    return render_template('index.html')


# API endpoint
@app.route('/mentors', methods=['GET', 'POST'])
def mentors():
    if request.method == 'GET':
        mentors = Mentor.query.all()
        json_mentors = map(get_mentor_json, mentors)
        return jsonify(mentors=json_mentors)
    if request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        mentor = Mentor(name=name, email=email)
        db.session.add(mentor)
        db.session.commit()
        return "success!"


# Manual add mentors form
@app.route('/addmentors', methods=['GET','POST'])
def addmentors():
    # support adding mentors
    if request.method == 'GET':
        return render_template('addmentors.html')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mentor = Mentor(name=name, email=email)
        db.session.add(mentor)
        db.session.commit()
        print name, email, " just signed up as a mentor!"
        return render_template('index.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('500.html'), 500


def get_mentor_json(mentor):
    return {'id': mentor.id,
            'name': mentor.name,
            'email': mentor.email}
