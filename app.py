from enum import unique

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
import sqlite3

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trendy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

data_base = sqlite3.connect('trendy.db')


class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True)
    valor = db.Column(db.Integer)
    estoque = db.Column(db.Integer)
    descricao = db.Column(db.String(500))
    imagem = db.Column(db.String(150))


# class Desenvolvedora(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(50), unique=True)
#     valor = db.Column(db.Integer)
#     estoque = db.Column(db.Integer)
#     descricao = db.Column(db.String(500))
#     imagem = db.Column(db.String(150))
#
#
# class Publicadora(db.Model):po
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(50), unique=True)
#     valor = db.Column(db.Integer)
#     estoque = db.Column(db.Integer)
#     descricao = db.Column(db.String(500))
#     imagem = db.Column(db.String(150))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product')
def product():
    return render_template('view-product.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/admin')
def admin():
    return render_template('admin/index.html', admin=True)


@app.route('/admin/add')
def add():
    return render_template('admin/add-product.html', admin=True)


@app.route('/admin/order')
def order():
    return render_template('admin/view-order.html', admin=True)


if __name__ == '__main__':
    manager.run()
