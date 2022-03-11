import os
import sys
from datetime import datetime

import click
from flask import Flask
from flask import redirect, url_for, abort, render_template, flash

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

from flask_migrate import Migrate

# 根据平台不同设置SQLite的uri
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 获取数据库对象
db = SQLAlchemy(app)

# 数据库迁移工具
migrate = Migrate(app, db)


# shell上下文处理器
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, migrate=migrate, Note=Note, Author=Author, Article=Article, Writer=Writer, Book=Book,
                Singer=Singer, Song=Song, Citizen=Citizen, Capital=Capital, Country=Country,
                Teacher=Teacher, Student=Student, Post=Post, Comment=Comment, Draft=Draft)


# 自定义数据库初始化命令
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after frop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        click.confirm("This operation will delete all database, do you want ti continue?", abort=True)
        db.drop_all()
        click.echo('Drop database!')
    db.create_all()
    click.echo('Initialized databse.')


# forms
class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Update')


class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')


# models
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=True)

    # 定义调用数据库查询时的显示格式
    def __repr__(self):
        return '<Note %s>' % self.body


# view
@app.route('/')
def index():
    form = DeleteNoteForm()
    notes = Note.query.all()
    return render_template('index.html', form=form, notes=notes)


@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        note.timestamp = datetime.now()
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved.')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        note.timestamp = datetime.now()
        db.session.commit()
        flash('Your note is updated.')
        return redirect(url_for('index'))
    # 在打开的页面中显示原来的note内容
    form.body.data = note.body
    return render_template('edit_note.html', form=form)


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted.')
    else:
        abort(400)
    return redirect(url_for('index'))


# 关系：
# 1. one to many
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship('Article')

    def __repr__(self):
        return '<Author %r>' % self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return '<Article %r>' % self.title


# 2. many to one
class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City')

    def __repr__(self):
        return '<Citizen %r>' % self.name


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return '<City %r>' % self.name


# 3. one to one
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True)
    capital = db.relationship('Capital', back_populates='country', uselist=False)

    def __repr__(self):
        return '<Country %r>' % self.name


class Capital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', back_populates='capital')

    def __repr__(self):
        return '<capital %r>' % self.name


# 4. many to many with association table
# 关联表
association_table = db.Table('association',
                             db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                             db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    grade = db.Column(db.String(20))
    teachers = db.relationship('Teacher',
                               secondary=association_table,  # 指定关联表
                               back_populates='students')

    def __repr__(self):
        return '<Student %r>' % self.name


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    office = db.Column(db.String(20))
    students = db.relationship('Student',
                               secondary=association_table,
                               back_populates='teachers')

    def __repr__(self):
        return '<Teacher %r>' % self.name


# 5. one to many + bidirectional relationship(双向关系)
class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    books = db.relationship('Book', back_populates='writer')

    def __repr__(self):
        return '<Writer %r>' % self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')

    def __repr__(self):
        return '<Book %r>' % self.name


# 6. one to many + bidirectional relationship + use backref to declare bidirectional relationship
class Singer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    songs = db.relationship('Song', backref='singer')

    def __repr__(self):
        return '<Singer %r>' % self.name


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    singer_id = db.Column(db.Integer, db.ForeignKey('singer.id'))

    def __repr__(self):
        return '<Song %r>' % self.name


# cascade级联
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    comments = db.relationship('Comment',
                               back_populates='post',
                               cascade='all, delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')


# event listening事件监听
class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    edit_time = db.Column(db.Integer, default=0)


@db.event.listens_for(Draft.body, 'set')
def increment_edit_time(target, value, oldvalue, initiator):
    if target.edit_time is not None:
        target.edit_time += 1

# # 等同于
# @db.event.listens_for(Draft.body, 'set', named=True)
# def increment_edit_time(**kwargs):
#     if kwargs['target'].edit_time:
#         kwargs['target'].edit_time += 1
