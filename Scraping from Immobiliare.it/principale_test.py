import sqlite3
import csv
import os

# Nome del file CSV generato dallo scraping
csv_file = 'annunci_padova_puliti.csv'

# Nome del database SQLite
db_file = 'annunci.db'

# Funzione per creare una nuova tabella e inserire i dati del CSV nel database
def crea_db_e_inserisci_dati(csv_file, db_file):
    # Se il database esiste già, cancellalo
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS annunci (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prezzo REAL,
        nome TEXT,
        descrizione TEXT,
        link TEXT,
        tipologia TEXT,
        contratto TEXT,
        piano TEXT,
        piani_edificio TEXT,
        ascensore TEXT,
        superficie REAL,
        locali TEXT,
        camere_da_letto TEXT,
        bagni TEXT,
        arredato TEXT,
        terrazzo TEXT,
        box_posti_auto TEXT,
        riscaldamento TEXT,
        climatizzazione TEXT,
        spese_condominio REAL,
        cauzione REAL
    )''')

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            prezzo = float(row[0]) if row[0] else None
            superficie = float(row[9]) if row[9] else None
            spese_condominio = float(row[-2]) if row[-2] else None
            cauzione = float(row[-1]) if row[-1] else None

            cursor.execute('''INSERT INTO annunci (
                prezzo, nome, descrizione, link, tipologia, contratto, piano, piani_edificio, ascensore, superficie,
                locali, camere_da_letto, bagni, arredato, terrazzo, box_posti_auto, riscaldamento, climatizzazione,
                spese_condominio, cauzione
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (prezzo, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], superficie, row[10], row[11], 
            row[12], row[13], row[14], row[15], row[16], row[17], spese_condominio, cauzione))

    conn.commit()
    conn.close()

# Funzione per visualizzare i report
def genera_report(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # A: I primi 10 appartamenti con prezzo minore che non sia 0
    cursor.execute('''
        SELECT id, prezzo, nome, link 
        FROM annunci 
        WHERE prezzo > 0 
        ORDER BY prezzo ASC 
        LIMIT 10
    ''')
    risultati = cursor.fetchall()
    print("Primi 10 appartamenti con prezzo minore (escludendo 0):")
    for annuncio in risultati:
        print(f"ID: {annuncio[0]}, Prezzo: {annuncio[1]} €, Nome: {annuncio[2]}, Link: {annuncio[3]}")

    # B: I primi 10 appartamenti dove prezzo + spese condominiali
    cursor.execute('''
        SELECT id, prezzo, spese_condominio, nome, link 
        FROM annunci 
        WHERE prezzo IS NOT NULL AND spese_condominio IS NOT NULL 
        ORDER BY (prezzo + spese_condominio) ASC 
        LIMIT 10
    ''')
    risultati_categoria = cursor.fetchall()
    print("\nPrimi 10 appartamenti con prezzo + spese condominiali:")
    for annuncio in risultati_categoria:
        totale = annuncio[1] + annuncio[2]
        print(f"ID: {annuncio[0]}, Prezzo: {annuncio[1]} €, Spese Condominiali: {annuncio[2]} €, Totale: {totale} €, Nome: {annuncio[3]}, Link: {annuncio[4]}")

    conn.close()

def conta_annunci(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM annunci")
    count = cursor.fetchone()[0]
    
    print(f"Numero totale di annunci nel database: {count}")
    
    conn.close()

# Esegui il programma
crea_db_e_inserisci_dati(csv_file, db_file)
conta_annunci(db_file)
genera_report(db_file)


# Note:
# Questo programma crea un database SQLite da un file CSV di annunci immobiliari,
# inserisce i dati nel database e genera report sui primi 10 appartamenti con il prezzo minore e il totale del prezzo
# più le spese condominiali, oltre a contare il numero totale di annunci nel database.
