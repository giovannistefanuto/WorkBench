import sys
from bs4 import BeautifulSoup
import requests

# Reconfigure standard output to use UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Fetch the HTML content
html_text = requests.get('https://www.immobiliare.it/affitto-case/padova/').text


# Print the HTML content
#print(html_text)


soup = BeautifulSoup(html_text, 'lxml')
#print(soup.prettify())

# Salva il contenuto HTML in un file
with open('pagina_immobiliare.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
    #print('File salvato con success')

#annunci = soup.find_all('div', class_='in-listingCard')   #ottengo tutto l'annuncio, per ogni annuncio
annunci = soup.find_all('div', class_='in-listingCard')
#print(annuncio)
for annuncio in annunci:
    prezzo = annuncio.find('div', class_='in-listingCardPrice').text.replace(' ', '').replace('/mese', '').replace('€', '')
    if prezzo < '10.200':
        nome = annuncio.find('a', class_='in-listingCardTitle').text
        url_description = annuncio.find('a', class_='in-listingCardTitle')['href']
        # Fetching HTML content from the URL
        html_text_description = requests.get(url_description).text

        # Creating a BeautifulSoup object and parsing with 'lxml'
        d_soup = BeautifulSoup(html_text_description, 'lxml')

        # Finding the div with class 'in-readAll'
        description_div = d_soup.find('div', class_='in-readAll')
        description = description_div.get_text(separator=" ", strip=True)
        print(f'''
        Prezzo: {prezzo}
        Nome: {nome}
        Descrizione: {description}
        ''')

# Se ci sono classi a dentro altre classi
# nome = annuncio.find('a', class_='in-listingCardTitle').span.text


# Questo programma estrae gli annunci di affitto da una pagina web di immobiliare.it, 
# estraendo informazioni come prezzo, nome e descrizione dell'annuncio.