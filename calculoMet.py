import meteostat as mt
from datetime import datetime
import pandas as pd
import re  # Para sanitizar el nombre

# Función para buscar estaciones cercanas (ej. en Argentina)
def find_stations(lat, lon, radius=300000):  # Radio en metros (50km por defecto; ajusta si necesitas más)
    stations = mt.Stations()
    stations = stations.nearby(lat, lon, radius)
    return stations.fetch()

# Solicitar coordenadas al usuario
while True:
    try:
        lat = float(input("Ingresa la latitud (ej. -34.6037 para Buenos Aires): "))
        lon = float(input("Ingresa la longitud (ej. -58.3816 para Buenos Aires): "))
        break
    except ValueError:
        print("Error: Ingresa números válidos para latitud y longitud.")

# Solicitar período de fechas al usuario
while True:
    try:
        start_str = input("Ingresa la fecha inicial (formato dd/mm/yyyy, ej. 01/10/2023): ")
        end_str = input("Ingresa la fecha final (formato dd/mm/yyyy, ej. 31/10/2023): ")
        start = datetime.strptime(start_str, '%d/%m/%Y')
        end = datetime.strptime(end_str, '%d/%m/%Y')
        if start >= end:
            raise ValueError("La fecha inicial debe ser anterior a la final.")
        break
    except ValueError as e:
        print(f"Error: {e}. Ingresa fechas válidas en formato dd/mm/yyyy.")

print(f"\nBuscando estaciones meteorológicas cercanas a latitud {lat}, longitud {lon} (radio: 50 km)...")

# Buscar y listar estaciones
stations_df = find_stations(lat, lon)
if stations_df.empty:
    print("No se encontraron estaciones cercanas en el radio especificado. Intenta aumentar el radio o cambiar coordenadas.")
    exit()

print("\nEstaciones disponibles (distancia desde las coordenadas ingresadas):")
for num, (i, row) in enumerate(stations_df.iterrows(), start=1):  # Contador numérico desde 1
    name = str(row.get('name', 'Desconocido'))
    station_id = str(row.get('wmo', row.get('icao', 'N/A')))
    distance_m = float(row.get('distance', 0.0))  # Distancia en metros
    distance_km = distance_m / 1000  # Convertir a km
    print(f"{num}. {name} (ID: {station_id}, Distancia: {distance_km:.1f} km)")

# Seleccionar estación
while True:
    try:
        choice = int(input("\nIngresa el número de la estación (1 a {}): ".format(len(stations_df)))) - 1
        if choice < 0 or choice >= len(stations_df):
            raise ValueError
        selected_station = stations_df.iloc[choice]
        station_id = str(selected_station.get('wmo', selected_station.get('icao', 'N/A')))
        station_name = str(selected_station['name'])
        print(f"Seleccionaste: {station_name} (ID: {station_id})")
        break
    except ValueError:
        print("Selección inválida. Ingresa un número entre 1 y {}.".format(len(stations_df)))

# Obtener datos diarios
print("Obteniendo datos...")
data = mt.Daily(station_id, start, end)
data = data.fetch()

if data.empty:
    print("No se encontraron datos para el rango especificado.")
    exit()

print(f"\nDatos obtenidos ({len(data)} días):")
print(data.head())  # Muestra primeras filas en prompt

# Cálculos estadísticos básicos (ajusta variables según data: 'tavg' media, 'tmin', 'tmax', 'prcp', 'wspd', etc.)
print("\nCalculando estadísticas...")

# Inicializar diccionario para estadísticas
stats = {}

# Media de temperatura media diaria
if 'tavg' in data.columns:
    temp_mean = data['tavg'].mean()
    stats['Temperatura Media Diaria (°C)'] = temp_mean
    print(f"Temperatura media diaria: {temp_mean:.2f} °C")

# Desviación estándar de precipitación
if 'prcp' in data.columns:
    prcp_std = data['prcp'].std()
    stats['Desviación Estándar Precipitación (mm)'] = prcp_std
    print(f"Desviación estándar de precipitación: {prcp_std:.2f} mm")

# Máximo de temperatura máxima
if 'tmax' in data.columns:
    tmax_max = data['tmax'].max()
    stats['Temperatura Máxima Absoluta (°C)'] = tmax_max
    print(f"Temperatura máxima absoluta: {tmax_max:.2f} °C")


# Agregado: Temperatura mínima absoluta
if 'tmin' in data.columns:
    tmin_min = data['tmin'].min()
    stats['Temperatura Mínima Absoluta (°C)'] = tmin_min
    print(f"Temperatura mínima absoluta: {tmin_min:.2f} °C")
# Agregado: Media de temperaturas mínimas diarias
if 'tmin' in data.columns:
    tmin_mean = data['tmin'].mean()
    stats['Temperatura Mínima Media Diaria (°C)'] = tmin_mean
    print(f"Temperatura mínima media diaria: {tmin_mean:.2f} °C")    

# Total de precipitación acumulada
if 'prcp' in data.columns:
    prcp_total = data['prcp'].sum()
    stats['Precipitación Total Acumulada (mm)'] = prcp_total
    print(f"Precipitación total acumulada: {prcp_total:.2f} mm")

# Ejemplo adicional: Conteo de días con lluvia (>0 mm)
if 'prcp' in data.columns:
    rainy_days = (data['prcp'] > 0).sum()
    stats['Días con Precipitación'] = rainy_days
    print(f"Días con precipitación: {rainy_days}")

print("Procesamiento completado.")

# Construir nombre del archivo
station_name_clean = re.sub(r'[^\w\-]', '', station_name.replace(' ', '_'))  # Limpia caracteres no alfanuméricos y reemplaza espacios
start_date = start.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD para el nombre del archivo
filename = f"{station_name_clean}_{start_date}.xlsx"

# Exportar a Excel
print(f"\nExportando datos a Excel: {filename}...")
try:
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Hoja 1: Datos diarios
        data.to_excel(writer, sheet_name='Datos Diarios', index=True)
        
        # Hoja 2: Estadísticas
        stats_df = pd.DataFrame(list(stats.items()), columns=['Estadística', 'Valor'])
        stats_df.to_excel(writer, sheet_name='Estadísticas', index=False)
    
    print(f"Archivo '{filename}' creado exitosamente con dos hojas.")
except Exception as e:
    print(f"Error al exportar a Excel: {e}")
