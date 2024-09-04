import os
from datetime import datetime
from PyPDF2 import PdfMerger

def merge_pdfs(source_folder, output_folder):
    # Verifica se la cartella di output esiste, altrimenti la crea
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Ottieni la lista dei file PDF nella cartella di origine
    pdf_files = [f for f in os.listdir(source_folder) if f.endswith('.pdf')]
    
    # Ordina i file in ordine alfabetico
    pdf_files.sort()

    # Crea un oggetto PdfMerger
    merger = PdfMerger()

    # Unisci i file PDF
    for pdf in pdf_files:
        merger.append(os.path.join(source_folder, pdf))

    # Ottieni la data e l'ora corrente nel formato desiderato
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
    
    # Crea il nome del file di output con data e ora
    output_filename = f"pdfUNITI_{timestamp}.pdf"
    
    # Salva il file PDF unito
    output_path = os.path.join(output_folder, output_filename)
    merger.write(output_path)
    merger.close()
    print(f"PDF unito salvato come: {output_path}")

# Specifica la cartella di origine e di destinazione con percorsi assoluti
source_folder = r'C:/Users/Utente/Desktop/WorkBench/Merge PDFs/source'
output_folder = r'C:/Users/Utente/Desktop/WorkBench/Merge PDFs/merged'
# Esegui la funzione per unire i PDF
merge_pdfs(source_folder, output_folder)
