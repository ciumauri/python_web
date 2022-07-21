from sqlalchemy import Table, create_engine

from flask_sqlalchemy import SQLAlchemy

import sqlite3

# import configparser

conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()


# config = configparser.ConfigParser()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


Users_tbl = Table('users', Users.metadata)


# function to create table using Users class
def create_users_table():
    Users.metadata.create_all(engine)


create_users_table()

# import pandas as pd
# c = conn.cursor()
# df = pd.read_sql('select * from users', conn)
# df
