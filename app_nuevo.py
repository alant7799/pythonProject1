import os
from flask import Flask
from flask import render_template, request, redirect, send_from_directory, url_for
from pytube import YouTube

app = Flask(__name__)

CARPETA = os.path.join('uploads')  # al path del proyecto le adjunto ‘upload’
app.config['CARPETA'] = CARPETA


@app.route('/')
def index():
    return render_template('paginas/index.html')


@app.route('/descargar', methods=['GET', 'POST'])
def descargar():

    _link = request.form['txtLink'] # Le pido al form los datos ingresados por cliente
    _audio = request.form['audio']

    objeto_video = YouTube(str(_link))  # Para pytube esto es un objeto

    path = objeto_video.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().download("uploads", filename=str(id_video) + ".mp4")

    if _audio == "Mp4":
        path = objeto_video.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download("uploads", filename=str(objeto_video.title) + ".mp4")
    else:
        path = (objeto_video.streams.filter(only_audio=True)[0]).download("uploads", filename=str(objeto_video.title)+
                ".mp4")

    print(path)
    return send_from_directory("uploads", path=str(objeto_video.title) + ".mp4", as_attachment=True)


@app.route("/index")
def inicio():
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



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

