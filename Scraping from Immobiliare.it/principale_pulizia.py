import csv
import re  # Regex per pulizia dei dati

def pulisci_dati(file_input, file_output):
    # Apri il file CSV originale e quello di output
    with open(file_input, mode='r', encoding='utf-8') as infile, \
         open(file_output, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Leggi l'intestazione
        header = next(reader)
        writer.writerow(header)  # Scrivi l'intestazione nel file di output

        # Trova l'indice delle colonne 'Prezzo', 'Superficie', 'Cauzione' e 'Spese condominiali'
        indice_prezzo = header.index('Prezzo')
        indice_superficie = header.index('Superficie')
        indice_cauzione = header.index('Cauzione')
        indice_spese_condominiali = header.index('Spese condominio')

        # Processa ogni riga
        for row in reader:
            try:
                # Pulizia della colonna Prezzo
                prezzo = row[indice_prezzo]
                match_prezzo = re.search(r'\d+[\.,]?\d*', prezzo)
                if match_prezzo:
                    prezzo_valido = float(match_prezzo.group(0).replace(',', '.'))
                    if prezzo_valido < 10:
                        prezzo_valido *= 1000
                    row[indice_prezzo] = str(prezzo_valido)
                else:
                    row[indice_prezzo] = "0"

                # Pulizia della colonna Superficie
                superficie = row[indice_superficie]
                superficie_pulita = superficie[:3].replace(' ', '')
                if superficie_pulita.isdigit():
                    row[indice_superficie] = str(int(superficie_pulita))
                else:
                    row[indice_superficie] = ""

                # Pulizia della colonna Cauzione
                cauzione = row[indice_cauzione]
                if cauzione == "Non indicata":
                    row[indice_cauzione] = "-1"
                else:
                    match_cauzione = re.search(r'\d+[\.,]?\d*', cauzione)
                    if match_cauzione:
                        cauzione_valida = float(match_cauzione.group(0).replace(',', '.'))
                        if cauzione_valida < 10:
                            cauzione_valida *= 1000
                        row[indice_cauzione] = str(cauzione_valida)
                    else:
                        row[indice_cauzione] = "-1"

                # Pulizia della colonna Spese condominiali
                spese_condominiali = row[indice_spese_condominiali]
                if spese_condominiali == "Nessuna spesa condominiale":
                    row[indice_spese_condominiali] = "0"
                else:
                    match_spese = re.search(r'\d+[\.,]?\d*', spese_condominiali)
                    if match_spese:
                        spese_valide = float(match_spese.group(0).replace(',', '.'))
                        if spese_valide < 10:
                            spese_valide *= 1000
                        row[indice_spese_condominiali] = str(spese_valide)
                    else:
                        row[indice_spese_condominiali] = "0"

                # Scrivi la riga pulita nel file di output
                writer.writerow(row)

            except ValueError as e:
                print(f"Errore nella pulizia della riga: {row}, errore: {e}")
                continue

# Nome del file CSV di input e output
file_input = 'annunci_padova.csv'
file_output = 'annunci_padova_puliti.csv'

# Esegui la pulizia dei dati
pulisci_dati(file_input, file_output)

print(f"Dati puliti salvati in {file_output}")
