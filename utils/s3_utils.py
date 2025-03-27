import boto3
import datetime
import streamlit as st
from config.aws_config import AWS_REGION, get_s3_client

def upload_file_to_s3(file_name, bucket, folder_name, key_suffix='', is_csv=True):
    """
    Sube un archivo a S3.

    Args:
        file_name (str): Ruta del archivo a subir.
        bucket (str): Nombre del bucket de S3.
        folder_name (str): Carpeta de destino en S3.
        key_suffix (str): Sufijo para la clave de S3.
        is_csv (bool): Indica si es un archivo CSV.

    Returns:
        bool: True si se completa con éxito.
    """
    hour_created = datetime.datetime.now().strftime("%H%M%S")
    date_created = datetime.datetime.now().strftime("%Y%m%d")

    if is_csv:
        # Reemplazar pipes con comas
        with open(file_name, 'r') as f:
            filedata = f.read()
        filedata = filedata.replace('|', ',')
        with open(file_name, 'w') as f:
            f.write(filedata)

    # En producción, esto utilizaría el SDK real de AWS
    # s3 = boto3.client('s3', region_name=AWS_REGION)
    # key = folder_name + (key_suffix or (date_created + hour_created + '_offers.csv'))
    # s3.upload_file(file_name, bucket, key)

    # Para desarrollo, simulamos la subida
    key = folder_name + (key_suffix or (date_created + hour_created + '_offers.csv'))

    # Log message for development
    print(f'[SIMULATED] File {file_name} was successfully uploaded to S3 {bucket}/{key}.')

    return True

def get_s3_object_exists(bucket, key):
    """
    Verifica si un objeto existe en S3.

    Args:
        bucket (str): Nombre del bucket de S3.
        key (str): Clave del objeto en S3.

    Returns:
        bool: True si el objeto existe.
    """
    try:
        # En producción, esto utilizaría el SDK real de AWS
        # s3 = get_s3_client()
        # s3.head_object(Bucket=bucket, Key=key)
        # return True

        # Para desarrollo, simulamos la verificación
        return True
    except Exception:
        return False

def create_presigned_url(bucket, key, expiration=3600):
    """
    Crea una URL prefirmada para un objeto en S3.

    Args:
        bucket (str): Nombre del bucket de S3.
        key (str): Clave del objeto en S3.
        expiration (int): Tiempo de expiración en segundos.

    Returns:
        str: URL prefirmada.
    """
    try:
        # En producción, esto utilizaría el SDK real de AWS
        # s3 = get_s3_client()
        # response = s3.generate_presigned_url('get_object',
        #                                     Params={'Bucket': bucket,
        #                                             'Key': key},
        #                                     ExpiresIn=expiration)
        # return response

        # Para desarrollo, simulamos la URL
        return f"https://{bucket}.s3.amazonaws.com/{key}?signature=EXAMPLE"
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

def list_objects(bucket, prefix):
    """
    Lista objetos en un bucket de S3.

    Args:
        bucket (str): Nombre del bucket de S3.
        prefix (str): Prefijo para filtrar objetos.

    Returns:
        list: Lista de objetos.
    """
    try:
        # En producción, esto utilizaría el SDK real de AWS
        # s3 = get_s3_client()
        # response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        # return response.get('Contents', [])

        # Para desarrollo, simulamos la lista
        return [{'Key': f"{prefix}example_file_{i}.csv", 'LastModified': datetime.datetime.now(), 'Size': 1024} for i in range(5)]
    except Exception as e:
        print(f"Error listing objects: {e}")
        return []
