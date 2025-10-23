import boto3
from botocore import UNSIGNED
from botocore.client import Config
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
bucket_name = 'smn-ar-wrf'
# Ejemplo de clave de archivo (cámbiala por una real de la lista)
file_key = 'DATA/WRF/DET/2022/01/08/12/WRFDETAR_01H_20220108_12_005.nc'  # Ajusta según lo que encuentres
# Descargar a un archivo local
local_file_path = 'datos_meteorologicos.nc'  # Elige un nombre y extensión (probablemente .grib o .nc)
s3.download_file(bucket_name, file_key, local_file_path)
print(f"Archivo descargado a {local_file_path}")
