import meteostat as mt
from datetime import datetime
import pandas as pd

# Función para buscar estaciones cercanas (ej. en Argentina)
def find_stations(lat, lon, radius=500000):  # Radio en metros (50km por defecto)
    stations = mt.Stations()
    stations = stations.nearby(lat, lon, radius)
    return stations.fetch()

# Ubicación base (ej. Buenos Aires; ajusta lat/lon para otras áreas)
base_lat, base_lon = -24.6037, -64.3816  # Buenos Aires
print("Buscando estaciones meteorológicas cercanas...")

# Buscar y listar estaciones2
stations_df = find_stations(base_lat, base_lon)
if stations_df.empty:
    print("No se encontraron estaciones cercanas.")
    exit()

print("\nEstaciones disponibles:")
for num, (i, row) in enumerate(stations_df.iterrows(), start=1):  # Contador numérico desde 1
    name = str(row.get('name', 'Desconocido'))
    station_id = str(row.get('wmo', row.get('icao', 'N/A')))
    distance = float(row.get('distance', 0.0))
    print(f"{num}. {name} (ID: {station_id}, Distancia: {distance:.1f} km)")

# Seleccionar estación
try:
    choice = int(input("\nIngresa el número de la estación (1 a {}): ".format(len(stations_df)))) - 1
    if choice < 0 or choice >= len(stations_df):
        raise ValueError
    selected_station = stations_df.iloc[choice]
    station_id = str(selected_station.get('wmo', selected_station.get('icao', 'N/A')))
    print(f"Seleccionaste: {str(selected_station['name'])} (ID: {station_id})")
except ValueError:
    print("Selección inválida.")
    exit()

# Definir rango de fechas (ej. último mes; ajusta según necesidad)
start = datetime(2023, 10, 1)
end = datetime(2023, 10, 31)

# Obtener datos diarios
print("Obteniendo datos...")
data = mt.Daily(station_id, start, end)
data = data.fetch()

if data.empty:
    print("No se encontraron datos para el rango especificado.")
    exit()

print(f"\nDatos obtenidos ({len(data)} días):")
print(data.head())  # Muestra primeras filas

# Cálculos estadísticos básicos (ajusta variables según data: 'tavg' media, 'tmin', 'tmax', 'prcp', 'wspd', etc.)
print("\nCalculando estadísticas...")

# Media de temperatura media diaria
if 'tavg' in data.columns:
    temp_mean = data['tavg'].mean()
    print(f"Temperatura media diaria: {temp_mean:.2f} °C")

# Desviación estándar de precipitación
if 'prcp' in data.columns:
    prcp_std = data['prcp'].std()
    print(f"Desviación estándar de precipitación: {prcp_std:.2f} mm")

# Máximo de temperatura máxima
if 'tmax' in data.columns:
    tmax_max = data['tmax'].max()
    print(f"Temperatura máxima absoluta: {tmax_max:.2f} °C")

# Total de precipitación acumulada
if 'prcp' in data.columns:
    prcp_total = data['prcp'].sum()
    print(f"Precipitación total acumulada: {prcp_total:.2f} mm")

# Ejemplo adicional: Conteo de días con lluvia (>0 mm)
if 'prcp' in data.columns:
    rainy_days = (data['prcp'] > 0).sum()
    print(f"Días con precipitación: {rainy_days}")

print("Procesamiento completado.")
