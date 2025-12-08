import sqlite3
from typing import Tuple
from config import settings
from dto import UserInDB


def create_user(username, first_name, last_name, fullname, email, hashed_password):
    connection = sqlite3.connect(f'{settings.DATABASE_PATH}')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO users VALUES'
                   ' (?,?,?,?,?,?,?,?)',
                   (1, username, first_name, last_name, fullname, email, hashed_password, False))
    connection.commit()
    connection.close()


def get_user_info(username) -> Tuple:
    connection = sqlite3.connect(f'{settings.DATABASE_PATH}')
    cursor = connection.cursor()

    cursor.execute('SELECT id, username, firstname, lastname, email, disabled from users WHERE username = ?',
                   (username,))
    response = cursor.fetchall()

    connection.close()
    return response[0]


def get_user_hashed_password(username):
    connection = sqlite3.connect(f'{settings.DATABASE_PATH}')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?',
                   (username,))
    response = cursor.fetchall()

    connection.close()

    user = UserInDB(
        username=response[0][1],
        email=response[0][5],
        full_name=response[0][4],
        disabled=response[0][7],
        hashed_password=response[0][6]
    )

    return user

