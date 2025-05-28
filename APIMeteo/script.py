import requests
from datetime import date, timedelta

# Coordinate di Padova
lat = 45.4064
lon = 11.8768

# Costruzione dell'URL per previsioni meteo orarie oggi e domani
start_date = date.today()
end_date = start_date + timedelta(days=1)

url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    f"&hourly=temperature_2m,weathercode"
    f"&start_date={start_date}&end_date={end_date}"
    "&timezone=Europe%2FBerlin"
)

# Mappa dei codici meteo con emoji e descrizioni
weather_codes = {
    0: ("Cielo sereno", "☀️"),
    1: ("Prevalentemente sereno", "🌤"),
    2: ("Parzialmente nuvoloso", "⛅"),
    3: ("Coperto", "☁️"),
    45: ("Nebbia", "🌫"),
    48: ("Nebbia con brina", "🌫❄️"),
    51: ("Pioggerella leggera", "🌦"),
    53: ("Pioggerella moderata", "🌦"),
    55: ("Pioggerella intensa", "🌧"),
    61: ("Pioggia leggera", "🌧"),
    63: ("Pioggia moderata", "🌧💧"),
    65: ("Pioggia intensa", "🌧🌊"),
    66: ("Pioggia gelata leggera", "🌧❄️"),
    67: ("Pioggia gelata intensa", "🌧❄️❄️"),
    71: ("Neve leggera", "🌨"),
    73: ("Neve moderata", "❄️"),
    75: ("Neve intensa", "❄️❄️"),
    80: ("Rovesci leggeri", "🌦"),
    81: ("Rovesci moderati", "🌧"),
    82: ("Rovesci violenti", "🌧⚡"),
    95: ("Temporale", "⛈"),
    96: ("Temporale con grandine", "⛈🌨"),
    99: ("Temporale violento con grandine", "⛈🌨⚡")
}

def get_weather():
    response = requests.get(url)
    data = response.json()

    temps = data['hourly']['temperature_2m']
    codes = data['hourly']['weathercode']
    times = data['hourly']['time']

    print("📍 Meteo per Padova, Italia (fonte: Open-Meteo.com)\n")

    for i in range(len(times)):
        hour = times[i][11:16]
        giorno = times[i][:10]
        temp = temps[i]
        code = codes[i]
        descrizione, emoji = weather_codes.get(code, ("Sconosciuto", "❓"))

        if giorno == str(start_date):
            header = "📅 Oggi"
        elif giorno == str(end_date):
            header = "📅 Domani"
        else:
            continue

        if hour == "00:00" or i == 0 or times[i-1][:10] != giorno:
            print(f"\n{header} ({giorno}):")

        print(f" - {hour}: {temp}°C, {descrizione} {emoji}")

try:
    get_weather()
except Exception as e:
    print("❌ Errore nel recupero delle previsioni:", e)
