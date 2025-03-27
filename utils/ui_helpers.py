import streamlit as st
import base64
from pathlib import Path
import os

def apply_custom_css():
    """
    Aplica los estilos CSS personalizados a la aplicación.
    """
    # Intentar leer el archivo CSS local primero
    css_file = Path(__file__).parent.parent / "assets" / "css" / "styles.css"

    if css_file.exists():
        with open(css_file, "r") as f:
            css = f.read()
    else:
        # CSS de respaldo si no se encuentra el archivo
        css = """
        /* Main colors */
        :root {
            --tigo-yellow: #fac619;
            --tigo-blue: #363856;
            --tigo-light-blue: #4a4c6a;
            --tigo-light-yellow: #fad54d;
            --background-color: #f8f9fa;
            --card-background: #ffffff;
        }

        /* Global styling */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: var(--background-color);
            color: #333;
        }

        /* Header styling */
        .css-1q60bmi, .css-10trblm, .stHeadingContainer h1, .stHeadingContainer h2, .stHeadingContainer h3 {
            color: var(--tigo-blue) !important;
            font-weight: 600 !important;
        }

        /* Custom cards */
        .card {
            background-color: var(--card-background);
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .card-title {
            color: var(--tigo-blue);
            font-weight: 600;
            font-size: 1.2rem;
            margin-bottom: 15px;
            border-bottom: 2px solid var(--tigo-yellow);
            padding-bottom: 8px;
        }

        /* Button styling */
        .stButton button {
            background-color: var(--tigo-blue) !important;
            color: white !important;
            border-radius: 5px !important;
            border: none !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
            transition: background-color 0.3s ease !important;
        }

        .stButton button:hover {
            background-color: var(--tigo-light-blue) !important;
        }

        /* Yellow button variant */
        .yellow-btn button {
            background-color: var(--tigo-yellow) !important;
            color: var(--tigo-blue) !important;
        }

        .yellow-btn button:hover {
            background-color: var(--tigo-light-yellow) !important;
        }

        /* Success alert */
        .success-alert {
            padding: 15px;
            border-radius: 5px;
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            margin: 10px 0;
        }

        /* Warning alert */
        .warning-alert {
            padding: 15px;
            border-radius: 5px;
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
            margin: 10px 0;
        }

        /* Error alert */
        .error-alert {
            padding: 15px;
            border-radius: 5px;
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            margin: 10px 0;
        }

        /* Metric card */
        .metric-card {
            text-align: center;
            padding: 20px 10px;
            border-radius: 8px;
            background-color: var(--tigo-blue);
            color: white;
        }

        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: var(--tigo-yellow);
        }

        .metric-label {
            font-size: 14px;
            opacity: 0.9;
        }
        """

    # Aplicar CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def get_img_as_base64(file):
    """
    Convierte una imagen a formato base64.

    Args:
        file (str): Ruta de la imagen.

    Returns:
        str: Imagen en formato base64.
    """
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_color(hex_color):
    """
    Establece un color de fondo para la aplicación.

    Args:
        hex_color (str): Color en formato hexadecimal.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {hex_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def make_grid(cols, rows):
    """
    Crea una cuadrícula personalizada.

    Args:
        cols (int): Número de columnas.
        rows (int): Número de filas.

    Returns:
        list: Lista de contenedores para cada celda.
    """
    grid = [0] * cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def create_link_button(link, label, icon=None):
    """
    Crea un botón con un enlace.

    Args:
        link (str): URL del enlace.
        label (str): Etiqueta del botón.
        icon (str): Código del icono (opcional).
    """
    icon_html = f'<i class="{icon}"></i> ' if icon else ''
    button_html = f'''
    <a href="{link}" target="_blank" style="text-decoration: none;">
        <div style="
            background-color: #363856;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-align: center;
            margin: 10px 0px;
            font-weight: 500;
            display: inline-block;
        ">
            {icon_html}{label}
        </div>
    </a>
    '''
    st.markdown(button_html, unsafe_allow_html=True)
