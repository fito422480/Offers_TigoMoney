import boto3
import datetime
from config.app_config import AWS_REGION, ACCOUNT_ID, APPNAME, COUNTRY, ENVIRONMENT

# Configuración de AWS
BUCKET_NAME = f'step-functions-data-{ENVIRONMENT}-{APPNAME}-{COUNTRY}-{AWS_REGION}-{ACCOUNT_ID}'

class STSClient:
    """
    Cliente para AWS STS (Security Token Service).
    En producción, esta clase utilizaría boto3 para obtener credenciales reales.
    """
    def get_caller_identity(self):
        """
        Obtiene la identidad del usuario actual.

        Returns:
            dict: Diccionario con información de identidad.
        """
        # En producción, esto sería:
        # client = boto3.client("sts")
        # return client.get_caller_identity()

        # Para desarrollo, retornamos un mock
        return {"UserId": "AROAXXXXXXXXXXXXXXXXX:user"}

def get_s3_client():
    """
    Obtiene un cliente de S3.

    Returns:
        boto3.client: Cliente de S3 configurado.
    """
    # En producción, esto utilizaría credenciales reales
    return boto3.client('s3', region_name=AWS_REGION)

def generate_s3_path(folder_name, file_name):
    """
    Genera una ruta para S3.

    Args:
        folder_name (str): Nombre de la carpeta.
        file_name (str): Nombre del archivo.

    Returns:
        str: Ruta completa para S3.
    """
    hour_created = datetime.datetime.now().strftime("%H%M%S")
    date_created = datetime.datetime.now().strftime("%Y%m%d")

    return f"{folder_name}{date_created}{hour_created}_{file_name}"

def generate_batch_folder_name(base_folder):
    """
    Genera un nombre de carpeta para un lote.

    Args:
        base_folder (str): Carpeta base.

    Returns:
        str: Nombre de carpeta de lote.
    """
    hour_created = datetime.datetime.now().strftime("%H%M%S")
    date_created = datetime.datetime.now().strftime("%Y%m%d")

    return f"{base_folder}cluster_{date_created}{hour_created}/"
