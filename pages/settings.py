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
    st.markdown("<h1 style='color: #363856; margin-bottom: 1rem;'>Configuración</h1>", unsafe_allow_html=True)

    # Banner de sección
    st.markdown(
        f"""
        <div style="
            background-color: {TIGO_COLORS['primary']};
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h2 style="color: {TIGO_COLORS['secondary']}; margin: 0;">Configuración del Sistema</h2>
            <p style="color: {TIGO_COLORS['secondary']}; margin-top: 5px;">
                Personalice los parámetros y ajustes del sistema de carga de ofertas.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sección de configuración general
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        ">
            <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0;">Configuración General</h3>
        """,
        unsafe_allow_html=True
    )

    # Configuraciones generales con dos columnas
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

    # Configuración de tipos de ofertas
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin: 20px 0;
        ">
            <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0;">Configuración de Tipos de Ofertas</h3>
        """,
        unsafe_allow_html=True
    )

    # Crear pestañas para configuración de tipos de ofertas
    tabs, tab_names = create_tabs_for_offers()

    # Mostrar configuración para cada tipo de oferta
    for i, tab in enumerate(tabs):
        offer_type_name = tab_names[i]
        offer_type_value = next(
            (t.value for t in OfferLoadTypes if t.name.upper() == offer_type_name.upper().replace(" ", "_")),
            list(OfferLoadTypes)[i].value
        )
        config = OFFER_CONFIGURATION.get(offer_type_value, {})

        with tab:
            # Columnas para organizar la información
            col1, col2 = st.columns(2)

            with col1:
                # Información de configuración
                st.markdown(f"<h4 style='color: #363856;'>Configuración para {offer_type_name}</h4>", unsafe_allow_html=True)

                # Ruta en S3
                st.markdown("<p style='color: #4b4d6d; font-weight: 600; margin-bottom: 5px;'>Ruta en S3:</p>", unsafe_allow_html=True)
                st.code(config.get('folder_name', 'No configurado'), language="bash")

                # Nombre de archivo
                st.markdown("<p style='color: #4b4d6d; font-weight: 600; margin-bottom: 5px;'>Nombre de archivo:</p>", unsafe_allow_html=True)
                st.code(config.get('file_name', 'No configurado'), language="bash")

                # Tamaño de fragmento
                if 'chunk_size' in config:
                    st.markdown("<p style='color: #4b4d6d; font-weight: 600; margin-bottom: 5px;'>Tamaño de fragmento:</p>", unsafe_allow_html=True)
                    st.code(str(config['chunk_size']), language="python")

                # Regla de descarte
                if 'discard_rule' in config and config['discard_rule'] is not None:
                    st.markdown("<p style='color: #4b4d6d; font-weight: 600; margin-bottom: 5px;'>Regla de descarte:</p>", unsafe_allow_html=True)
                    st.code(config['discard_rule'].__name__, language="python")

            with col2:
                # Campos obligatorios
                st.markdown("<h4 style='color: #363856;'>Campos obligatorios</h4>", unsafe_allow_html=True)

                # Obtener encabezados obligatorios
                header_format = config.get('header_format')

                if header_format and header_format.value:
                    # Crear dataframe para mostrar los campos
                    headers_df = pd.DataFrame({"Campo": header_format.value})
                    st.dataframe(headers_df, hide_index=True, use_container_width=True)
                else:
                    st.info("No hay campos obligatorios definidos para este tipo.")

                # Opciones adicionales
                if 'options' in config:
                    st.markdown("<h4 style='color: #363856;'>Opciones adicionales</h4>", unsafe_allow_html=True)

                    # Flag de fin de carga
                    if 'endupload_flag' in config['options']:
                        st.markdown(
                            f"""
                            <p style='color: #4b4d6d;'>
                                <span style='font-weight: 600;'>Flag de fin de carga:</span>
                                <code style='background-color: #edf2f7; padding: 2px 4px; border-radius: 4px;'>
                                    {config['options']['endupload_flag']}
                                </code>
                            </p>
                            """,
                            unsafe_allow_html=True
                        )

                    # Campos adicionales
                    if 'additional_fields' in config['options']:
                        st.markdown("<p style='color: #4b4d6d; font-weight: 600;'>Campos adicionales:</p>", unsafe_allow_html=True)

                        for field, value in config['options']['additional_fields'].items():
                            st.markdown(
                                f"""
                                <p style='color: #4b4d6d; margin-left: 15px;'>
                                    • <code style='background-color: #edf2f7; padding: 2px 4px; border-radius: 4px;'>{field}</code>:
                                    <code style='background-color: #edf2f7; padding: 2px 4px; border-radius: 4px;'>{value}</code>
                                </p>
                                """,
                                unsafe_allow_html=True
                            )

                    # Función de transformación
                    if 'transform_function' in config['options']:
                        st.markdown(
                            f"""
                            <p style='color: #4b4d6d;'>
                                <span style='font-weight: 600;'>Función de transformación:</span>
                                <code style='background-color: #edf2f7; padding: 2px 4px; border-radius: 4px;'>
                                    {config['options']['transform_function'].__name__}
                                </code>
                            </p>
                            """,
                            unsafe_allow_html=True
                        )

    # Cerrar el div de configuración de tipos de ofertas
    st.markdown("</div>", unsafe_allow_html=True)

    # Sección para guardar configuración
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin: 20px 0;
        ">
            <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0;">Guardar configuración</h3>
        """,
        unsafe_allow_html=True
    )

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
        # Sección de procesamiento
        st.markdown("<h4 style='color: #363856;'>Configuración de procesamiento</h4>", unsafe_allow_html=True)

        # Controles de configuración avanzada
        col1, col2 = st.columns(2)

        with col1:
            st.slider("Tiempo máximo de procesamiento (minutos)", 1, 60, 15)
            st.slider("Número máximo de reintentos", 1, 10, 3)

        with col2:
            st.checkbox("Habilitar notificaciones por correo electrónico", value=True)
            st.checkbox("Habilitar notificaciones de error en Slack", value=False)

        # Sección de logs
        st.markdown("<h4 style='color: #363856;'>Configuración de registros (logs)</h4>", unsafe_allow_html=True)

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

        # Sección de tareas programadas
        st.markdown("<h4 style='color: #363856;'>Tareas programadas</h4>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Habilitar cargas automáticas", value=False)
        with col2:
            st.time_input("Hora de carga programada", value=None)

        # Sección de seguridad
        st.markdown("<h4 style='color: #363856;'>Configuración de seguridad</h4>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("Habilitar cifrado en tránsito", value=True)
        with col2:
            st.checkbox("Habilitar cifrado en reposo", value=True)
        with col3:
            st.checkbox("Exigir autenticación MFA para cambios", value=False)
