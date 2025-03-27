import streamlit as st
import pandas as pd
from components.cards import render_card, show_alert, welcome_banner
from components.navigation import create_tabs_for_offers
from config.app_config import OFFER_CONFIGURATION, HELP_TEXTS, BUCKET_NAME, YEAR, MONTH, DAY
from utils.file_processors import process_and_upload_csv
from libs.classes import OfferLoadTypes

def show_offer_upload():
    """
    Muestra la página de carga de ofertas.
    """
    st.markdown("# Carga de Ofertas")

    # Mostrar banner de bienvenida
    welcome_banner(
        "Bienvenido al Sistema de Carga de Ofertas",
        "Seleccione el tipo de oferta que desea cargar en las pestañas a continuación."
    )

    # Crear pestañas para los diferentes tipos de oferta
    tabs, tab_names = create_tabs_for_offers()

    # Procesar cada pestaña
    for i, tab in enumerate(tabs):
        offer_type = list(OfferLoadTypes)[i].value
        tab_name = tab_names[i]

        with tab:
            st.markdown(f"## Carga de Ofertas {tab_name}")

            # Crear layout con columnas
            col1, col2 = st.columns([2, 1])

            with col1:
                # Card para subir archivos
                render_card(
                    f"Subir Archivo de {tab_name}",
                    f"Cargue su archivo CSV con las ofertas de {tab_name.lower()} para procesamiento y carga a S3."
                )

                # File uploader
                uploaded_file = st.file_uploader(
                    f"Seleccione el archivo de {tab_name}",
                    type=["csv"],
                    key=f"{tab_name.lower()}_file_uploader"
                )

                if uploaded_file is not None:
                    # Vista previa de datos
                    try:
                        df = pd.read_csv(uploaded_file)
                        st.markdown("### Vista previa de datos")
                        st.dataframe(df.head(5), use_container_width=True)

                        # Información del archivo
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Filas", len(df))
                        col2.metric("Columnas", len(df.columns))
                        col3.metric("Tamaño", f"{uploaded_file.size / 1024:.2f} KB")

                        # Botón de procesamiento
                        if tab_name in ["Batch"]:
                            # Botón amarillo para algunos tipos
                            st.markdown('<div class="yellow-btn">', unsafe_allow_html=True)
                            process_button = st.button(f"Procesar y Cargar Ofertas {tab_name}", key=f"{tab_name.lower()}_upload_button")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            # Botón estándar para otros
                            process_button = st.button(f"Procesar y Cargar Ofertas {tab_name}", key=f"{tab_name.lower()}_upload_button")

                        if process_button:
                            success = process_and_upload_csv(uploaded_file, offer_type)
                            if success:
                                show_alert(f"¡Archivo {uploaded_file.name} procesado y cargado correctamente!", "success")
                    except Exception as e:
                        show_alert(f"Error al procesar el archivo: {str(e)}", "error")

            with col2:
                # Card de información
                help_text = HELP_TEXTS.get(offer_type, {}).get("format_required", "")
                if not help_text:
                    # Texto predeterminado si no hay específico
                    help_text = """
                    <b>Formato requerido:</b>
                    <ul>
                        <li>Archivo CSV</li>
                        <li>Tamaño máximo: 50MB</li>
                    </ul>

                    <b>Proceso:</b>
                    <ol>
                        <li>Suba el archivo</li>
                        <li>Valide los datos en la vista previa</li>
                        <li>Haga clic en "Procesar y Cargar"</li>
                    </ol>
                    """

                render_card(
                    "Información",
                    help_text
                )

            # Información adicional
            st.markdown("### Información adicional")
            with st.expander(f"Detalles del proceso de carga {tab_name}"):
                additional_info = HELP_TEXTS.get(offer_type, {}).get("additional_info", "")
                if additional_info:
                    st.markdown(additional_info.format(
                        bucket_name=BUCKET_NAME,
                        year=YEAR,
                        month=MONTH,
                        day=DAY
                    ))
                else:
                    # Información predeterminada
                    config = OFFER_CONFIGURATION.get(offer_type, {})
                    folder_name = config.get("folder_name", "")
                    chunk_size = config.get("chunk_size", "N/A")
                    is_csv = config.get("is_csv", True)

                    st.markdown(f"""
                    Los archivos se procesan en fragmentos y se cargan a S3 con la siguiente estructura:

                    - **Bucket:** `{BUCKET_NAME}`
                    - **Ruta:** `{folder_name}`
                    - **Formato de archivos:** {"CSV" if is_csv else "JSON"}
                    """)

                    if chunk_size != "N/A":
                        st.markdown(f"- **Tamaño de fragmento:** {chunk_size:,} registros")

                # Mostrar información adicional específica
                if offer_type == OfferLoadTypes.PAYMENT.value:
                    st.info("Las ofertas de pago incluirán automáticamente el usuario de carga en cada registro.")
                elif offer_type == OfferLoadTypes.REFINANCE.value:
                    st.info("Las ofertas de refinanciamiento incluirán automáticamente el usuario de carga en cada registro.")
                elif offer_type == OfferLoadTypes.MICRO_LOANS_OFFERS.value:
                    st.info("Las ofertas de micro préstamos se procesarán según las reglas de descarte específicas.")
                elif offer_type == OfferLoadTypes.DA_COLLECTION.value:
                    st.info("Los archivos CSV se transformarán a formato JSON antes de subirse a S3.")
