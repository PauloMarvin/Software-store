from enum import unique

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
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

class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer) #in cents
    stock = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))



class AddProduct(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])


class AddPublisher(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])

class AddDeveloper(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html',products = products)


@app.route('/product/<id>')
def product(id):

    product = Product.query.filter_by(id = id).first()
    form = AddToCart()
    return render_template('view-product.html', product = product, form = form)


@app.route('/add-to-cart')
def add_to_cart():
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/admin')
def admin():
    products = Product.query.all()
    products_in_stock = Product.query.filter(Product.stock > 0).count()
    return render_template('admin/index.html', admin=True, products=products,products_in_stock= products_in_stock)

@app.route('/admin/add',methods=['GET', 'POST'])
def add():
    form = AddProduct()

    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.image.data))

        new_product = Product(name=form.name.data, price=form.price.data, stock=form.stock.data,
                              description=form.description.data, image=image_url)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/add-product.html', admin=True, form=form)


@app.route('/admin/order')
def order():
    return render_template('admin/view-order.html', admin=True)


if __name__ == '__main__':
    app.run(debug=True)
