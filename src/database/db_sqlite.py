# src/database/db_sqlite.py
import sqlite3
from flask import g

DATABASE = 'memoramaDB.db'  # Ruta de tu base de datos SQLite

def get_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Devuelve filas como diccionarios
    return g.db

def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
