     import requests
     import pandas as pd
     from datetime import datetime

     # Tu API key de OpenWeatherMap (regístrate para obtenerla)
     API_KEY = "TU_API_KEY_AQUI"  # Reemplaza con tu key real

     # Coordenadas del usuario (ej. Buenos Aires)
     lat = -34.6037
     lon = -58.3816

     # Obtener datos actuales
     url_current = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
     response = requests.get(url_current)
     if response.status_code == 200:
         data = response.json()
         humidity = data['main']['humidity']  # Humedad relativa (%)
         temp = data['main']['temp']  # Temperatura (°C)
         print(f"Humedad actual: {humidity}%, Temperatura: {temp}°C")
     else:
         print("Error al acceder a OpenWeatherMap.")

     # Para pronósticos (5 días, incluye humedad)
     url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
     response = requests.get(url_forecast)
     if response.status_code == 200:
         data = response.json()
         # Procesa lista de pronósticos (cada 3 horas)
         for item in data['list'][:5]:  # Primeros 5 (ej. 15 horas)
             dt = datetime.fromtimestamp(item['dt'])
             humidity = item['main']['humidity']
             temp = item['main']['temp']
             print(f"{dt}: Humedad {humidity}%, Temp {temp}°C")
     