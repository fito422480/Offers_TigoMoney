import streamlit as st
from config.app_config import COUNTRY, ENVIRONMENT, LOAD_USER, YEAR, MONTH, DAY

def render_sidebar():
    """
    Renderiza la barra lateral de navegación con funcionalidad mejorada.

    Returns:
        str: Opción seleccionada.
    """
    with st.sidebar:
        # Sección de navegación
        st.markdown("### Navegación")

        # Crear selección de navegación con radio buttons más estilizados
        selected = st.radio(
            "Navegación",
            options=[
                "Dashboard",
                "Carga de Ofertas",
                "Historial",
                "Configuración"
            ],
            index=1,  # Por defecto seleccionar "Carga de Ofertas"
            key="navigation_radio"
        )

        # Información del usuario con estilo simplificado
        st.markdown("---")
        st.markdown("### Usuario")

        # Usar columnas para mostrar la información de usuario
        st.text(f"Usuario: {LOAD_USER}")
        st.text(f"País: {COUNTRY.capitalize()}")
        st.text(f"Ambiente: {ENVIRONMENT.upper()}")

        # Sección de fecha simplificada
        st.markdown("---")
        st.markdown("### Fecha")

        # Mostrar las fechas en formato simple
        st.text(f"Año: {YEAR}")
        st.text(f"Mes: {MONTH}")
        st.text(f"Día: {DAY}")

    return selected

def create_tabs_for_offers():
    """
    Crea pestañas para los diferentes tipos de ofertas con estilo personalizado.

    Returns:
        tuple: Tupla con las pestañas creadas y sus nombres.
    """
    tab_names = [
        "Direct",
        "Batch",
        "Pago",
        "Refinanciamiento",
        "Micro Préstamos",
        "DA Collection"
    ]

    # Añadir CSS personalizado para las pestañas
    st.markdown(
        """
        <style>
        /* Estilos personalizados para pestañas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: #fac619;
            padding: 6px !important;
            border-radius: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            font-weight: 600;
            color: #363856 !important;
            background-color: #fac619;
            border-radius: 8px;
            margin: 0;
            padding: 10px 20px;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background-color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    tabs = st.tabs(tab_names)

    return tabs, tab_names
