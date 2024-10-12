import cv2
import numpy as np
import tkinter as tk

# Funzione per ridimensionare l'immagine solo per la visualizzazione
def resize_to_screen(image, screen_width, screen_height):
    # Ottieni le dimensioni originali dell'immagine
    img_height, img_width = image.shape[:2]

    # Trova il fattore di scala per ridimensionare l'immagine mantenendo le proporzioni
    scale_w = screen_width / img_width
    scale_h = screen_height / img_height
    scale = min(scale_w, scale_h)

    # Calcola le nuove dimensioni
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    # Ridimensiona l'immagine
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_image

# Usa Tkinter per ottenere le dimensioni dello schermo
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.withdraw()  # Chiudi la finestra Tkinter

# Dimensioni della scacchiera (numero di angoli interni)
CHECKERBOARD = (8, 6)  # Scacchiera 8x6 angoli interni

# Prepara i punti oggetto reali (coordinate 3D)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Lista per i punti oggetto e immagine
obj_points = []  # Punti 3D reali
img_points = []  # Punti 2D nella foto della scacchiera

# Leggi l'immagine della scacchiera (nome aggiornato: "img.jpg")
image_file = "img.jpg"
img = cv2.imread(image_file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Trova gli angoli interni della scacchiera
ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

# Se la scacchiera è stata trovata correttamente
if ret:
    obj_points.append(objp)
    img_points.append(corners)

    # Disegna gli angoli trovati nella scacchiera sull'immagine originale
    img_with_corners = cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)

    # Ridimensiona l'immagine solo per la visualizzazione
    resized_img = resize_to_screen(img_with_corners, screen_width, screen_height)

    # Mostra l'immagine ridimensionata con gli angoli trovati
    cv2.imshow('Scacchiera con angoli trovati', resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Calibrazione della fotocamera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    # Stampa i risultati
    print("Matrice della fotocamera (intrinseca):\n", mtx)
    print("\nCoefficienti di distorsione:\n", dist)
    print("\nVettore di rotazione (rvecs):\n", rvecs)
    print("\nVettore di traslazione (tvecs):\n", tvecs)
else:
    print("Non è stato possibile trovare gli angoli della scacchiera. Prova con un'immagine diversa o migliora la qualità della foto.")
