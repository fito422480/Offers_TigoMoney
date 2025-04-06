import streamlit as st
import pandas as pd
from components.cards import render_card, show_alert
from components.navigation import create_tabs_for_offers
from config.app_config import OFFER_CONFIGURATION, BUCKET_NAME, TIGO_COLORS
from config.aws_config import AWS_REGION
from libs.classes import OfferLoadTypes, OfferHeadersMandatory

def show_settings():
    """
    Muestra la página de configuración con el estilo Tigo Money.
    """
    # Título de la página
    st.markdown(f"<h1 style='color: {TIGO_COLORS['text_primary']}; margin-bottom: 1rem;'>Configuración</h1>", unsafe_allow_html=True)

    # Sección de configuración general
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border-top: 4px solid {TIGO_COLORS['primary']};
            border-left: 4px solid {TIGO_COLORS['primary']};
        ">
            <h3 style="
                color: {TIGO_COLORS['secondary']};
                margin-top: 0;
                margin-bottom: 15px;
                font-weight: 600;
                font-size: 1.2rem;
                padding-bottom: 8px;
                border-bottom: 2px solid {TIGO_COLORS['primary']};
            ">Configuración General</h3>
            <p style="
                color: {TIGO_COLORS['text_secondary']};
                margin: 0;
            ">Personalice los parámetros y ajustes del sistema de carga de ofertas.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # El resto del código permanece igual, solo reemplazando BRAND_COLORS con TIGO_COLORS
    # Por ejemplo, donde decía BRAND_COLORS['secondary'], ahora será TIGO_COLORS['secondary']

    # (Continuaría el resto del código original, reemplazando BRAND_COLORS con TIGO_COLORS)
    col1, col2 = st.columns(2)

    with col1:
        # Parámetros generales
        st.markdown("<h4 style='color: #363856;'>Parámetros Generales</h4>", unsafe_allow_html=True)

        environment = st.selectbox(
            "Entorno",
            ["DEV", "QA", "UAT", "PROD"],
            index=0
        )

        country = st.selectbox(
            "País",
            ["Colombia", "Paraguay", "Bolivia", "El Salvador"],
            index=0
        )

        chunk_size = st.number_input(
            "Tamaño de fragmento",
            min_value=100,
            max_value=10000,
            value=5000,
            step=100
        )

    with col2:
        # Configuración de AWS
        st.markdown("<h4 style='color: #363856;'>Configuración de AWS</h4>", unsafe_allow_html=True)

        aws_region = st.selectbox(
            "Región AWS",
            ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "sa-east-1"],
            index=0
        )

        s3_bucket = st.text_input(
            "Bucket S3",
            value=BUCKET_NAME
        )

        timeout = st.number_input(
            "Tiempo de conexión (s)",
            min_value=10,
            max_value=300,
            value=30
        )

    # Cerrar el div de configuración general
    st.markdown("</div>", unsafe_allow_html=True)    

    # El resto del código continúa igual que en tu versión original

    # Mensaje de advertencia
    st.warning("Los cambios en la configuración requieren aprobación del administrador.")

    # Botón para guardar
    col1, col2, col3 = st.columns([2, 2, 1])
    with col3:
        if st.button("Guardar Cambios", use_container_width=True):
            # Simulación de guardado
            st.success("Configuración guardada correctamente. Los cambios estarán disponibles después de la aprobación.")
            st.balloons()

    # Cerrar el div de guardar configuración
    st.markdown("</div>", unsafe_allow_html=True)

    # Configuración avanzada
    with st.expander("Configuración avanzada", expanded=False):
       
        # Controles de configuración avanzada
        col1, col2 = st.columns(2)

        with col1:
            st.slider("Tiempo máximo de procesamiento (minutos)", 1, 60, 15)
            st.slider("Número máximo de reintentos", 1, 10, 3)

        with col2:
            st.checkbox("Habilitar notificaciones por correo electrónico", value=True)
            st.checkbox("Habilitar notificaciones de error en Slack", value=False)

        log_level = st.selectbox(
            "Nivel de log",
            ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=1
        )

        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Guardar logs en S3", value=True)
        with col2:
            st.checkbox("Generar reportes de carga", value=True)

        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Habilitar cargas automáticas", value=False)
        with col2:
            st.time_input("Hora de carga programada", value=None)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("Habilitar cifrado en tránsito", value=True)
        with col2:
            st.checkbox("Habilitar cifrado en reposo", value=True)
        with col3:
            st.checkbox("Exigir autenticación MFA para cambios", value=False)

if __name__ == "__main__":
    show_settings()