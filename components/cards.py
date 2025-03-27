import streamlit as st

def render_card(title, content):
    """
    Renderiza una tarjeta personalizada con título y contenido.

    Args:
        title (str): Título de la tarjeta.
        content (str): Contenido HTML de la tarjeta.
    """
    card_html = f"""
    <div class="card">
        <div class="card-title">{title}</div>
        {content}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def display_metric(value, label, column):
    """
    Muestra una métrica en una tarjeta con estilo.

    Args:
        value (str): Valor de la métrica.
        label (str): Etiqueta descriptiva.
        column (streamlit.delta_generator.DeltaGenerator): Columna de Streamlit.
    """
    with column:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

def show_alert(message, alert_type="info"):
    """
    Muestra un mensaje de alerta con estilo.

    Args:
        message (str): Mensaje de alerta.
        alert_type (str): Tipo de alerta ("success", "warning", "error" o "info").
    """
    if alert_type == "success":
        st.markdown(f'<div class="success-alert">{message}</div>', unsafe_allow_html=True)
    elif alert_type == "warning":
        st.markdown(f'<div class="warning-alert">{message}</div>', unsafe_allow_html=True)
    elif alert_type == "error":
        st.markdown(f'<div class="error-alert">{message}</div>', unsafe_allow_html=True)
    else:
        st.info(message)

def welcome_banner(title, description):
    """
    Muestra un banner de bienvenida.

    Args:
        title (str): Título del banner.
        description (str): Descripción o mensaje.
    """
    st.markdown(f"""
    <div class="welcome-banner">
        <h2>{title}</h2>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)
