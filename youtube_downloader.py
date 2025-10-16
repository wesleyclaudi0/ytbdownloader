import os
import tkinter as tk
from tkinter import messagebox
import threading
import yt_dlp

# Função principal de download de vídeo
def baixar_video():
    baixar('video')

# Função principal de download de áudio
def baixar_audio():
    baixar('audio')

# Função genérica de download
def baixar(tipo):
    url = entry_url.get()
    if not url or url == "Cole o link do vídeo aqui...":
        messagebox.showerror("Erro", "Por favor, cole o link do vídeo.")
        return

    btn_video.config(state=tk.DISABLED)
    btn_audio.config(state=tk.DISABLED)
    label_status.config(text="⏳ Baixando...")

    def processo_download():
        try:
            pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

            if tipo == 'video':
                # Baixa vídeo + áudio mesclado (MP4)
                ydl_opts = {
                    'outtmpl': os.path.join(pasta_downloads, '%(title)s.%(ext)s'),
                    'format': 'best[ext=mp4]',
                    'progress_hooks': [hook_progresso]
                }
            else:  # audio
                # Baixa áudio em M4A sem converter
                ydl_opts = {
                    'outtmpl': os.path.join(pasta_downloads, '%(title)s.%(ext)s'),
                    'format': 'bestaudio[ext=m4a]',  # força M4A
                    'progress_hooks': [hook_progresso]
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            tipo_texto = "Vídeo" if tipo == 'video' else "Áudio"
            label_status.config(text=f"✅ {tipo_texto} concluído! Salvo em: {pasta_downloads}")
            messagebox.showinfo("Concluído", f"{tipo_texto} salvo em:\n{pasta_downloads}")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
        finally:
            btn_video.config(state=tk.NORMAL)
            btn_audio.config(state=tk.NORMAL)

    threading.Thread(target=processo_download).start()

# Atualiza status de progresso
def hook_progresso(d):
    if d['status'] == 'downloading':
        label_status.config(text=f"Baixando: {d['_percent_str']} ({d['_speed_str']})")
    elif d['status'] == 'finished':
        label_status.config(text="✅ Download concluído!")

# Cria janela
root = tk.Tk()
root.title("🎬 YouTube Downloader")
root.geometry("500x300")
root.resizable(False, False)
root.configure(bg="#2b2b40")

# Título
titulo = tk.Label(root, text="YouTube Downloader", bg="#2b2b40", fg="white", font=("Segoe UI", 18, "bold"))
titulo.pack(pady=10)

# Campo de entrada com placeholder
entry_url = tk.Entry(root, width=55, font=("Segoe UI", 10), fg="#888888")
entry_url.pack(pady=10)
entry_url.insert(0, "Cole o link do vídeo aqui...")  # invite message

# Funções para placeholder
def on_entry_click(event):
    if entry_url.get() == "Cole o link do vídeo aqui...":
        entry_url.delete(0, "end")
        entry_url.config(fg="black")

def on_focusout(event):
    if entry_url.get() == "":
        entry_url.insert(0, "Cole o link do vídeo aqui...")
        entry_url.config(fg="#888888")

entry_url.bind("<FocusIn>", on_entry_click)
entry_url.bind("<FocusOut>", on_focusout)

# Botões de download
btn_video = tk.Button(root, text="⬇️ Baixar vídeo", bg="#ff4747", fg="white",
                      font=("Segoe UI", 11, "bold"), width=25, command=baixar_video)
btn_video.pack(pady=5)

btn_audio = tk.Button(root, text="🎵 Baixar áudio (M4A)", bg="#4caf50", fg="white",
                      font=("Segoe UI", 11, "bold"), width=25, command=baixar_audio)
btn_audio.pack(pady=5)

# Status
label_status = tk.Label(root, text="", bg="#2b2b40", fg="#cfcfcf", font=("Segoe UI", 10))
label_status.pack(pady=10)

root.mainloop()