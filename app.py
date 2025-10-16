import os
import re
from flask import Flask, render_template, request, redirect, jsonify, flash
import threading
import yt_dlp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Pasta de download
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Variável global para progresso
progresso_atual = {"percent": 0, "status": ""}

# Hook de progresso
def hook_progresso(d):
    global progresso_atual
    if d['status'] == 'downloading':
        # Remove códigos ANSI antes de converter
        percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str'])
        progresso_atual['percent'] = float(percent_str.replace('%',''))
        progresso_atual['status'] = f"Baixando: {percent_str} ({d['_speed_str']})"
    elif d['status'] == 'finished':
        progresso_atual['percent'] = 100
        progresso_atual['status'] = "✅ Download concluído!"

# Função de download
def baixar_video_audio(url, tipo):
    global progresso_atual
    progresso_atual = {"percent": 0, "status": "Iniciando..."}
    try:
        if tipo == 'video':
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'format': 'best[ext=mp4]',
                'progress_hooks': [hook_progresso]
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'format': 'bestaudio[ext=m4a]',
                'progress_hooks': [hook_progresso]
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        progresso_atual['status'] = f"Erro: {e}"
        progresso_atual['percent'] = 0

# Página principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        tipo = request.form.get("tipo")
        if not url:
            flash("Por favor, cole o link do vídeo.")
            return redirect("/")

        # Inicia download em thread separada
        threading.Thread(target=baixar_video_audio, args=(url, tipo)).start()
        flash(f"Download iniciado para {tipo}! Arquivos serão salvos em: {DOWNLOAD_FOLDER}")
        return redirect("/")

    return render_template("index.html", pasta_downloads=DOWNLOAD_FOLDER)

# Rota para progresso (JSON)
@app.route("/progresso")
def progresso():
    return jsonify(progresso_atual)

if __name__ == "__main__":
    app.run(debug=True)
