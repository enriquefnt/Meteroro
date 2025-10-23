import xarray as xr

# Ruta al archivo GRIB descargado (ej. del bucket S3)
file_path = 'wrfout_d01_2023-10-01_00:00:00.grib'  # Reemplaza con tu archivo real

# Abre el dataset con cfgrib
ds = xr.open_dataset(file_path, engine='cfgrib')

# Muestra las variables disponibles (ej. temperatura a 2m: 't2m')
print(ds)

# Cálculos estadísticos básicos (ej. para temperatura a 2m)
if 't2m' in ds:
    # Media espacial (sobre latitud y longitud)
    temp_mean = ds['t2m'].mean(dim=['latitude', 'longitude'])
    print(f"Temperatura media: {temp_mean.values} K")  # Convierte a °C si es necesario: -273.15
    
    # Desviación estándar temporal (si hay múltiples tiempos)
    if 'time' in ds.dims:
        temp_std = ds['t2m'].std(dim='time')
        print(f"Desviación estándar temporal: {temp_std.values} K")
    
    # Máximo y mínimo
    temp_max = ds['t2m'].max()
    temp_min = ds['t2m'].min()
    print(f"Temperatura máxima: {temp_max.values} K, Mínima: {temp_min.values} K")
    
    # Ejemplo de cálculo personalizado: Media por día (si hay datos horarios)
    # ds_daily = ds.resample(time='D').mean()  # Agrupa por día
    # print(ds_daily['t2m'])
else:
    print("Variable 't2m' no encontrada; revisa las variables en ds.")

# Cierra el dataset
ds.close()
