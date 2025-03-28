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
    # CSS para la aplicación completa
    st.markdown(
        f"""
        <style>
        /* Colores principales */
        :root {{
            --primary: {TIGO_COLORS['primary']};
            --primary-light: {TIGO_COLORS['primary_light']};
            --primary-dark: {TIGO_COLORS['primary_dark']};
            --secondary: {TIGO_COLORS['secondary']};
            --secondary-light: {TIGO_COLORS['secondary_light']};
            --secondary-dark: {TIGO_COLORS['secondary_dark']};
            --background: {TIGO_COLORS['background']};
            --text-primary: {TIGO_COLORS['text_primary']};
            --text-secondary: {TIGO_COLORS['text_secondary']};
            --success: {TIGO_COLORS['success']};
            --warning: {TIGO_COLORS['warning']};
            --error: {TIGO_COLORS['error']};
        }}

        /* Estilo global */
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--background);
            color: var(--text-primary);
        }}

        /* Configuración de la página principal */
        .stApp {{
            background-color: var(--background);
        }}

        /* Encabezados */
        h1, h2, h3, h4, h5, h6, .css-10trblm, .css-1vbd788, .css-zt5igj {{
            color: var(--secondary);
            font-weight: 600;
        }}

        /* Texto */
        p, div, .stMarkdown {{
            color: var(--text-primary);
        }}

        /* Fijar el fondo blanco en toda la página */
        [data-testid="stAppViewContainer"] {{
            background-color: white;
        }}

        [data-testid="stHeader"] {{
            background-color: white;
        }}

        /* Sidebar */
        .css-1d391kg, [data-testid="stSidebar"] {{
            background: var(--secondary);
            color: white;
        }}

        /* Elementos del sidebar */
        [data-testid="stSidebar"] h3 {{
            color: white;
        }}

        [data-testid="stSidebar"] .stRadio label {{
            color: white;
        }}

        /* Radio buttons en sidebar */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        /* Textos blancos en sidebar */
        [data-testid="stSidebar"] .stMarkdown p {{
            color: white !important;
        }}

        [data-testid="stSidebar"] .stText p {{
            color: white !important;
        }}

        /* Contenido principal */
        .main .block-container {{
            background-color: white;
            padding: 2rem;
            border-radius: 0.5rem;
        }}

        /* Cards estilo moderno */
        .card {{
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-top: 4px solid var(--primary);
        }}

        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }}

        .card-title {{
            color: var(--secondary);
            font-weight: 600;
            font-size: 1.2rem;
            margin-bottom: 15px;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 8px;
        }}

        /* Botones */
        .stButton > button {{
            background-color: var(--primary) !important;
            color: var(--secondary) !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }}

        .stButton > button:hover {{
            background-color: var(--primary-light) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
        }}

        /* Select boxes */
        .stSelectbox > div > div {{
            background-color: var(--secondary) !important;
            color: white !important;
            border-radius: 8px !important;
        }}

        .stSelectbox > div > div > div {{
            color: white !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: var(--primary) !important;
            border-radius: 8px !important;
            padding: 5px !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            color: var(--secondary) !important;
            font-weight: 600 !important;
            border-radius: 4px !important;
            margin: 0 2px !important;
            padding: 10px 16px !important;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: white !important;
            color: var(--secondary) !important;
        }}

        /* File uploader */
        [data-testid="stFileUploader"] {{
            background-color: white !important;
            border-radius: 10px !important;
            padding: 20px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
        }}

        [data-testid="stFileUploadDropzone"] {{
            background-color: var(--primary) !important;
            border: 2px dashed var(--primary-dark) !important;
            border-radius: 10px !important;
            color: var(--secondary) !important;
        }}

        /* Dataframes */
        [data-testid="stDataFrame"] {{
            background-color: white !important;
            border-radius: 10px !important;
            padding: 10px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
        }}

        [data-testid="stDataFrame"] th {{
            background-color: var(--secondary) !important;
            color: white !important;
            padding: 10px !important;
        }}

        [data-testid="stDataFrame"] td {{
            padding: 8px 10px !important;
        }}

        /* Metrics cards */
        .metric-card {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border-top: 4px solid var(--primary);
            transition: transform 0.3s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }}

        .metric-label {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }}

        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--secondary);
        }}

        .metric-change {{
            margin-top: 0.5rem;
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 500;
        }}

        .metric-change.positive {{
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--success);
        }}

        .metric-change.negative {{
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--error);
        }}

        /* Alertas */
        .success-alert, .warning-alert, .error-alert, .info-alert {{
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            display: flex;
            align-items: center;
        }}

        .success-alert {{
            background-color: #d1fae5;
            border-left: 4px solid var(--success);
            color: #065f46;
        }}

        .warning-alert {{
            background-color: #fef3c7;
            border-left: 4px solid var(--warning);
            color: #92400e;
        }}

        .error-alert {{
            background-color: #fee2e2;
            border-left: 4px solid var(--error);
            color: #b91c1c;
        }}

        .info-alert {{
            background-color: #e0f2fe;
            border-left: 4px solid #3b82f6;
            color: #1e40af;
        }}

        /* Página de bienvenida */
        .welcome-banner {{
            background-color: var(--primary);
            color: var(--secondary);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }}

        .welcome-banner h1 {{
            color: var(--secondary);
            font-size: 2rem;
            margin-bottom: 1rem;
        }}

        .welcome-banner p {{
            color: var(--secondary-dark);
            font-size: 1.1rem;
        }}

        /* Navegación de radio buttons estilizada */
        div.row-widget.stRadio > div {{
            flex-direction: column;
            gap: 0.5rem;
        }}

        div.row-widget.stRadio > div[role="radiogroup"] > label {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: white;
            transition: all 0.2s ease;
            cursor: pointer;
            display: flex;
            align-items: center;
        }}

        div.row-widget.stRadio > div[role="radiogroup"] > label:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {{
            background-color: white;
        }}

        div.row-widget.stRadio > div[role="radiogroup"] > label[aria-checked="true"] {{
            background-color: var(--primary);
            color: var(--secondary);
            font-weight: 600;
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            background-color: var(--secondary);
            color: white !important;
            border-radius: 8px;
            padding: 0.75rem 1rem;
        }}

        .streamlit-expanderContent {{
            background-color: white;
            border-radius: 0 0 8px 8px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}

        /* Código */
        .stCodeBlock {{
            background-color: var(--secondary) !important;
            color: var(--primary) !important;
            border-radius: 8px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_logo():
    """
    Muestra el logo de Tigo Money en la sidebar.
    """
    try:
        # Intenta cargar el logo desde assets
        logo_path = Path('assets/tigo_logo.png')
        if logo_path.exists():
            with open(logo_path, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode()

            st.sidebar.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="data:image/png;base64,{encoded_image}" style="width: 120px;">
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Si no existe el logo, muestra un texto estilizado
            st.sidebar.markdown(
                f"""
                <div style="text-align: center; margin: 20px 0;">
                    <div style="display: inline-block; padding: 10px 15px; background-color: {TIGO_COLORS['secondary']};
                         border-radius: 8px; font-weight: bold; font-size: 24px; letter-spacing: 1px;">
                        Tigo<span style="color: {TIGO_COLORS['primary']}"> Money</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception as e:
        # Si ocurre algún error, muestra sólo el texto
        st.sidebar.markdown(
            f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="display: inline-block; padding: 10px 15px; background-color: {TIGO_COLORS['secondary']};
                     border-radius: 8px; font-weight: bold; font-size: 24px; letter-spacing: 1px;">
                    Tigo<span style="color: {TIGO_COLORS['primary']}"> Money</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
