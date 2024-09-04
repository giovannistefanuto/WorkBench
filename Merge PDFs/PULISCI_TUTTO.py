import os

def clean_folder(folder_path):
    # Verifica se la cartella esiste
    if os.path.exists(folder_path):
        # Ottieni la lista dei file nella cartella
        files = os.listdir(folder_path)
        
        # Cancella ogni file nella cartella
        for f in files:
            file_path = os.path.join(folder_path, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"File eliminato: {file_path}")
            except Exception as e:
                print(f"Errore nell'eliminazione di {file_path}: {e}")
    else:
        print(f"La cartella {folder_path} non esiste.")

# Specifica i percorsi delle cartelle da pulire
source_folder = r'C:\Users\Utente\Desktop\WorkBench\Merge PDFs\source'
output_folder = r'C:\Users\Utente\Desktop\WorkBench\Merge PDFs\merged'

# Pulisce entrambe le cartelle
clean_folder(source_folder)
clean_folder(output_folder)
