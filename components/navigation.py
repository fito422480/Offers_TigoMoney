import streamlit as st
import base64
from PIL import Image
import io
from config.app_config import COUNTRY, ENVIRONMENT, LOAD_USER, YEAR, MONTH, DAY

def get_tigo_logo():
    """
    Genera el HTML para el logo de Tigo Money.

    Returns:
        str: HTML para mostrar el logo.
    """
    # Crear logo minimalista de Tigo Money usando capacidades de dibujo
    html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background-color: #363856; color: white; padding: 10px 15px; border-radius: 8px;
                   display: inline-block; font-weight: bold; font-size: 24px; letter-spacing: 1px;">
            Tigo<span style="color: #fac619;"> Money</span>
        </div>
    </div>
    """
    return html

def render_sidebar():
    """
    Renderiza la barra lateral de navegación.

    Returns:
        str: Opción seleccionada.
    """
    with st.sidebar:
        # Logo
        st.markdown(get_tigo_logo(), unsafe_allow_html=True)
        st.markdown("---")

        # Navegación
        st.markdown("### Navegación")
        app_page = st.radio(
            "Seleccione una página:",
            ["Dashboard", "Carga de Ofertas", "Historial", "Configuración"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Información de usuario
        st.markdown("### Usuario")
        st.text(f"Usuario: {LOAD_USER}")
        st.text(f"País: {COUNTRY.capitalize()}")
        st.text(f"Ambiente: {ENVIRONMENT.upper()}")

        st.markdown("---")

        # Fecha
        st.markdown("### Fecha")
        st.text(f"Año: {YEAR}")
        st.text(f"Mes: {MONTH}")
        st.text(f"Día: {DAY}")

        st.markdown("---")

        # Ayuda
        st.markdown("### Ayuda")
        if st.button("Documentación"):
            st.info("La documentación está disponible en la intranet de Tigo Money.")

        if st.button("Soporte"):
            st.info("Para soporte, contacte a su equipo de IT.")

    return app_page

def create_tabs_for_offers():
    """
    Crea pestañas para los diferentes tipos de ofertas.

    Returns:
        tuple: Tupla con las pestañas creadas y sus nombres.
    """
    tab_names = [
        "Batch", "Direct", "Pago", "Refinanciamiento",
        "Micro Préstamos", "DA Collection"
    ]

    tabs = st.tabs(tab_names)

    return tabs, tab_names
