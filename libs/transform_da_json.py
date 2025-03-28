import pandas as pd
import numpy as np

def transform_da_json(input_df: pd.DataFrame) -> list:
    """
    Transforma un DataFrame a formato JSON para DA Collection.

    Args:
        input_df (pd.DataFrame): DataFrame de entrada.

    Returns:
        list: Lista de diccionarios transformados.
    """
    # Reemplazar NaN con None para JSON
    transformed_data = input_df.replace({np.nan: None}).to_dict(orient='records')

    # Añadir estructura 'body' para cada registro
    return list(map(lambda el: {'body': el}, transformed_data))
