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
    mentors = Mentor.query.all()
    return render_template('index.html', mentors=mentors)


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
        bio = request.form.get('bio')
        mentor = Mentor(name=name, email=email, bio=bio)

        skills = []
        all_skills = map(lambda x: x.name, Skill.query.all())
        skill_string = request.form.get('skills')
        skill_list = [x.strip() for x in skill_string.split(',')]
        for skill in skill_list:
            if name not in all_skills: # avoid duplicate skills
                skills.append(Skill(name=skill))

        # add mentor to mentor table
        db.session.add(mentor)
        db.session.commit()

        # add new skills to skill table
        for skill in skills:
            db.session.add(skill)
            db.session.commit()

        # add all skills to mapping between mentors and skills table
        for skill in skill_list: # just names
            skill_obj = Skill.query.filter_by(name=skill).first()
            mapping = MentorSkills(mentor_id=mentor.id, skill_id=skill_obj.id)
            db.session.add(mapping)

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
    mappings = MentorSkills.query.filter_by(mentor_id=mentor.id).all()
    skills = map(lambda x: Skill.query.filter_by(id=x.skill_id), mappings)
    skills_json = map(get_skill_json, skills)

    return {'id': mentor.id,
            'name': mentor.name,
            'email': mentor.email,
            'skills': skills_json}


def get_skill_json(skill):
    return {'id': skill.id,
            'name': skill.name}
