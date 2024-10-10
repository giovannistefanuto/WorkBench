import os
import pandas as pd

def converti_csv_in_excel(cartella):
    # Scorri ogni file nella cartella specificata
    for file_name in os.listdir(cartella):
        # Verifica se il file ha estensione .csv
        if file_name.endswith('.csv'):
            # Crea il percorso completo del file CSV
            file_csv = os.path.join(cartella, file_name)
            
            # Leggi il file CSV utilizzando pandas
            try:
                df = pd.read_csv(file_csv)
                
                # Crea il nome del file Excel cambiando l'estensione
                file_excel = file_csv.replace('.csv', '.xlsx')
                
                # Scrivi il DataFrame in un file Excel
                df.to_excel(file_excel, index=False)

                print(f"Convertito {file_csv} in {file_excel}")
            
            except Exception as e:
                print(f"Errore durante la conversione di {file_csv}: {e}")

# Specifica il percorso della cartella che contiene i file CSV
cartella = r'C:\Users\Utente\Desktop\WorkBench\Scraping from Immobiliare.it'

# Esegui la conversione di tutti i file CSV in Excel
converti_csv_in_excel(cartella)
