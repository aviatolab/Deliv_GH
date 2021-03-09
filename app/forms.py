from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    mail = EmailField('Электропочта', [InputRequired(message="Введите что-нибудь")])
    username = StringField('Юзернейм', [InputRequired(message="Введите что-нибудь")])
    password = PasswordField('Пароль', [InputRequired(message="Введите что-нибудь"),
                                      Length(min=6, max=30, message="Длина от 6 до 30")])
    password2 = PasswordField('Пароль ещё раз', [InputRequired(message="Введите что-нибудь"),
                                               Length(min=6, max=30, message="Длина от 6 до 30")])
    submit = SubmitField('Зарегистрироваться')


class AuthFrom(FlaskForm):
    mail = StringField('Электропочта', [InputRequired(message="Введите что-нибудь")])
    password = PasswordField('Пароль', [InputRequired(message="Введите что-нибудь")])
    submit = SubmitField('Войти')


class OrderForm(FlaskForm):
    client_name = StringField('Ваше имя')
    address = StringField('Адрес')
    phone = StringField('Ваш телефон')
    order_sum = HiddenField()
    order_cart = HiddenField()
    submit = SubmitField('Оформить заказ')
