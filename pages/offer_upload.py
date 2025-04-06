import streamlit as st
import pandas as pd
from components.cards import render_card, show_alert
from components.navigation import create_tabs_for_offers
from config.app_config import OFFER_CONFIGURATION, HELP_TEXTS, BUCKET_NAME, YEAR, MONTH, DAY, TIGO_COLORS
from utils.file_processors import process_and_upload_csv
from libs.classes import OfferLoadTypes
from utils.ui_helpers import welcome_banner, create_section_header

def show_offer_upload():
    """
    Muestra la página de carga de ofertas con estilo Tigo Money.
    """
    # Título principal con ícono (link icon)
    st.markdown("<h1 style='color: #363856; margin-bottom: 0;'>Carga de Ofertas</h1>", unsafe_allow_html=True)

    # Crear pestañas para los diferentes tipos de oferta
    tabs, tab_names = create_tabs_for_offers()

    # Procesar cada pestaña
    for i, tab in enumerate(tabs):
        offer_type_name = tab_names[i]
        offer_type = next(
            (t.value for t in OfferLoadTypes if t.name.upper() == offer_type_name.upper().replace(" ", "_")),
            list(OfferLoadTypes)[i].value
        )

        with tab:
            # Título de la sección con ícono (link icon)
            st.markdown(f"<h2 style='color: #363856;'>Carga de Ofertas {offer_type_name}</h2>", unsafe_allow_html=True)

            # Crear layout con columnas
            col1, col2 = st.columns([2, 1])

            with col1:
                # Sección de subida de archivo con estilo mejorado
                st.markdown(
                    f"""
                    <div style="
                        background-color: white;
                        border-radius: 10px;
                        padding: 20px;
                        margin-bottom: 20px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                        border-top: 4px solid #fac619;
                    ">
                        <h3 style="color: #363856; margin-top: 0;">Subir Archivo de {offer_type_name}</h3>
                        <p style="color: #363856;">
                            Cargue su archivo CSV con las ofertas de {offer_type_name.lower()}
                            para procesamiento y carga a S3.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Texto instructivo
                st.markdown(f"<p style='color: #363856;'>Seleccione el archivo de {offer_type_name.lower()}</p>", unsafe_allow_html=True)

                # File uploader
                uploaded_file = st.file_uploader(
                    "Seleccione el archivo",
                    type=["csv"],
                    key=f"{offer_type_name.lower().replace(' ', '_')}_file_uploader",
                    label_visibility="collapsed"
                )

                if uploaded_file is not None:
                    try:
                        # Vista previa de datos
                        df = pd.read_csv(uploaded_file)

                        # Mostrar éxito al cargar archivo
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #d1fae5;
                                border-left: 4px solid #10b981;
                                border-radius: 4px;
                                padding: 15px;
                                margin: 15px 0;
                            ">
                                <div style="display: flex; align-items: center;">
                                    <div style="margin-right: 10px; font-size: 20px;">✅</div>
                                    <div style="color: #065f46;">
                                        Archivo cargado con éxito. {len(df)} registros encontrados.
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Vista previa de datos con estilo mejorado
                        st.markdown(
                            f"""
                            <div style="
                                background-color: white;
                                border-radius: 10px;
                                padding: 15px;
                                margin-bottom: 20px;
                                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                            ">
                                <h4 style="color: #363856; margin-top: 0;">Vista previa de datos</h4>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Dataframe con los primeros 5 registros
                        st.dataframe(df.head(5), use_container_width=True)

                        # Información del archivo
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Filas", len(df))
                        col2.metric("Columnas", len(df.columns))
                        col3.metric("Tamaño", f"{uploaded_file.size / 1024:.2f} KB")

                        # Botón de procesamiento
                        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
                        if st.button(f"Procesar y Cargar Ofertas {offer_type_name}", key=f"{offer_type_name.lower()}_upload_button", use_container_width=True):
                            success = process_and_upload_csv(uploaded_file, offer_type)
                            if success:
                                st.success(f"¡Archivo {uploaded_file.name} procesado y cargado correctamente!")
                    except Exception as e:
                        st.error(f"Error al procesar el archivo: {str(e)}")

            with col2:
                # Sección de información
                st.markdown(
                    f"""
                    <div style="
                        background-color: white;
                        border-radius: 10px;
                        padding: 20px;
                        margin-bottom: 20px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                        border-top: 4px solid {TIGO_COLORS['primary']};
                        border-left: 4px solid {TIGO_COLORS['primary']};
                    ">
                        <h3 style="
                            color: {TIGO_COLORS['secondary']};
                            margin-top: 0;
                            margin-bottom: 1rem;
                            font-weight: 600;
                            font-size: 1.2rem;
                            padding-bottom: 8px;
                            border-bottom: 2px solid {TIGO_COLORS['primary']};
                        ">Información</h3>
                        <p style="
                            color: {TIGO_COLORS['text_secondary']};
                            margin-bottom: 1rem;
                        ">Formato requerido:</p>
                        <div style="
                            background-color: #f3f4f6;
                            padding: 15px;
                            border-radius: 8px;
                            margin-bottom: 1rem;
                        ">
                            <ul style="
                                color: {TIGO_COLORS['text_secondary']};
                                margin: 0;
                                padding-left: 20px;
                            ">
                                <li>Archivo CSV</li>
                                <li>Tamaño máximo: 50MB</li>
                            </ul>
                        </div>
                        <p style="
                            color: {TIGO_COLORS['text_secondary']};
                            margin-bottom: 1rem;
                            font-weight: 600;
                        ">Proceso:</p>
                        <ol style="
                            color: {TIGO_COLORS['text_secondary']};
                            margin: 0;
                            padding-left: 20px;
                            list-style-type: decimal;
                        ">
                            <li>Suba el archivo</li>
                            <li>Valide los datos en la vista previa</li>
                            <li>Haga clic en "Procesar y Cargar"</li>
                        </ol>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Sección de código de ejemplo
                st.markdown(
                    f"""
                    <div style="
                        background-color: white;
                        border-radius: 10px;
                        padding: 20px;
                        margin-bottom: 20px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                        border-top: 4px solid {TIGO_COLORS['primary']};
                        border-left: 4px solid {TIGO_COLORS['primary']};
                    ">
                        <h3 style="
                            color: {TIGO_COLORS['secondary']};
                            margin-top: 0;
                            margin-bottom: 1rem;
                            font-weight: 600;
                            font-size: 1.2rem;
                            padding-bottom: 8px;
                            border-bottom: 2px solid {TIGO_COLORS['primary']};
                        ">Formato CSV</h3>
                        <pre style="
                            background-color: #f3f4f6;
                            padding: 20px;
                            border-radius: 8px;
                            margin: 0;
                            font-size: 0.9rem;
                            line-height: 1.4;
                            overflow-x: auto;
                        ">
IdCustomer,FirstName,LastName,...
123456,Juan,Pérez,...
789012,María,Rodríguez,...</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Información adicional
            with st.expander("Detalles del proceso de carga", expanded=False):
                # Configuración específica
                config = OFFER_CONFIGURATION.get(offer_type, {})
                folder_name = config.get("folder_name", "")

                st.write("")  # Add some space
                st.markdown("**Bucket:**")
                st.code(BUCKET_NAME, language=None)

                st.markdown("**Ruta:**")
                st.code(folder_name, language=None)

                st.markdown("**Fecha de proceso:**")
                st.text(f"{DAY}/{MONTH}/{YEAR}")

                # Mostrar información adicional específica
                if offer_type == OfferLoadTypes.PAYMENT.value:
                    st.info("Las ofertas de pago incluirán automáticamente el usuario de carga en cada registro.")
                elif offer_type == OfferLoadTypes.REFINANCE.value:
                    st.info("Las ofertas de refinanciamiento incluirán automáticamente el usuario de carga en cada registro.")
                elif offer_type == OfferLoadTypes.MICRO_LOANS_OFFERS.value:
                    st.info("Las ofertas de micro préstamos se procesarán según las reglas de descarte específicas.")
                elif offer_type == OfferLoadTypes.DA_COLLECTION.value:
                    st.info("Los archivos CSV se transformarán a formato JSON antes de subirse a S3.")
