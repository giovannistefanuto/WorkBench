import qrcode

url = "https://giovannistefanuto.github.io/"  # metti qui il tuo URL
qr = qrcode.make(url)
qr.save("qr_miosito.png")  # Salva il QR code come immagine
