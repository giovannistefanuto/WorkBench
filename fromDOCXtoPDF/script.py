import os
from docx2pdf import convert

# Cartella di origine con i file .docx
source_folder = r"C:\Users\Utente\Desktop\WorkBench\fromDOCXtoPDF\SOURCE"
# Cartella di destinazione per i file PDF
pdf_folder = r"C:\Users\Utente\Desktop\WorkBench\fromDOCXtoPDF\PDF"

# Crea la cartella di destinazione se non esiste
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# Scorri tutti i file nella cartella source
for filename in os.listdir(source_folder):
    if filename.endswith(".docx"):
        # Percorso completo del file .docx
        docx_path = os.path.join(source_folder, filename)
        # Percorso completo per salvare il file PDF
        pdf_path = os.path.join(pdf_folder, filename.replace(".docx", ".pdf"))
        
        # Converti il file .docx in PDF
        convert(docx_path, pdf_path)

print("Conversione completata!")
