import time
import random

from flask import render_template, redirect, url_for, session, request

from app import app
from app.models import db, User, Dish, Category, Order
from app.forms import RegisterForm, OrderForm, AuthFrom

SESSION_KEY_OF_CART = 'cart'


def text_to_cart():
    dishes_in_cart = session.get(SESSION_KEY_OF_CART, [])
    number_of_dishes = len(dishes_in_cart)
    if not number_of_dishes:
        return 'Корзина пуста'
    sum = 0
    for dish_in_cart, dish_amount in dishes_in_cart.items():
        dish_in_cart_entity = db.session.query(Dish).get(dish_in_cart)
        sum += dish_in_cart_entity.price * dish_amount
        print(dish_amount)
    return f'В корзине {number_of_dishes} {ending(number_of_dishes)} на сумму {sum} руб'


def ending(dish_number):
    remainder = dish_number % 10
    if remainder == 0 or remainder >= 5 or (10 <= dish_number <= 19):
        return 'блюд'
    elif remainder == 1:
        return 'блюдо'
    else:
        return 'блюда'


def get_user():
    username = ''
    user = session.get('user')
    if user:
        username = user['username']
    return username


@app.route('/')
def render_main():
    categories = db.session.query(Category).all()
    dishes = db.session.query(Dish).all()
    cart_text = text_to_cart()
    username = get_user()
    categories_random_dishes = []
    for cat in categories:
        categories_random_dishes.append({'category': cat, 'dish': random.sample(cat.dishes, 3)})
    return render_template('main.html', categories=categories_random_dishes, dishes=dishes, cart_text=cart_text, username=username)


@app.route('/register', methods=['GET', 'POST'])
def render_register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    elif request.method == 'POST':
        mail = form.mail.data
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data

        if not form.validate():
            return render_template('register.html', form=form)

        error_messages = []
        if password != password2:
            error_messages.append('Пароли не совпадают!')

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            error_messages.append('Пользователь с таким username уже существует!')

        existing_mail = User.query.filter_by(mail=mail).first()
        if existing_mail:
            error_messages.append('Пользователь с такой электропочтой уже существует!')

        if error_messages:
            return render_template('register.html', form=form, error_msg=' '.join(error_messages))

        user = User(mail=mail,
                    username=username,
                    password=password,
                    role='user')
        db.session.add(user)
        db.session.commit()
        return render_template('register_success.html', username=username)


@app.route('/auth', methods=['GET', 'POST'])
def render_auth():
    form = AuthFrom()
    if request.method == 'POST':
        user = User.query.filter_by(mail=form.mail.data).first()

        if user and user.password_valid(form.password.data):
            session["user"] = {
                "id": user.id,
                "username": user.username,
                "mail": user.mail,
                "role": user.role,
            }
            return redirect("/")
        else:
            return render_template('auth.html', form=form, error_msg='Неверное имя пользователя или пароль')
    return render_template('auth.html', form=form)


@app.route('/logout')
def render_logout():
    session.pop('user')
    return redirect(url_for('render_auth'))


@app.route('/account')
def render_account():
    username = get_user()
    return render_template('account.html', username=username)


@app.route('/cart')
def render_cart():
    username = get_user()
    dishes_dict = session.get(SESSION_KEY_OF_CART, [])
    dishes = []
    sum = 0
    for dish_id, dish_amount in dishes_dict.items():
        dish = db.session.query(Dish).get(dish_id)
        dishes.append({
            'id': dish.id,
            'price': dish.price,
            'title': dish.title,
            'amount': dish_amount
        })
        sum += dish.price * dish_amount
    form = OrderForm(order_sum=sum, order_cart=dishes_dict)

    is_auth = bool(session.get('user'))
    return render_template('cart.html', dishes=dishes, form=form, decline_dish=ending, username=username,
                           is_auth=is_auth, sum=sum)


@app.route('/ordered', methods=['POST'])
def render_ordered():
    form = OrderForm()
    client_name = form.client_name.data
    address = form.address.data
    phone = form.phone.data
    order_sum = form.order_sum.data
    dish_list = form.order_cart.data
    username = get_user()

    order = Order(date=time.time(),
                  client_name=client_name,
                  order_sum=order_sum,
                  phone=phone,
                  address=address,
                  dish_list=dish_list,
                  owner=User.query.filter_by(username=username).first(),
                  status='NEW')
    db.session.add(order)
    db.session.commit()
    mail = session['user']['mail']
    return render_template('ordered.html', mail=mail)


@app.route('/add_to_cart/<int:dish_id>')
def add_to_cart(dish_id):
    dishes_dict = session.get(SESSION_KEY_OF_CART, {})
    print(dishes_dict)
    dish_amount = dishes_dict.get(str(dish_id), 0)
    dishes_dict[str(dish_id)] = dish_amount + 1
    session[SESSION_KEY_OF_CART] = dishes_dict
    return redirect(url_for('render_main'))


@app.route('/delete_from_cart/<int:dish_id>')
def delete_from_cart(dish_id):
    dishes_dict = session.get(SESSION_KEY_OF_CART, {})
    del dishes_dict[dish_id]
    session[SESSION_KEY_OF_CART] = dishes_dict
    return redirect(url_for('render_cart'))


@app.route('/clear_cart')
def clear_cart():
    session[SESSION_KEY_OF_CART] = []
    return redirect(url_for('render_cart'))
