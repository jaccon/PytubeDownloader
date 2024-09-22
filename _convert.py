import os
import csv
from yt_dlp import YoutubeDL
from moviepy.editor import AudioFileClip
from tqdm import tqdm

# Definir a pasta de saída
OUTPUT_FOLDER = 'output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Função para baixar e salvar o vídeo/áudio
def download_video(url, format_type):
    ydl_opts = {}
    if format_type == 'mp3':
        # Baixar o áudio apenas e convertê-lo
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{OUTPUT_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format_type == 'mp4':
        # Baixar o vídeo no formato MP4
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{OUTPUT_FOLDER}/%(title)s.%(ext)s',
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download completo: {url}")
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

# Função para processar o arquivo CSV
def process_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                url, format_type = row
                print(f"Baixando {url} no formato {format_type}")
                download_video(url.strip(), format_type.strip())

# Caminho do arquivo CSV
csv_file_path = 'data/videos.csv'

# Executar o processo de download
if __name__ == '__main__':
    process_csv(csv_file_path)
