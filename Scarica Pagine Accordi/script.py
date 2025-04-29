import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from reportlab.pdfgen import canvas

# Funzione per fare uno screenshot della pagina e salvarlo
def capture_screenshot(url, output_folder):
    # Configura il browser (usiamo Chrome in modalità headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # modalità senza interfaccia grafica
    chrome_options.add_argument("--window-size=1920x1080")  # Risoluzione per lo screenshot
    
    # Crea l'oggetto Service con il percorso di chromedriver
    service = Service('path/to/chromedriver')  # Sostituisci con il percorso corretto
    
    # Avvia il browser con il servizio e le opzioni
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    
    # Cattura lo screenshot
    screenshot_path = os.path.join(output_folder, f"{url.split('//')[1].replace('/', '_')}.png")
    driver.save_screenshot(screenshot_path)
    driver.quit()
    
    return screenshot_path

# Funzione per creare un PDF a partire dallo screenshot
def create_pdf_from_image(image_path, output_pdf):
    # Usa ReportLab per creare il PDF
    c = canvas.Canvas(output_pdf)
    c.drawImage(image_path, 0, 0)
    c.save()

# Funzione principale
def main():
    # URL del sito che vuoi catturare
    url = "https://www.accordiespartiti.it/accordi/italiani/dalla-lucio/attenti-al-lupo/"
    output_folder = "output"  # La cartella dove salvare il PDF e lo screenshot
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Cattura lo screenshot della pagina web
    screenshot_path = capture_screenshot(url, output_folder)
    
    # Crea il PDF con il nome del sito
    pdf_name = os.path.join(output_folder, f"{url.split('//')[1].replace('/', '_')}.pdf")
    create_pdf_from_image(screenshot_path, pdf_name)
    
    print(f"PDF salvato in {pdf_name}")

if __name__ == "__main__":
    main()
