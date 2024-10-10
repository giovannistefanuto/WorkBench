import requests
from bs4 import BeautifulSoup
import csv

# Funzione per estrarre le informazioni da una singola pagina
def estrai_annunci(url, writer, caratteristiche_keys):
    # Richiedi il contenuto della pagina
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # Trova tutti gli annunci
    annunci = soup.find_all('div', class_='in-listingCard')

    for annuncio in annunci:
        try:
            # Estrai prezzo, nome e link alla descrizione dell'annuncio
            prezzo = annuncio.find('div', class_='in-listingCardPrice').text.strip().replace('€', '').replace(' ', '').replace('/mese', '')
            nome = annuncio.find('a', class_='in-listingCardTitle').text.strip()
            url_description = annuncio.find('a', class_='in-listingCardTitle')['href']

            # Richiedi la descrizione dettagliata dell'annuncio
            html_text_description = requests.get(url_description).text
            d_soup = BeautifulSoup(html_text_description, 'lxml')
            description_div = d_soup.find('div', class_='in-readAll')
            description = description_div.get_text(separator=" ", strip=True) if description_div else "Descrizione non disponibile"

            # Estrai le caratteristiche della proprietà
            caratteristiche_div = d_soup.find('div', {'data-tracking-key': 'primary-data'})
            caratteristiche = {key: "" for key in caratteristiche_keys}  # Inizializza un dizionario vuoto per le caratteristiche

            if caratteristiche_div:
                caratteristiche_items = caratteristiche_div.find_all('div', class_='re-featuresItem')
                for item in caratteristiche_items:
                    titolo = item.find('dt', class_='re-featuresItem__title').text.strip()
                    valore = item.find('dd', class_='re-featuresItem__description').text.strip()
                    if titolo in caratteristiche:
                        caratteristiche[titolo] = valore  # Aggiungi il valore alla chiave corretta

            # Estrai le informazioni sulle spese condominiali e la cauzione
            costi_div = d_soup.find('div', {'data-tracking-key': 'costs'})
            spese_condominio = ""
            cauzione = ""

            if costi_div:
                costi_items = costi_div.find_all('div', class_='re-featuresItem')
                for item in costi_items:
                    titolo = item.find('dt', class_='re-featuresItem__title').text.strip()
                    valore = item.find('dd', class_='re-featuresItem__description').text.strip()

                    if titolo == "Spese condominio":
                        spese_condominio = valore.replace('€', '').replace('/mese', '').strip()
                    elif titolo == "Cauzione":
                        cauzione = valore.replace('€', '').strip()

            # Crea la riga da scrivere nel CSV
            row = [prezzo, nome, description, url_description] + [caratteristiche[key] for key in caratteristiche_keys] + [spese_condominio, cauzione]
            writer.writerow(row)

        except AttributeError as e:
            # Gestisce eventuali errori di attribuzione in caso di mancanza di qualche campo
            print(f"Errore nell'estrazione di un annuncio: {e}")
    
    # Restituisce l'URL della pagina successiva
    return estrai_pagina_successiva(soup)

# Funzione per estrarre l'URL della pagina successiva
def estrai_pagina_successiva(soup):
    # Cerca il div che contiene il pulsante "Successiva"
    next_page = soup.find('div', {'data-cy': 'pagination-next'}).find('a')
    
    # Controlla se esiste un pulsante "Successiva" e restituisce l'href se disponibile
    if next_page and 'href' in next_page.attrs:
        next_page_url = next_page['href']
        return next_page_url
    else:
        return None

# Funzione principale per eseguire lo scraping su più pagine e salvare i risultati in un CSV
def scraping_immobiliare(base_url, file_name):
    # Definisci le chiavi delle caratteristiche che vuoi estrarre
    caratteristiche_keys = ['Tipologia', 'Contratto', 'Piano', 'Piani edificio', 'Ascensore', 'Superficie', 'Locali', 'Camere da letto', 'Bagni', 'Arredato', 'Terrazzo', 'Box, posti auto', 'Riscaldamento', 'Climatizzazione']

    # Apri il file CSV in modalità scrittura
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Scrivi l'intestazione del CSV (colonne)
        header = ['Prezzo', 'Nome', 'Descrizione', 'Link'] + caratteristiche_keys + ['Spese condominio', 'Cauzione']
        writer.writerow(header)

        url = base_url
        while url:
            print(f"Scraping pagina: {url}")
            url = estrai_annunci(url, writer, caratteristiche_keys)

# Esegui lo scraping e salva i dati in un file CSV
base_url = 'https://www.immobiliare.it/affitto-case/verona/'
file_name = 'annunci_padova.csv'
scraping_immobiliare(base_url, file_name)

print(f"I dati degli annunci sono stati salvati in {file_name}")
