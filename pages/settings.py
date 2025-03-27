import streamlit as st
import pandas as pd
from components.cards import render_card, show_alert
from components.navigation import create_tabs_for_offers
from config.app_config import OFFER_CONFIGURATION, BUCKET_NAME
from config.aws_config import AWS_REGION
from libs.classes import OfferLoadTypes, OfferHeadersMandatory

def show_settings():
    """
    Muestra la página de configuración.
    """
    st.markdown("# Configuración")

    # Configuration sections
    st.markdown("## Configuración General")

    col1, col2 = st.columns(2)

    with col1:
        render_card(
            "Parámetros Generales",
            """
            <form>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">Entorno</label>
                    <select style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                        <option>DEV</option>
                        <option>UAT</option>
                        <option>PROD</option>
                    </select>
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">País</label>
                    <select style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                        <option>Colombia</option>
                        <option>Paraguay</option>
                        <option>Bolivia</option>
                        <option>El Salvador</option>
                    </select>
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">Tamaño de fragmento</label>
                    <input type="number" value="5000" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                </div>
            </form>
            """
        )

    with col2:
        render_card(
            "Configuración de AWS",
            f"""
            <form>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">Región AWS</label>
                    <select style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                        <option>{AWS_REGION}</option>
                        <option>us-east-2</option>
                        <option>us-west-1</option>
                        <option>us-west-2</option>
                        <option>sa-east-1</option>
                    </select>
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">Bucket S3</label>
                    <input type="text" value="{BUCKET_NAME}" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">Umbral de conexión (s)</label>
                    <input type="number" value="30" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                </div>
            </form>
            """
        )

    st.markdown("## Configuración de Tipos de Ofertas")

    # Create tabs for offer type configurations
    config_tabs, tab_names = create_tabs_for_offers()

    # Display configuration for each offer type
    for i, tab in enumerate(config_tabs):
        offer_type = list(OfferLoadTypes)[i].value
        config = OFFER_CONFIGURATION[offer_type]

        with tab:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### Configuración para {tab_names[i]}")

                # Display current configuration
                st.markdown("**Ruta en S3:**")
                st.code(config['folder_name'])

                st.markdown("**Nombre de archivo:**")
                st.code(config['file_name'])

                if 'chunk_size' in config:
                    st.markdown("**Tamaño de fragmento:**")
                    st.code(str(config['chunk_size']))

                if 'discard_rule' in config and config['discard_rule'] is not None:
                    st.markdown("**Regla de descarte:**")
                    st.code(config['discard_rule'].__name__)

            with col2:
                st.markdown("### Campos obligatorios")

                # Get the mandatory headers for this type
                header_format = config['header_format']

                if header_format.value:
                    for header in header_format.value:
                        st.markdown(f"- {header}")
                else:
                    st.markdown("No hay campos obligatorios definidos para este tipo.")

                # Display other options
                if 'options' in config:
                    st.markdown("### Opciones adicionales")

                    if 'endupload_flag' in config['options']:
                        st.markdown(f"**Flag de fin de carga:** `{config['options']['endupload_flag']}`")

                    if 'additional_fields' in config['options']:
                        st.markdown("**Campos adicionales:**")
                        for field, value in config['options']['additional_fields'].items():
                            st.markdown(f"- {field}: `{value}`")

                    if 'transform_function' in config['options']:
                        st.markdown(f"**Función de transformación:** `{config['options']['transform_function'].__name__}`")

    # Save button (no real functionality in this demo)
    st.markdown("## Guardar configuración")

    st.warning("Los cambios en la configuración requieren aprobación del administrador.")

    if st.button("Guardar Cambios"):
        show_alert("Configuración guardada correctamente. Los cambios estarán disponibles después de la aprobación.", "success")
        st.balloons()

    # Configuración avanzada
    st.markdown("## Configuración avanzada")
    with st.expander("Opciones avanzadas"):
        st.markdown("### Configuración de procesamiento")

        st.slider("Tiempo máximo de procesamiento (minutos)", 1, 60, 15)
        st.slider("Número máximo de reintentos", 1, 10, 3)
        st.checkbox("Habilitar notificaciones por correo electrónico", value=True)
        st.checkbox("Habilitar notificaciones de error en Slack", value=False)

        st.markdown("### Configuración de registros (logs)")

        st.selectbox("Nivel de log", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], index=1)
        st.checkbox("Guardar logs en S3", value=True)
        st.checkbox("Generar reportes de carga", value=True)

        st.markdown("### Tareas programadas")

        st.checkbox("Habilitar cargas automáticas", value=False)
        st.time_input("Hora de carga programada", value=None)

        st.markdown("### Configuración de seguridad")

        st.checkbox("Habilitar cifrado en tránsito", value=True)
        st.checkbox("Habilitar cifrado en reposo", value=True)
        st.checkbox("Exigir autenticación MFA para cambios", value=False)
