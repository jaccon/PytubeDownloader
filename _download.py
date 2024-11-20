import os
import json
import yt_dlp as ydl
import csv
from pathlib import Path
from tqdm import tqdm

def loadConfig(configFile):
    with open(configFile, 'r') as file:
        return json.load(file)

def logDownloadProgress(d, logFile):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)
        percent = (downloaded / total) * 100
        print(f"Download: {percent:.2f}%")
    elif d['status'] == 'finished':
        videoName = d.get('filename')
        size = d.get('total_bytes')
        quality = d.get('format')
        logMessage = f"Baixado: {videoName} | Tamanho: {size / (1024*1024):.2f} MB | Qualidade: {quality}\n"
        print(f"Download concluído: {videoName}")
        
        with open(logFile, 'a') as log:
            log.write(logMessage)

def downloadVideo(url, outputPath='./', cookiesPath='cookies.txt', useProxy=False, logFile='download.log'):
    try:
        print(f"Iniciando o download do vídeo: {url}")

        options = {
            'outtmpl': os.path.join(outputPath, '%(title)s.%(ext)s'),
            'format': 'best',
            'noplaylist': True,
            'quiet': False,
            'age_limit': 18,
            'cookies': cookiesPath,
            'progress_hooks': [lambda d: logDownloadProgress(d, logFile)]
        }

        if useProxy:
            options['proxy'] = 'http://seu_proxy_aqui:porta'

        with ydl.YoutubeDL(options) as ydlInstance:
            ydlInstance.download([url])
        print(f"Vídeo {url} baixado com sucesso!")

    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

def readUrlsFromCsv(csvFile):
    urls = []
    with open(csvFile, 'r') as file:
        csvReader = csv.reader(file)
        for row in csvReader:
            if row:  # Ignorar linhas vazias
                urls.append(row[0])  # Supõe que a URL está na primeira coluna
    return urls

def main():
    configFilePath = Path(__file__).parent / 'config.json'
    config = loadConfig(configFilePath)

    outputPath = config.get('outputPath', './downloads')
    cookiesPath = config.get('cookiesPath', 'cookies.txt')
    useProxy = config.get('useProxy', False)

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    logFile = 'download.log'

    # Lê as URLs do arquivo CSV
    videoUrls = readUrlsFromCsv('data/data.csv')

    for url in tqdm(videoUrls, desc="Baixando vídeos", unit="vídeo"):
        downloadVideo(url, outputPath, cookiesPath, useProxy, logFile)

if __name__ == "__main__":
    main()
