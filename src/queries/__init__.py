import sqlite3
from typing import Tuple
from config import settings
from dto import UserInDB, User


def get_database_connection():
    connection = sqlite3.connect(f'{settings.DATABASE_PATH}')
    cursor = connection.cursor()
    return connection, cursor


def create_user(username, first_name, last_name, fullname, email, hashed_password):
    connection, cursor = get_database_connection()

    cursor.execute('INSERT INTO users VALUES'
                   ' (?,?,?,?,?,?,?,?)',
                   (1, username, first_name, last_name, fullname, email, hashed_password, False))
    connection.commit()
    connection.close()


def get_user_info(username) -> User:
    connection, cursor = get_database_connection()

    cursor.execute('SELECT username, email, fullname, disabled from users WHERE username = ?',
                   (username,))
    response = cursor.fetchall()

    user = User(
        username=response[0][0],
        email=response[0][1],
        full_name=response[0][2],
        disabled=response[0][3]
    )

    connection.close()
    return user


def get_user_hashed_password(username) -> UserInDB:
    connection, cursor = get_database_connection()

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

