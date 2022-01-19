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
    return render_template('paginas/index.html')


@app.route("/store", methods=['POST'])
def storage():
    _link = request.form['txtLink']
    _audio = request.form['audio']

    video = YouTube(str(_link))  # for pytube this is an object
    print(_link)
    sql = "INSERT INTO `main` (`ID`,`FOTO`,`NOMBRE`,`URL`,`TIPO`) VALUES (NULL, ?, ?, ?, ?);"
    datos = (video.thumbnail_url, video.title, _link, _audio)

    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect("/")


@app.route("/destroy/<int:id>")
def destroy(id):
    sql = "DELETE FROM `main` WHERE ID=?;"
    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()
    id = str(id)
    cursor.execute(sql, id)
    try:
        os.remove(os.path.join(app.config['CARPETA'], str(id) + ".mp4"))
    except FileNotFoundError:
        conn.commit()
        return redirect("/")
    conn.commit()
    return redirect("/")


@app.route("/edit/<int:id>")
def edit(id):
    sql = "SELECT * FROM `main` WHERE ID=?;"
    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()
    id = str(id)
    cursor.execute(sql, id)
    conn.commit()
    archivos = cursor.fetchall()
    return render_template("paginas/edit.html", archivos=archivos)


@app.route('/descargar/<int:id>', methods=['GET', 'POST'])
def descargar(id):
    sql = "SELECT * FROM `main` WHERE ID=?;"
    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()
    id = str(id)
    cursor.execute(sql, id)
    conn.commit()
    archivos = cursor.fetchall()
    return render_template("paginas/descargar.html", archivos=archivos)


def borrar_datos():
    sql = "DELETE FROM `main`;"
    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template("paginas/index.html")


@app.route("/return_file/<int:id>")
def return_files(id):
    sql = "SELECT * FROM `main` WHERE `ID`=?;"
    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()
    id = str(id)
    cursor.execute(sql, id)
    lista_videos = cursor.fetchall()

    print(lista_videos)
    video = lista_videos[0]

    id_video = video[0]
    # foto_video = video[1]
    # nombre_video = video[2]
    url_video = video[3]
    tipo_video = video[4]

    objeto_video = YouTube(url_video)

    if tipo_video == "Mp4":
        path = objeto_video.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download("uploads", filename=str(id_video) + ".mp4")
    else:
        path = (objeto_video.streams.filter(only_audio=True)[0]).download("uploads", filename=str(id_video) + ".mp4")

    print(path)

    return send_from_directory("uploads", path=str(id_video) + ".mp4", as_attachment=True), borrar_datos()


@app.route("/index")
def inicio():
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
