from bs4 import BeautifulSoup

#Questo progetto è un tentativo (per imparare) di come si può utilizzare BeautifulSoup per estrarre informazioni 
#da un file LOCALE in HTML

with open ('home.html', 'r') as file:
    content = file.read()
    #print(content)  #VEDI IL CONTENUTO DELL'HTML IN MODO GREZZO
    soup = BeautifulSoup(content, 'lxml')
    #print(soup.prettify())  #VEDI IL CONTENUTO DELL'HTML IN MODO ORDINATO
    #courses_html_tags = soup.find_all('h5')
    #print(courses_html_tags)  #VEDI IL CONTENUTO DI TAGS, OVVERO TUTTI I TAGS DI TIPO H5
    #for course in courses_html_tags:
    #    print(course.text)    #VEDI IL CONTENUTO DI TEXT, OVVERO TUTTI I TEXT DENTRO I TAGS DI TIPO H5

    course_cards = soup.find_all('div', class_='card')   #N.B. mettere class_ invece di class perchè class è una keyword in python
    for course in course_cards:
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]   #"a" è il tag che contiene il prezzo, "split()" divide il testo in una lista di parole, e [-1] prende l'ultimo elemento della lista
        print(f'{course_name} costa esattamente {course_price}')