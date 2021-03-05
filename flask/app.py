from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Library(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    
    def __repr__(self):
        return '<Library %r>' % self.id


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/library/all', methods = ['GET'])
def all():
    library = Library.query.order_by(Library.id).all()
    return render_template('all.html', library=library)


@app.route('/library', methods = ['POST', 'GET'])
def library():
    if request.method == 'POST':
        id = request.form['id']
        library = Library.query.order_by(Library.id).all()
        id = int(id)
        return render_template('solo.html', library=library, name=id)
    else:
        return render_template('library.html')


@app.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        id = request.form['id']
        text = request.form['text']

        library = Library(id=id, text=text)

        try:
            db.session.add(library)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении книги произошла ошибка'
    else:        
        return render_template('add.html')


if __name__ == '__main__':
    app.run()