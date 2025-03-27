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

# Date constants
YEAR = datetime.datetime.now().strftime("%Y")
MONTH = datetime.datetime.now().strftime("%m")
DAY = datetime.datetime.now().strftime("%d")

# User information (from AWS in production)
LOAD_USER = "user"

# Colores de la marca
TIGO_YELLOW = "#fac619"
TIGO_BLUE = "#363856"
TIGO_LIGHT_BLUE = "#4a4c6a"
TIGO_LIGHT_YELLOW = "#fad54d"

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

# Definiciones de textos de ayuda
HELP_TEXTS = {
    OfferLoadTypes.BATCH.value: {
        "format_required": """
        <b>Formato requerido:</b>
        <ul>
            <li>Archivo CSV</li>
            <li>Columnas obligatorias: FirstName, LastName</li>
            <li>Tamaño máximo: 50MB</li>
        </ul>

        <b>Proceso:</b>
        <ol>
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
    # Los demás tipos de ofertas tendrían configuraciones similares
}
