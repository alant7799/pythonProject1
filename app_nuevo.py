import os
from flask import Flask
from flask import render_template, request, redirect, send_from_directory, url_for
from pytube import YouTube
import sqlite3

app = Flask(__name__)

CARPETA = os.path.join('uploads')  # al path del proyecto le adjunto ‘upload’
app.config['CARPETA'] = CARPETA

@app.route('/')
def index():
    sql = "SELECT * FROM `main`;"
    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()
    cursor.execute(sql)

    archivos = cursor.fetchall()
    print(archivos)

    conn.commit()

    return render_template('paginas/index.html', archivos=archivos)