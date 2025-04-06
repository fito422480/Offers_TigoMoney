import streamlit as st
import base64
from pathlib import Path
import os

# Colores Tigo Money
TIGO_COLORS = {
    "primary": "#fac619",        # Amarillo Tigo
    "primary_light": "#fdd44f",  # Amarillo claro
    "primary_dark": "#e6a800",   # Amarillo oscuro
    "secondary": "#363856",      # Azul oscuro
    "secondary_light": "#4b4d6d", # Azul claro
    "secondary_dark": "#21222f",  # Azul más oscuro
    "background": "#FFFFFF",     # Fondo BLANCO
    "text_primary": "#363856",   # Texto principal (azul)
    "text_secondary": "#4b4d6d",  # Texto secundario
    "success": "#10B981",        # Verde éxito
    "warning": "#fac619",        # Amarillo advertencia
    "error": "#EF4444",          # Rojo error
}

def apply_custom_css():
    """
    Aplica los estilos CSS personalizados a la aplicación.
    """
    # Agregar CSS para ocultar específicamente los items duplicados en el sidebar
    hide_duplicate_menu = """
    <style>
    /* Ocultar los elementos de navegación duplicados */
    [data-testid="stSidebar"] > div:first-child > div:first-child > div:first-child > div > div:first-child {
        display: none;
    }
    
    /* Ocultar los links de navegación automáticos */
    [data-testid="stSidebar"] a[href="#app"], 
    [data-testid="stSidebar"] a[href="#dashboard"],
    [data-testid="stSidebar"] a[href="#history"],
    [data-testid="stSidebar"] a[href="#offer-upload"],
    [data-testid="stSidebar"] a[href="#settings"] {
        display: none !important;
    }
    
    /* Ocultar los elementos con clase css-16idsys p */
    [data-testid="stSidebar"] .css-16idsys p {
        display: none;
    }
    
    /* También intentar usar el selector específico para la lista de navegación */
    [data-testid="stSidebarNavContainer"] {
        display: none !important;
    }
    
    /* Ocultar cualquier contenedor div que pudiera estar envolviendo estos elementos */
    [data-testid="stSidebar"] > div > div > div:nth-child(1) {
        display: none;
    }
    </style>
    """
    st.markdown(hide_duplicate_menu, unsafe_allow_html=True)
    

def show_logo():
    """
    Muestra el logo de Tigo Money en la sidebar.
    """
    with st.sidebar:
        # Logo Tigo Money con colores de la marca
        try:
            # Intenta cargar el logo TM.png desde la nueva ubicación
            logo_path = Path(__file__).parent.parent / 'assets' / 'img' / 'tm.png'
            
            if logo_path.exists():
                with open(logo_path, "rb") as img_file:
                    encoded_image = base64.b64encode(img_file.read()).decode()
            else:
                # Si no existe el logo, muestra el texto estilizado
                logo_html = """
                <div style="margin: 10px 0;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="display: inline-block; padding: 6px 10px; background-color: rgb(54, 56, 86); border-radius: 4px; font-weight: bold; font-size: 16px; letter-spacing: 0.3px;">
                            Tigo<span style="color: rgb(250, 198, 25);"> Money</span>
                        </div>
                    </div>
                </div>
                """
                st.markdown(logo_html, unsafe_allow_html=True)
        except Exception as e:
            # Si ocurre algún error, muestra el texto estilizado
            logo_html = """
            <div style="margin: 10px 0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="display: inline-block; padding: 6px 10px; background-color: rgb(54, 56, 86); border-radius: 4px; font-weight: bold; font-size: 16px; letter-spacing: 0.3px;">
                        Tigo<span style="color: rgb(250, 198, 25);"> Money</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(logo_html, unsafe_allow_html=True)

def welcome_banner(title, description):
    """
    Muestra un banner de bienvenida.

    Args:
        title (str): Título del banner.
        description (str): Descripción o mensaje.
    """
    st.markdown(
        f"""
        <div style="
            background-color: {TIGO_COLORS['primary']};
            border-radius: 10px;
            padding: 30px 20px;
            margin-bottom: 20px;
            text-align: center;
        ">
            <h1 style="color: {TIGO_COLORS['secondary']}; margin: 0; font-size: 28px;">{title}</h1>
            <p style="color: {TIGO_COLORS['secondary']}; margin-top: 10px; font-size: 16px;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_card(title, content):
    """
    Renderiza una tarjeta personalizada con título y contenido.

    Args:
        title (str): Título de la tarjeta.
        content (str): Contenido HTML de la tarjeta.
    """
    card_html = f"""
    <div style="
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-top: 4px solid {TIGO_COLORS['primary']};
    ">
        <div style="
            color: {TIGO_COLORS['secondary']};
            font-weight: 600;
            font-size: 18px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid {TIGO_COLORS['primary']};
        ">{title}</div>
        <div style="color: {TIGO_COLORS['text_primary']};">
            {content}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def display_metric(value, label, change=None, icon=None):
    """
    Muestra una métrica con estilo de tarjeta.

    Args:
        value (str): Valor de la métrica.
        label (str): Etiqueta descriptiva.
        change (float, optional): Cambio porcentual.
        icon (str, optional): Icono a mostrar.
    """
    change_html = ""
    if change is not None:
        change_class = "positive" if change >= 0 else "negative"
        change_icon = "↑" if change >= 0 else "↓"
        change_html = f"""
        <div class="metric-change {change_class}">
            {change_icon} {abs(change)}% from previous
        </div>
        """

    icon_html = ""
    if icon:
        icon_html = f"""
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: {TIGO_COLORS['primary']};">
            {icon}
        </div>
        """

    st.markdown(
        f"""
        <div class="metric-card">
            {icon_html}
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {change_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def show_alert(message, alert_type="info"):
    """
    Muestra un mensaje de alerta con estilo.

    Args:
        message (str): Mensaje de alerta.
        alert_type (str): Tipo de alerta ("success", "warning", "error" o "info").
    """
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    st.markdown(
        f"""
        <div class="{alert_type}-alert">
            <div style="margin-right: 10px; font-size: 20px;">{icons[alert_type]}</div>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_section_header(title, description=None, icon=None):
    """
    Crea un encabezado de sección con estilo.

    Args:
        title (str): Título de la sección.
        description (str, optional): Descripción de la sección.
        icon (str, optional): Icono para la sección.
    """
    icon_html = f'<div style="margin-right: 10px; font-size: 24px;">{icon}</div>' if icon else ''

    description_html = ""
    if description:
        description_html = f'<p style="margin: 0; color: {TIGO_COLORS["text_secondary"]};">{description}</p>'

    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border-left: 4px solid {TIGO_COLORS["primary"]};
        ">
            <div style="display: flex; align-items: center;">
                {icon_html}
                <div>
                    <h2 style="margin: 0; color: {TIGO_COLORS["secondary"]};">{title}</h2>
                    {description_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
