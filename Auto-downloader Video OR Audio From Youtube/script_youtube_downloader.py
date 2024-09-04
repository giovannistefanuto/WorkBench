import os
import yt_dlp as youtube_dl

# Definisci le cartelle di output per MP3 e MP4
MP3_OUTPUT_PATH = r'C:/Users/Utente/Desktop/WorkBench/Auto-downloader Video OR Audio From Youtube/mp3'
MP4_OUTPUT_PATH = r'C:/Users/Utente/Desktop/WorkBench/Auto-downloader Video OR Audio From Youtube/mp4'

# File di testo contenenti gli URL
MP3_URL_FILE = r'C:/Users/Utente/Desktop/WorkBench/Auto-downloader Video OR Audio From Youtube/elenco url per mp3.txt'
MP4_URL_FILE = r'C:/Users/Utente/Desktop/WorkBench/Auto-downloader Video OR Audio From Youtube/elenco url per mp4.txt'

def download_video(url, audio_only):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(MP3_OUTPUT_PATH if audio_only else MP4_OUTPUT_PATH, '%(title)s.%(ext)s'),
            'retries': 10,  # Numero di tentativi di download in caso di errore
            'sleep_interval': 5,  # Secondi tra i tentativi
            'max_sleep_interval': 10,  # Tempo massimo di attesa tra i tentativi
            # 'ratelimit': '1M',  # Rimuovi o commenta questa linea se causa problemi
        }

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio'

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Download completato con successo in {'MP3' if audio_only else 'MP4'}.")

    except Exception as e:
        print(f"Si è verificato un errore: {e}")

def download_from_file(file_path, audio_only):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()

        urls = [url.strip() for url in urls if url.strip()]  # Rimuove righe vuote e spazi

        if not urls:
            print(f"Nessun URL trovato nel file {file_path}.")
            return

        for url in urls:
            download_video(url, audio_only)

    except Exception as e:
        print(f"Si è verificato un errore nella lettura del file {file_path}: {e}")

if __name__ == "__main__":
    # Scarica video dai file di testo
    download_from_file(MP3_URL_FILE, audio_only=True)
    download_from_file(MP4_URL_FILE, audio_only=False)

    while True:
        # Chiedi all'utente se vuole scaricare altro
        cont = input("Vuoi scaricare altro? (SI/NO): ").strip().lower()
        if cont == 'si':
            url = input("Inserisci l'URL del video YouTube: ")
            format_type = input("Vuoi scaricare in formato MP3 o MP4? ").lower()

            if format_type not in ['mp3', 'mp4']:
                print("Formato non valido. Per favore, scegli 'mp3' o 'mp4'.")
            else:
                audio_only = format_type == 'mp3'
                download_video(url, audio_only)
        elif cont == 'no':
            print("Operazione completata.")
            break
        else:
            print("Risposta non valida. Per favore, rispondi con 'SI' o 'NO'.")
