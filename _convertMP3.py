import os
import json
from tqdm import tqdm
from pydub import AudioSegment
import threading

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    print(config)  
    return config

def convert_to_mp3(mp4_file, mp3_path):
    try:
        video = AudioSegment.from_file(mp4_file)
        mp3_file = os.path.join(mp3_path, os.path.splitext(os.path.basename(mp4_file))[0] + '.mp3')
        video.export(mp3_file, format='mp3')
        print(f"Arquivo convertido: {mp3_file}")
    except Exception as e:
        print(f"Erro ao converter {mp4_file}: {e}")

def convert_files_in_directory(downloads_path, output_mp3_path, num_threads):
    mp4_files = [f for f in os.listdir(downloads_path) if f.endswith('.mp4')]
    
    if not os.path.exists(output_mp3_path):
        os.makedirs(output_mp3_path)
    
    with tqdm(total=len(mp4_files), desc="Convertendo MP4 para MP3") as pbar:
        def worker(file):
            convert_to_mp3(os.path.join(downloads_path, file), output_mp3_path)
            pbar.update(1)
        
        threads = []
        for file in mp4_files:
            if len(threads) >= num_threads:
                for t in threads:
                    t.join()
                threads = []

            thread = threading.Thread(target=worker, args=(file,))
            threads.append(thread)
            thread.start()

        for t in threads:
            t.join()

def main():
    config = load_config()

    
    print(config)

    downloads_path = config["outputPath"]  
    output_mp3_path = config["outputMp3"]  
    num_threads = config["numThreads"]  

    convert_files_in_directory(downloads_path, output_mp3_path, num_threads)

if __name__ == "__main__":
    main()
