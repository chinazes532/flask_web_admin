from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gen_user:%3CJ2SDeYc(N%7B%3Bmm@91.135.157.238:5432/default_db'
db = SQLAlchemy(app)


class Texts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def users():
    users = Users.query.order_by(Users.id).all()
    return render_template('users.html',
                           users=users)


@app.route('/texts')
def texts():
    texts = Texts.query.order_by(Texts.id).all()  # Сортировка по id
    return render_template('texts.html', texts=texts)


@app.route('/edit_text/<int:id>', methods=['GET', 'POST'])
def edit_text(id):
    text = Texts.query.get_or_404(id)
    if request.method == 'POST':
        text.text = request.form['text']
        db.session.commit()
        return redirect(url_for('texts'))
    return render_template('edit_text.html',
                           text=text)


@app.route('/products')
def products():
    products = Products.query.order_by(Products.id).all()
    return render_template('products.html',
                           products=products)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product = Products(name=request.form['name'],
                           description=request.form['description'],
                           price=request.form['price'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('add_product.html')


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Products.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']

        # Преобразуем строку в число с плавающей точкой
        try:
            product.price = float(request.form['price'])
        except ValueError:
            # Обработка ошибки, если преобразование не удалось
            return "Ошибка: цена должна быть числом", 400

        db.session.commit()
        return redirect(url_for('products'))

    return render_template('edit_product.html', product=product)


@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = Products.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))


if __name__ == '__main__':
    app.run()