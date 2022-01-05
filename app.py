import os
from flask import Flask
from flask import render_template, request, redirect, send_from_directory
from pytube import YouTube
import sqlite3

app = Flask(__name__)

CARPETA = os.path.join('uploads')  # al path del proyecto le adjunto ‘upload’
app.config['CARPETA'] = CARPETA


# guardar en la configuracion de python la carpeta de las fotos


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


@app.route('/create')
def create():
    return render_template('paginas/create.html')


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


@app.route("/update", methods=['POST'])
def update():
    _nombre = request.form['txtNombre']  # toma los datos txtNombre del form
    _tipo = request.form['audio']
    id = request.form['txtId']

    conn = sqlite3.connect("MiBaseDeDatos.sqlite")
    cursor = conn.cursor()

    sql = "UPDATE `main` SET `NOMBRE`=? ,`TIPO`=? WHERE ID=?;"
    datos = (_nombre, _tipo, id)  # crea la sentencia sql

    cursor.execute(sql, datos)  # ejecuta la sentencia sql
    conn.commit()
    return redirect("/")  # y renderiza indexViejo.html


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


# @app.route("/return_file/")
# def return_files():
#   return send_from_directory("C:/youtube/uploads/",path="300  This is where we hold them.mp4",as_attachment=True)


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

    return send_from_directory("uploads", path=str(id_video) + ".mp4", as_attachment=True)


@app.route("/index")
def inicio():
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
