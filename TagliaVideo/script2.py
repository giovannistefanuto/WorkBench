from moviepy.video.io.VideoFileClip import VideoFileClip

# Funzione per tagliare il video
def taglia_video(input_path, output_path, start_time, end_time):
    # Carica il video
    clip = VideoFileClip(input_path)
    
    # Taglia il video tra start_time e end_time
    clipped = clip.subclip(start_time, end_time)
    
    # Salva il video tagliato
    clipped.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Parametri
input_video = "20241006_194104.mov"  # Percorso del video di input
output_video = "output_video.mov"  # Percorso del video di output
start_secondo = 30  # Secondo di inizio
end_secondo = 39  # Secondo di fine

# Esegui la funzione
taglia_video(input_video, output_video, start_secondo, end_secondo)
