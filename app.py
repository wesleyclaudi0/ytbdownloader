# app.py
import os
from flask import Flask, render_template, request, redirect, send_from_directory, flash
import threading
import yt_dlp

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necessário para flash messages

DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Função genérica de download
def baixar_video_audio(url, tipo):
    try:
        if tipo == 'video':
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'format': 'best[ext=mp4]',
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'format': 'bestaudio[ext=m4a]',
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print("Erro:", e)

# Página inicial
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        tipo = request.form.get("tipo")
        if not url:
            flash("Por favor, cole o link do vídeo.")
            return redirect("/")

        # Baixar em uma thread separada para não travar o servidor
        threading.Thread(target=baixar_video_audio, args=(url, tipo)).start()
        flash(f"Download iniciado para {tipo}! Verifique a pasta Downloads.")
        return redirect("/")

    return render_template("index.html")

# Permite baixar arquivos manualmente (opcional)
@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
