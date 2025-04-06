import streamlit as st
import os
import sys
import time
from pathlib import Path
from config.app_config import COUNTRY, ENVIRONMENT, LOAD_USER, YEAR, MONTH, DAY, TIGO_COLORS
from pages.dashboard import show_dashboard
from pages.offer_upload import show_offer_upload
from pages.history import show_history
from pages.settings import show_settings

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Page config (primero siempre)
st.set_page_config(
    page_title="Tigo Money - Carga de Ofertas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultar elementos nativos de Streamlit
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    #MainMenu, footer, header { visibility: hidden; }
    .main .block-container {
        max-width: 100%;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Estilos personalizados para la app
sidebar_style = """
<style>
[data-testid="column"]:first-child {
    background-color: #363856;
    padding: 20px;
    border-radius: 10px;
    color: white;
    height: 100vh;
}

div.row-widget.stRadio > div {
    flex-direction: column;
    gap: 8px;
}

div.row-widget.stRadio > div[role="radiogroup"] > label {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 12px 15px;
    color: white !important;
    transition: all 0.2s ease;
    cursor: pointer;
    display: flex;
    align-items: center;
    margin: 2px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

div.row-widget.stRadio > div[role="radiogroup"] > label[aria-checked="true"] {
    background-color: #fac619;
    color: #363856 !important;
    font-weight: 600;
    border-color: #fac619;
}

div.row-widget.stRadio > div[role="radiogroup"] > label[aria-checked="true"] span {
    color: #363856 !important;
}

[data-testid="column"]:nth-child(2) {
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 10px;
}

[data-testid="stAppViewContainer"] {
    background-color: #f0f2f6;
}
section.main {
    background-color: #f0f2f6 !important;
}
</style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

# Session state init
if 'upload_history' not in st.session_state:
    st.session_state.upload_history = []
if 'upload_stats' not in st.session_state:
    st.session_state.upload_stats = {}
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Dashboard"

# Íconos en el menú
menu_icons = {
    "Dashboard": "📊 Dashboard",
    "Carga de Ofertas": "📤 Carga de Ofertas",
    "Historial": "📁 Historial",
    "Configuración": "⚙️ Configuración"
}
reverse_menu = {v: k for k, v in menu_icons.items()}

# Función principal
def main():
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown("""
        <div style="background-color: #363856; padding: 8px 12px; border-radius: 6px; margin-bottom: 10px; display: inline-block;">
            <span style="color: white; font-weight: bold; font-size: 18px;">Tigo</span>
            <span style="color: #fac619; font-weight: bold; font-size: 18px;"> Money</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; opacity: 0.2;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #fac619; margin-bottom: 15px; font-weight: bold;'>Home</h3>", unsafe_allow_html=True)

        menu_display = list(menu_icons.values())
        default_index = menu_display.index(menu_icons[st.session_state.selected_page]) if st.session_state.selected_page in menu_icons else 0

        selected_display = st.radio(
            "Seleccione una opción",
            options=menu_display,
            index=default_index,
            key="navigation_radio",
            label_visibility="collapsed"
        )

        selected_page = reverse_menu[selected_display]

        if selected_page != st.session_state.selected_page:
            with st.spinner('Cargando...'):
                time.sleep(0.6)
            st.session_state.selected_page = selected_page

        st.markdown("<hr style='margin: 20px 0; opacity: 0.2;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #fac619; margin-bottom: 15px; font-weight: bold;'>Usuario</h3>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 12px 15px; 
              color: #363856; margin: 2px 0; border: 1px solid rgba(255, 255, 255, 0.1);">
            Usuario: {LOAD_USER}
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 12px 15px; 
              color: #363856; margin: 2px 0; border: 1px solid rgba(255, 255, 255, 0.1);">
            País: {str(COUNTRY).capitalize()}
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 12px 15px; 
              color: #363856; margin: 2px 0; border: 1px solid rgba(255, 255, 255, 0.1);">
            Ambiente: {str(ENVIRONMENT).upper()}
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 20px 0; opacity: 0.2;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #fac619; margin-bottom: 15px; font-weight: bold;'>Fecha</h3>", unsafe_allow_html=True)

        formatted_date = f"{DAY}/{MONTH}/{YEAR}"
        st.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 12px 15px; 
              color: #363856; margin: 2px 0; border: 1px solid rgba(255, 255, 255, 0.1);">
            Fecha: {formatted_date}
        </div>""", unsafe_allow_html=True)

    with col2:
        if st.session_state.selected_page == "Dashboard":
            show_dashboard()
        elif st.session_state.selected_page == "Carga de Ofertas":
            show_offer_upload()
        elif st.session_state.selected_page == "Historial":
            show_history()
        elif st.session_state.selected_page == "Configuración":
            show_settings()
        else:
            show_dashboard()

if __name__ == "__main__":
    main()
