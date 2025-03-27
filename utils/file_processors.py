import streamlit as st
import pandas as pd
import numpy as np
import tempfile
import os
import datetime
import json
from pathlib import Path
from config.app_config import OFFER_CONFIGURATION, BUCKET_NAME
from libs.classes import OffersFormatHeadersFileException
from utils.s3_utils import upload_file_to_s3
from config.aws_config import generate_batch_folder_name

def reformat_file(file_content, is_csv=True):
    """
    Reformatea el contenido del archivo.

    Args:
        file_content (str): Contenido del archivo.
        is_csv (bool): Indica si es un archivo CSV.

    Returns:
        str: Contenido reformateado.
    """
    if is_csv:
        return file_content.replace('|', ',')
    return file_content

def process_and_upload_csv(uploaded_file, offer_type):
    """
    Procesa y sube un archivo CSV a S3.

    Args:
        uploaded_file (streamlit.UploadedFile): Archivo subido.
        offer_type (str): Tipo de oferta.

    Returns:
        bool: True si se completa con éxito, False en caso contrario.
    """
    if uploaded_file is None:
        st.warning("Por favor, suba un archivo primero.")
        return False

    config = OFFER_CONFIGURATION.get(offer_type)
    if not config:
        st.error("Tipo de oferta no válido.")
        return False

    try:
        # Guardar archivo subido a directorio temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name

        # Mostrar progreso
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Aplicar reglas de descarte si corresponde
        if 'discard_rule' in config and config['discard_rule'] is not None:
            status_text.text("Aplicando reglas de descarte...")
            progress_bar.progress(25)
            temp_file_path = config['discard_rule'](temp_file_path, config['header_format'])

        # Leer y procesar en fragmentos si se especifica
        chunk_size = config.get('chunk_size', 10000)
        is_csv = config.get('is_csv', True)

        status_text.text("Procesando y subiendo en fragmentos...")
        progress_bar.progress(50)

        # Generar nombre de lote para S3
        batch_folder = generate_batch_folder_name(config['folder_name'])

        # Campos adicionales de la configuración
        additional_fields = config.get('options', {}).get("additional_fields", {}).items()
        endupload_flag = config.get('options', {}).get("endupload_flag")
        transform_function = config.get('options', {}).get('transform_function', None)

        # Procesar archivo en fragmentos
        i = 0
        df_chunks = pd.read_csv(temp_file_path)
        total_chunks = len(df_chunks) // chunk_size + (1 if len(df_chunks) % chunk_size != 0 else 0)

        for i, chunk in enumerate(np.array_split(df_chunks, total_chunks)):
            # Actualizar progreso
            progress_value = 50 + (i / total_chunks) * 40
            progress_bar.progress(int(progress_value))
            status_text.text(f"Procesando fragmento {i+1}/{total_chunks}...")

            for field, value in additional_fields:
                chunk[field] = value

            key_suffix = ''
            # Procesar según el tipo de archivo
            if is_csv:
                chunk_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
                chunk.to_csv(chunk_file.name, index=False)
                temp_chunk_path = chunk_file.name
            else:
                chunk_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
                if transform_function is not None:
                    with open(chunk_file.name, 'w') as fwriter:
                        json.dump(transform_function(chunk), fwriter)
                key_suffix = f'da-ondemand-{i}.json'
                temp_chunk_path = chunk_file.name

            # Subir a S3
            upload_file_to_s3(
                temp_chunk_path,
                BUCKET_NAME,
                batch_folder,
                key_suffix=key_suffix,
                is_csv=is_csv
            )

            # Limpiar archivo temporal
            os.unlink(temp_chunk_path)

        # Subir flag de fin si es necesario
        if endupload_flag:
            status_text.text("Finalizando subida...")
            end_flag_file = tempfile.NamedTemporaryFile(delete=False, suffix='.flag')
            with open(end_flag_file.name, 'w') as f:
                f.write('')

            upload_file_to_s3(
                end_flag_file.name,
                BUCKET_NAME,
                batch_folder,
                key_suffix=f'{endupload_flag}.flag'
            )

            os.unlink(end_flag_file.name)

        # Limpiar archivo temporal original
        os.unlink(temp_file_path)

        # Completar progreso
        progress_bar.progress(100)
        status_text.text("¡Carga completa!")

        # Agregar a estadísticas de carga
        if 'upload_stats' not in st.session_state:
            st.session_state.upload_stats = {}

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if today not in st.session_state.upload_stats:
            st.session_state.upload_stats[today] = {}

        offer_name = next((t.name for t in list(OFFER_CONFIGURATION.keys()) if t.value == offer_type), offer_type)
        if offer_name not in st.session_state.upload_stats[today]:
            st.session_state.upload_stats[today][offer_name] = 0

        st.session_state.upload_stats[today][offer_name] += 1

        # Actualizar historial de cargas
        if 'upload_history' not in st.session_state:
            st.session_state.upload_history = []

        st.session_state.upload_history.append({
            'filename': uploaded_file.name,
            'bucket': BUCKET_NAME,
            'key': f"{batch_folder}{uploaded_file.name}",
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return True

    except OffersFormatHeadersFileException as e:
        st.error(f"Error de formato: {e.message}")
        return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def validate_headers(uploaded_file, required_headers):
    """
    Valida que el archivo tenga las columnas requeridas.

    Args:
        uploaded_file (streamlit.UploadedFile): Archivo subido.
        required_headers (list): Lista de columnas requeridas.

    Returns:
        tuple: (bool, DataFrame) Indica si es válido y el DataFrame leído.
    """
    try:
        df = pd.read_csv(uploaded_file)

        # Verificar si todas las columnas requeridas están presentes
        missing_headers = set(required_headers) - set(df.columns)
        if missing_headers:
            return False, None, f"Faltan las siguientes columnas: {', '.join(missing_headers)}"

        return True, df, None
    except Exception as e:
        return False, None, f"Error al leer el archivo: {str(e)}"
