import tempfile
import pandas as pd
import numpy as np
from typing import cast
from pathlib import Path
from libs.classes import OfferHeadersMandatory, OffersFormatHeadersFileException

# Variable para simular la configuración del entorno
COUNTRY = "colombia"

def is_valid_file_headers(file_name: str, headers_type: OfferHeadersMandatory = OfferHeadersMandatory.DIRECT) -> bool:
    """
    Verifica si el archivo tiene las cabeceras necesarias.

    Args:
        file_name (str): Ruta del archivo.
        headers_type (OfferHeadersMandatory): Tipo de cabeceras requeridas.

    Returns:
        tuple: (bool, DataFrame) Indica si es válido y el DataFrame leído.
    """
    df_val = pd.read_csv(file_name)
    # if not (len(list(set(df_val.columns) - set(headers_type.value))) == 0 and len(list(set(headers_type.value) - set(df_val.columns))) == 0):
    if not all(header in list(df_val.columns) for header in list(headers_type.value)):
        return False, None
    return True, df_val


def discard_offers_rules(file_name: str, headers_type: OfferHeadersMandatory = OfferHeadersMandatory.DIRECT) -> str:
    """
    Aplica reglas de descarte para ofertas estándar.

    Args:
        file_name (str): Ruta del archivo.
        headers_type (OfferHeadersMandatory): Tipo de cabeceras requeridas.

    Returns:
        str: Ruta del archivo procesado.
    """
    file_path = Path(file_name)
    is_valid_file, df_clean = is_valid_file_headers(file_name, headers_type)
    if not is_valid_file:
        raise OffersFormatHeadersFileException()

    df_clean = df_clean[(df_clean['FirstName'].notnull())]
    df_clean = df_clean[(df_clean['LastName'].notnull())]

    if "Installment_ProductType" not in df_clean.columns:
        index_df = list(df_clean.columns).index('FirstName')
        df_clean.insert(index_df, "Installment_ProductType", "NN")
        # df_clean["Installment_ProductType"] = ''

    out_path = Path(tempfile.gettempdir()).joinpath(file_path.name)
    cast(pd.DataFrame, df_clean).to_csv(out_path, index=False)
    return str(out_path.resolve())


def discard_micro_loan_offers(file_name: str,
                              headers_type: OfferHeadersMandatory = OfferHeadersMandatory.MICRO_LOAN_OFFERS) -> str:
    """
    Aplica reglas de descarte para micro préstamos.

    Args:
        file_name (str): Ruta del archivo.
        headers_type (OfferHeadersMandatory): Tipo de cabeceras requeridas.

    Returns:
        str: Ruta del archivo procesado.
    """
    file_path = Path(file_name)
    is_valid_file, df_clean = is_valid_file_headers(file_name, headers_type)
    if not is_valid_file:
        raise OffersFormatHeadersFileException()

    df_clean = df_clean[(df_clean['FirstName'].notnull())]
    df_clean = df_clean[(df_clean['LastName'].notnull())]

    # Verificamos si las columnas existen antes de filtrar
    if 'IdWallet' in df_clean.columns:
        df_clean = df_clean[(df_clean['IdWallet'].notnull())]

    if 'DocumentNumber' in df_clean.columns:
        df_clean = df_clean[(df_clean['DocumentNumber'].notnull())]

    if 'OfferAmount' in df_clean.columns:
        df_clean = df_clean[(df_clean['OfferAmount'].notnull())]

    if 'ProductType' in df_clean.columns:
        df_clean = df_clean[(df_clean['ProductType'].notnull())]

    out_path = Path(tempfile.gettempdir()).joinpath(file_path.name)
    cast(pd.DataFrame, df_clean).to_csv(out_path, index=False)
    return str(out_path.resolve())
