from flask import Flask, request, redirect, url_for, render_template
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://localhost/flask_one_to_many"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
modus = Modus(app)
db = SQLAlchemy(app)
Migrate(app, db)


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    excuses = db.relationship('Excuse', backref='student', lazy='joined')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Excuse(db.Model):

    __tablename__ = "excuses"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    is_believable = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, content, is_believable, student_id):
        self.content = content
        self.is_believable = is_believable
        self.student_id = student_id


@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/students', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        new_student = Student(request.form['first_name'],
                              request.form['last_name'])
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', students=Student.query.all())


@app.route('/students/new')
def new():
    return render_template('new.html')


@app.route('/students/<int:id>/edit')
def edit(id):
    return render_template('edit.html', student=Student.query.get(id))


@app.route('/students/<int:id>/', methods=["GET", "PATCH", "DELETE"])
def show(id):
    found_student = Student.query.get(id)
    if request.method == b'PATCH':
        found_student.first_name = request.form['first_name']
        found_student.last_name = request.form['last_name']
        db.session.add(found_student)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == b'DELETE':
        db.session.delete(found_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('show.html', student=found_student)


# =========================================
#               EXCUSES ROUTES
# =========================================

@app.route('/students/<int:student_id>/excuses', methods=["GET", "POST"])
def excuse_index(student_id):
    if request.method == 'POST':
        new_excuse = Excuse(request.form.get('content'),
                            bool(request.form.get('is_believable')),
                            student_id)
        db.session.add(new_excuse)
        db.session.commit()
        return redirect(url_for('excuse_index', student_id=student_id))
    found_student = Student.query.get(student_id)
    return render_template('excuse_index.html', student=found_student)


@app.route('/students/<int:student_id>/excuses/new')
def excuse_new(student_id):
    return render_template('excuse_new.html', student_id=student_id)

@app.route('/students/<int:student_id>/excuses/<int:excuse_id>/edit')
def excuse_edit(student_id, excuse_id):
    found_student = Student.query.get(student_id)
    return render_template('excuse_edit.html', excuse=Excuse.query.get(excuse_id), student=found_student)

@app.route(
    '/students/<int:student_id>/excuses/<int:excuse_id>',
    methods=["GET", "PATCH", "DELETE"])
def excuse_show(student_id, excuse_id):
    found_excuse = Excuse.query.get(excuse_id)
    if request.method == b'PATCH':
        found_excuse.content = request.form['content']
        found_excuse.is_believable = bool(request.form['is_believable'])
        db.session.add(found_excuse)
        db.session.commit()
        return redirect(url_for('excuse_index', student_id=student_id))
    if request.method == b'DELETE':
        db.session.delete(found_excuse)
        db.session.commit()
        return redirect(url_for('excuse_index', student_id=student_id))
    else:
        found_student = found_excuse.student
        if found_excuse.is_believable:
            is_slacker = False
        else:
            is_slacker = True
        return render_template('excuse_show.html', excuse=found_excuse, student=found_student, slacker=is_slacker)
