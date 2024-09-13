from flask import Flask, request, render_template, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import bcrypt
from helper import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/lighthouseDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<UserEMAIL {self.email}>'

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


@app.route('/', methods=['GET', 'POST'])
def home():
    # Create admin user first time only
    # try:
    #     new_user = Person(email='admin@lighthouse.com', user_type='admin')
    #     new_user.set_password('123456')
    #
    #     # Add the new user to the session and commit
    #     db.session.add(new_user)
    #     db.session.commit()
    # except Exception as e:
    #     print(e)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Person.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user'] = user.email
            return jsonify({'message': 'success'})
            # return redirect('/dashboard', 302)
        else:
            return jsonify({'message': 'failed'})
    else:
        return render_template('user-login.html')


@app.route('/file_upload', methods=['POST', 'GET'])
def file_upload():
    if 'user' not in session:
        return redirect('/', 302)

    if request.method == 'POST':
        file = request.files['upfile']
        if file.filename.split('.')[-1] not in ['txt', 'doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png']:
            return jsonify({'message': 'failed', 'error': 'invalid_file_format'})

        try:
            file_pth = 'static/uploads/' + file.filename
            file.save(file_pth)
        except Exception as e:
            print(e)
            return jsonify({'message': 'failed'})

        if file.filename.split('.')[-1].lower() in ['txt', 'doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'tiff']:
            output = get_data_from_text(file_pth)
            return jsonify({'message': 'success', 'data': output})
        else:
            return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'failed'})


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'user' not in session:
        return redirect('/', 302)
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect('/', 302)


@app.route('/update_password', methods=['POST', 'GET'])
def update_password():
    if 'user' not in session:
        return redirect('/', 302)
    if request.method == 'POST':
        if request.form['old_pass'] and request.form['new_pass']:
            old_pass = request.form['old_pass']
            new_pass = request.form['new_pass']
            user = Person.query.filter_by(email=session['user']).first()
            if user and bcrypt.checkpw(old_pass.encode('utf-8'), user.password.encode('utf-8')):
                user.set_password(new_pass)
                db.session.commit()
                return jsonify({'message': 'success'})
            else:
                return jsonify({'message': 'failed'})
    else:
        return render_template('update-password.html')


if __name__ == '__main__':
    app.secret_key = '\xf0\xe18\xfe\x89\x19+\x1aU\xe8\x03\x12/i\xa5\xf5\xe7\x98e\x02\xde \xbb\xfb'
    app.config['SESSION_TYPE'] = 'filesystem'
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('Person'):
            db.create_all()  # This will create the table(s) in the database
    app.run(port=8000, debug=True)
