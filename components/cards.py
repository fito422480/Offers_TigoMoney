import streamlit as st
from config.app_config import TIGO_COLORS

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
        ">{title}</h3>
        <div style="color: {TIGO_COLORS['text_secondary']};">
            {content}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def display_metric(value, label, change=None, icon=None):
    """
    Muestra una métrica en una tarjeta estilizada.

    Args:
        value (str): Valor de la métrica.
        label (str): Etiqueta descriptiva.
        change (float, optional): Cambio porcentual.
        icon (str, optional): Icono a mostrar.
    """
    change_html = ""
    if change is not None:
        change_color = TIGO_COLORS['success'] if change >= 0 else TIGO_COLORS['error']
        change_icon = "↑" if change >= 0 else "↓"
        change_html = f"""
        <div style="
            color: {change_color};
            font-size: 0.8rem;
            font-weight: 500;
            margin-top: 5px;
            display: inline-block;
            padding: 2px 8px;
            background-color: {change_color}20;
            border-radius: 999px;
        ">
            {change_icon} {abs(change)}% from previous
        </div>
        """

    icon_html = ""
    if icon:
        icon_html = f"""
        <div style="
            font-size: 24px;
            margin-bottom: 10px;
            color: {TIGO_COLORS['primary']};
        ">
            {icon}
        </div>
        """

    metric_html = f"""
    <div style="
        background: linear-gradient(135deg, {TIGO_COLORS['secondary']} 0%, {TIGO_COLORS['secondary_light']} 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    ">
        {icon_html}
        <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 5px;">{label}</div>
        <div style="font-size: 2rem; font-weight: 700; color: {TIGO_COLORS['primary']};">{value}</div>
        {change_html}
    </div>
    """

    st.markdown(metric_html, unsafe_allow_html=True)

def show_alert(message, alert_type="info"):
    """
    Muestra un mensaje de alerta con estilo.

    Args:
        message (str): Mensaje de alerta.
        alert_type (str): Tipo de alerta ("success", "warning", "error" o "info").
    """
    alert_colors = {
        "success": {"bg": "#d1fae5", "border": "#10b981", "text": "#065f46"},
        "warning": "#fef3c7;#f59e0b;#92400e",
        "error": "#fee2e2;#ef4444;#b91c1c",
        "info": "#e0f2fe;#3b82f6;#1e40af"
    }

    bg_color, border_color, text_color = alert_colors.get(
        alert_type, alert_colors["info"]
    ).split(";")

    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    alert_html = f"""
    <div style="
        background-color: {bg_color};
        border-left: 4px solid {border_color};
        color: {text_color};
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
        display: flex;
        align-items: flex-start;
    ">
        <div style="margin-right: 10px; font-size: 18px;">
            {icons.get(alert_type, icons["info"])}
        </div>
        <div>
            {message}
        </div>
    </div>
    """

    st.markdown(alert_html, unsafe_allow_html=True)

def create_stat_card(title, value, subtitle=None, icon=None, change=None):
    """
    Crea una tarjeta de estadística moderna.

    Args:
        title (str): Título de la métrica.
        value (str): Valor principal a mostrar.
        subtitle (str, optional): Texto secundario.
        icon (str, optional): Código de emoji o icono.
        change (float, optional): Porcentaje de cambio.
    """
    # Determinar el color y el icono de cambio
    change_html = ""
    if change is not None:
        change_color = TIGO_COLORS['success'] if change >= 0 else TIGO_COLORS['error']
        change_icon = "↑" if change >= 0 else "↓"
        change_html = f"""
        <div style="
            color: {change_color};
            font-size: 0.75rem;
            font-weight: 500;
            margin-top: 8px;
            display: inline-block;
            padding: 2px 8px;
            background-color: {change_color}20;
            border-radius: 999px;
        ">
            {change_icon} {abs(change)}% from previous
        </div>
        """

    # HTML para el icono
    icon_html = ""
    if icon:
        icon_html = f"""
        <div style="
            width: 40px;
            height: 40px;
            background-color: {TIGO_COLORS['primary']}20;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            font-size: 24px;
        ">
            {icon}
        </div>
        """

    # HTML para el subtítulo
    subtitle_html = f"""<div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">{subtitle}</div>""" if subtitle else ""

    # HTML completo de la tarjeta
    card_html = f"""
    <div style="
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: transform 0.2s ease;
        border-top: 3px solid {TIGO_COLORS['primary']};
    " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 15px rgba(0, 0, 0, 0.1)';"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 10px rgba(0, 0, 0, 0.05)';">
        {icon_html}
        <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 4px;">{title}</div>
        <div style="font-size: 1.875rem; font-weight: 700; color: {TIGO_COLORS['secondary']};">{value}</div>
        {subtitle_html}
        {change_html}
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)

def info_card(title, content, icon=None, color=None):
    """
    Crea una tarjeta informativa con un estilo específico.

    Args:
        title (str): Título de la tarjeta.
        content (str): Contenido de la tarjeta.
        icon (str, optional): Código de emoji o icono.
        color (str, optional): Color para resaltar la tarjeta.
    """
    if color is None:
        color = TIGO_COLORS['primary']

    icon_html = f"""<div style="font-size: 24px; margin-right: 10px;">{icon}</div>""" if icon else ""

    card_html = f"""
    <div style="
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 4px solid {color};
    ">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            {icon_html}
            <h4 style="margin: 0; color: {TIGO_COLORS['secondary']}; font-weight: 600;">{title}</h4>
        </div>
        <div style="color: {TIGO_COLORS['text_secondary']}; font-size: 0.95rem;">
            {content}
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)
