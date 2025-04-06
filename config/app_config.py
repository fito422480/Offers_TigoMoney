import datetime
from libs.classes import OfferHeadersMandatory, OfferLoadTypes
from libs.discard_offers_functions import discard_offers_rules, discard_micro_loan_offers
from libs.transform_da_json import transform_da_json

# Environment variables
ENVIRONMENT = "dev"
COUNTRY = "colombia"
APPNAME = "tigo-money"
AWS_REGION = "us-east-1"
ACCOUNT_ID = "123456789012"

# Nombre del bucket de S3
BUCKET_NAME = f'step-functions-data-{ENVIRONMENT}-{APPNAME}-{COUNTRY}-{AWS_REGION}-{ACCOUNT_ID}'

# Date constants
YEAR = datetime.datetime.now().strftime("%Y")
MONTH = datetime.datetime.now().strftime("%m")
DAY = datetime.datetime.now().strftime("%d")

# User information (from AWS in production)
LOAD_USER = "user"

# Colores de la marca Tigo Money
TIGO_COLORS = {
    "primary": "#fac619",        # Amarillo Tigo
    "primary_light": "#fdd44f",  # Amarillo claro
    "primary_dark": "#e6a800",   # Amarillo oscuro
    "secondary": "#363856",      # Azul oscuro rico
    "secondary_light": "#4a4c6a", # Azul claro, ligeramente ajustado
    "secondary_dark": "#21222f",  # Azul más oscuro
    "background": "#FFFFFF",     # Fondo blanco puro
    "text_primary": "#363856",   # Texto principal (azul)
    "text_secondary": "#4b4d6d", # Texto secundario
    "success": "#10B981",        # Verde para éxito
    "warning": "#fac619",        # Amarillo para advertencia
    "error": "#EF4444",          # Rojo para error
    "info": "#3B82F6"            # Azul para información
}

# Configuration de los tipos de ofertas
OFFER_CONFIGURATION = {
    OfferLoadTypes.DIRECT.value: {
        "file_name": "output_lending_offers.csv",
        "folder_name": f'offers/news/direct/year={YEAR}/month={MONTH}/day={DAY}/',
        "header_format": OfferHeadersMandatory.DIRECT,
        "discard_rule": discard_offers_rules,
        "options": {
            "endupload_flag": 'offers_direct_news_endupload'
        }
    },
    OfferLoadTypes.BATCH.value: {
        "file_name": "output_lending_offers_batch.csv",
        "folder_name": f'offers/news/batch/year={YEAR}/month={MONTH}/day={DAY}/',
        "header_format": OfferHeadersMandatory.BATCH,
        "discard_rule": discard_offers_rules,
        "options": {
            "endupload_flag": 'offers_batch_news_endupload'
        }
    },
    OfferLoadTypes.PAYMENT.value: {
        "file_name": "campaign_deductions_debt_loans.csv",
        "folder_name": f'collection/removal/year={YEAR}/month={MONTH}/day={DAY}/',
        "header_format": OfferHeadersMandatory.PAYMENT,
        "chunk_size": 5000,
        "options": {
            "endupload_flag": 'paymentoffer_news_endupload',
            "additional_fields": {
                "IdLoadUsr": LOAD_USER,
            }
        }
    },
    OfferLoadTypes.REFINANCE.value: {
        "file_name": "collection_refinancing_campaign.csv",
        "folder_name": f"collection/refinance/year={YEAR}/month={MONTH}/day={DAY}/",
        "header_format": OfferHeadersMandatory.REFINANCE,
        "chunk_size": 5000,
        "options": {
            "endupload_flag": 'refinance_news_endupload',
            "additional_fields": {
                "IdLoadUsr": LOAD_USER,
            }
        }
    },
    OfferLoadTypes.MICRO_LOANS_OFFERS.value: {
        "file_name": "output_micro_loan_offers.csv",
        "folder_name": f'micro_loan_offers/news/direct/year={YEAR}/month={MONTH}/day={DAY}/',
        "header_format": OfferHeadersMandatory.MICRO_LOAN_OFFERS,
        "discard_rule": discard_micro_loan_offers,
        "options": {
            "endupload_flag": 'micro_loan_offers_news_endupload',
            "additional_fields": {
                "IdLoadUsr": LOAD_USER,
            }
        }
    },
    OfferLoadTypes.DA_COLLECTION.value: {
        "file_name": "output_da_collection.csv",
        "folder_name": f'automatic_debit/on-demand/year={YEAR}/month={MONTH}/day={DAY}/',
        "header_format": OfferHeadersMandatory.DA_COLLECTION,
        "chunk_size": 10000,
        "is_csv": False,
        "options": {
            "endupload_flag": 'da_collection_news_endupload',
            "transform_function": transform_da_json
        }
    }
}

# Definiciones de textos de ayuda para cada tipo de oferta
HELP_TEXTS = {
    OfferLoadTypes.BATCH.value: {
        "format_required": """
        <p style="font-weight: 600; color: white; margin-bottom: 10px;">Formato requerido:</p>
        <ul style="padding-left: 20px; margin-bottom: 15px; color: white;">
            <li>Archivo CSV</li>
            <li>Columnas obligatorias: FirstName, LastName</li>
            <li>Tamaño máximo: 50MB</li>
        </ul>

        <p style="font-weight: 600; color: white; margin-bottom: 10px;">Proceso:</p>
        <ol style="padding-left: 20px; color: white;">
            <li>Suba el archivo</li>
            <li>Valide los datos en la vista previa</li>
            <li>Haga clic en "Procesar y Cargar"</li>
        </ol>
        """,
        "additional_info": """
        Las ofertas batch se procesan en fragmentos y se cargan a S3 con la siguiente estructura:

        - **Bucket:** `{bucket_name}`
        - **Ruta:** `offers/news/batch/year={year}/month={month}/day={day}/`
        - **Formato de archivos:** CSV con valores separados por comas
        """
    },
    # Resto de la configuración de HELP_TEXTS sigue igual...
}