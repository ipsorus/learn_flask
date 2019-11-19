from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()
with app.app_context():
    username = input('Введите имя пользователя:')

    if User.query.filter(User.username == username).count():
        print('Пользователь с таким логином существует')
        sys.exit(0)

    password1 = getpass('Введите пароль:')
    password2 = getpass('Повторите пароль:')

    if not password1==password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print (f'Создан пользователь с id-{new_user.id}')