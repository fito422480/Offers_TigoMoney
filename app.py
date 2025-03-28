import streamlit as st
import os
import sys

# Asegurarse de que todos los directorios estén en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from components.navigation import render_sidebar
from pages.dashboard import show_dashboard
from pages.offer_upload import show_offer_upload
from pages.history import show_history
from pages.settings import show_settings
from utils.ui_helpers import apply_custom_css, show_logo

# Configuración de la página
st.set_page_config(
    page_title="Tigo Money - Carga de Ofertas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos personalizados
apply_custom_css()

# Inicializar session state
if 'upload_history' not in st.session_state:
    st.session_state.upload_history = []

if 'upload_stats' not in st.session_state:
    st.session_state.upload_stats = {}

def main():
    # Renderizar la barra lateral con logo
    show_logo()

    # Renderizar navegación y obtener página seleccionada
    app_page = render_sidebar()

    # Configurar el fondo blanco
    st.markdown(
        """
        <style>
        .main {
            background-color: white !important;
        }
        .block-container {
            background-color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Mostrar la página correspondiente
    if app_page == "Dashboard":
        show_dashboard()
    elif app_page == "Carga de Ofertas":
        show_offer_upload()
    elif app_page == "Historial":
        show_history()
    elif app_page == "Configuración":
        show_settings()

if __name__ == "__main__":
    main()
