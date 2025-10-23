import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Configurar cliente S3 sin firma (acceso anónimo)
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Nombre del bucket
bucket_name = 'smn-ar-wrf'

# Listar objetos en el bucket (puedes agregar prefijos si sabes la estructura, ej. 'wrf/' para subcarpetas)
response = s3.list_objects_v2(Bucket=bucket_name)

# Imprimir nombres de archivos
if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print("El bucket está vacío o no hay acceso.")