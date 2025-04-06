import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from components.cards import render_card
from utils.ui_helpers import display_metric, create_section_header
from config.app_config import BUCKET_NAME, TIGO_COLORS
from pathlib import Path

def show_dashboard():
    """
    Muestra el dashboard con estadísticas y gráficos.
    """
    # Inicializar session_state si no existe
    if 'upload_history' not in st.session_state:
        st.session_state.upload_history = []

    if 'upload_stats' not in st.session_state:
        st.session_state.upload_stats = {}

    # Título del dashboard
    st.markdown(
        """
        <div style="padding: 2rem 0 1rem 0;">
            <h1 style="color: #363856; font-size: 2rem; font-weight: 600; margin: 0; padding: 0;">
                Dashboard de Carga de Ofertas
            </h1>
            <p style="color: #4b4d6d; margin: 0.5rem 0 0 0; font-size: 1rem;">
                Visualiza y controla tus operaciones de carga de ofertas!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Métricas principales
    st.markdown("<h2 style='color: #363856; margin-bottom: 1rem;'>Métricas principales</h2>", unsafe_allow_html=True)

    # Crear una fila de métricas
    col1, col2, col3, col4 = st.columns(4)

    # Calcular métricas
    total_uploads = len(st.session_state.upload_history)
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_uploads = sum(1 for item in st.session_state.upload_history 
                      if pd.to_datetime(item['timestamp']).strftime("%Y-%m-%d") == today)

    # Mostrar métricas en estilo de tarjetas
    with col1:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {TIGO_COLORS['secondary']} 0%, {TIGO_COLORS['secondary_light']} 100%);
                border-radius: 10px;
                padding: 1.5rem;
                color: white;
                height: 100%;
            ">
                <div style="font-size: 0.875rem; opacity: 0.8; margin-bottom: 0.5rem;">Cargas totales</div>
                <div style="font-size: 2rem; font-weight: 700; color: {TIGO_COLORS['primary']};">{total_uploads}</div>
                <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">Todas las ofertas</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {TIGO_COLORS['secondary']} 0%, {TIGO_COLORS['secondary_light']} 100%);
                border-radius: 10px;
                padding: 1.5rem;
                color: white;
                height: 100%;
            ">
                <div style="font-size: 0.875rem; opacity: 0.8; margin-bottom: 0.5rem;">Cargas de hoy</div>
                <div style="font-size: 2rem; font-weight: 700; color: {TIGO_COLORS['primary']};">{today_uploads}</div>
                <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">{today}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {TIGO_COLORS['secondary']} 0%, {TIGO_COLORS['secondary_light']} 100%);
                border-radius: 10px;
                padding: 1.5rem;
                color: white;
                height: 100%;
            ">
                <div style="font-size: 0.875rem; opacity: 0.8; margin-bottom: 0.5rem;">Tasa de éxito</div>
                <div style="font-size: 2rem; font-weight: 700; color: {TIGO_COLORS['primary']};">98.7%</div>
                <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem; color: #10B981;">↑ 1.2% vs. anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {TIGO_COLORS['secondary']} 0%, {TIGO_COLORS['secondary_light']} 100%);
                border-radius: 10px;
                padding: 1.5rem;
                color: white;
                height: 100%;
            ">
                <div style="font-size: 0.875rem; opacity: 0.8; margin-bottom: 0.5rem;">Tiempo promedio</div>
                <div style="font-size: 2rem; font-weight: 700; color: {TIGO_COLORS['primary']};">0.6s</div>
                <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem; color: #EF4444;">↓ 0.2s vs. anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Separador
    st.markdown("<hr style='margin: 2rem 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # Actividad reciente y distribución
    col1, col2 = st.columns([3, 2])

    with col1:
        # Sección de actividad reciente
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 1rem;
                border-top: 4px solid {TIGO_COLORS['primary']};
                border-left: 4px solid {TIGO_COLORS['primary']};
            ">
                <h3 style="
                    color: {TIGO_COLORS['secondary']};
                    margin-top: 0;
                    margin-bottom: 1rem;
                    font-weight: 600;
                    font-size: 1.2rem;
                    padding-bottom: 8px;
                    border-bottom: 2px solid {TIGO_COLORS['primary']};
                ">Actividad Reciente</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.upload_history:
            # Mostrar las últimas 5 cargas
            recent_uploads = st.session_state.upload_history[-5:][::-1]
            for upload in recent_uploads:
                timestamp = pd.to_datetime(upload['timestamp'])
                st.markdown(
                    f"""
                    <div style="
                        background-color: white;
                        border-radius: 8px;
                        padding: 1rem;
                        margin-bottom: 0.75rem;
                        border-left: 4px solid {TIGO_COLORS['primary']};
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: 500; color: {TIGO_COLORS['secondary']};">{upload['type']}</div>
                                <div style="font-size: 0.875rem; color: {TIGO_COLORS['text_secondary']};">
                                    {timestamp.strftime('%d/%m/%Y %H:%M')}
                                </div>
                            </div>
                            <div style="font-size: 0.875rem; color: {TIGO_COLORS['success'] if upload['status'] == 'success' else TIGO_COLORS['error']};">
                                {upload['status'].capitalize()}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                f"""
                <div style="
                    background-color: white;
                    border-radius: 8px;
                    padding: 1rem;
                    margin-bottom: 0.75rem;
                    border-left: 4px solid {TIGO_COLORS['primary']};
                ">
                    <div style="font-size: 0.875rem; color: {TIGO_COLORS['text_secondary']};">
                        No hay actividad reciente para mostrar.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        # Sección de distribución de cargas
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 1rem;
                border-top: 4px solid {TIGO_COLORS['primary']};
                border-left: 4px solid {TIGO_COLORS['primary']};
            ">
                <h3 style="
                    color: {TIGO_COLORS['secondary']};
                    margin-top: 0;
                    margin-bottom: 1rem;
                    font-weight: 600;
                    font-size: 1.2rem;
                    padding-bottom: 8px;
                    border-bottom: 2px solid {TIGO_COLORS['primary']};
                ">Distribución de Cargas</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.upload_history:
            # Crear gráfico de distribución
            history_df = pd.DataFrame(st.session_state.upload_history)
            
            # Contar por tipo de carga
            type_counts = history_df['type'].value_counts()
            
            # Crear gráfico de barras
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=type_counts.index,
                y=type_counts.values,
                marker_color=[TIGO_COLORS['primary'], TIGO_COLORS['secondary'], TIGO_COLORS['primary_light'], TIGO_COLORS['secondary_light']][:len(type_counts)]
            ))

            fig.update_layout(
                title="",
                xaxis_title="Tipo de Carga",
                yaxis_title="Número de Cargas",
                template="plotly_white",
                margin=dict(t=0, b=50, l=50, r=20),
                height=300
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            # Datos de ejemplo
            sample_counts = {
                "Batch": 12,
                "Direct": 8,
                "Pago": 5,
                "Refinanciamiento": 3
            }

            fig = px.bar(
                x=list(sample_counts.keys()),
                y=list(sample_counts.values()),
                color_discrete_sequence=[TIGO_COLORS['primary'], TIGO_COLORS['secondary'],
                                        TIGO_COLORS['primary_light'], TIGO_COLORS['secondary_light']]
            )

            fig.update_layout(
                title="",
                xaxis_title="Tipo de Carga",
                yaxis_title="Número de Cargas",
                template="plotly_white",
                margin=dict(t=0, b=50, l=50, r=20),
                height=300
            )

            st.caption("Vista previa de ejemplo:")
            st.plotly_chart(fig, use_container_width=True)

    # Historial de cargas
    st.markdown(
        f"""
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
                margin-bottom: 1rem;
                font-weight: 600;
                font-size: 1.2rem;
                padding-bottom: 8px;
                border-bottom: 2px solid {TIGO_COLORS['primary']};
            ">Historial de Cargas</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.upload_history:
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                border-top: 4px solid {TIGO_COLORS['primary']};
                border-left: 4px solid {TIGO_COLORS['primary']};
            ">
                <div style="text-align: center;">
                    <h4 style="
                        color: {TIGO_COLORS['secondary']};
                        margin: 0 0 1rem 0;
                        font-weight: 600;
                    ">No hay historial disponible</h4>
                    <p style="
                        color: {TIGO_COLORS['text_secondary']};
                        margin: 0;
                    ">No se han encontrado cargas anteriores. El historial se mostrará aquí una vez que realice cargas de archivos.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Crear un dataframe para mostrar el historial
        history_df = pd.DataFrame(st.session_state.upload_history)
        history_df['filename'] = history_df['filename'].apply(lambda x: Path(x).name)
        history_df['date'] = pd.to_datetime(history_df['timestamp']).dt.strftime('%d/%m/%Y')

        # Mostrar historial de cargas recientes
        st.dataframe(
            history_df[['date', 'filename', 'bucket', 'type', 'status']],
            column_config={
                "date": "Fecha",
                "filename": "Archivo",
                "bucket": "Bucket",
                "type": "Tipo",
                "status": "Estado"
            },
            hide_index=True,
            use_container_width=True
        )

    # Tendencia semanal
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            border-top: 4px solid {TIGO_COLORS['primary']};
            border-left: 4px solid {TIGO_COLORS['primary']};
        ">
            <h3 style="
                color: {TIGO_COLORS['secondary']};
                margin-top: 0;
                margin-bottom: 1rem;
                font-weight: 600;
                font-size: 1.2rem;
                padding-bottom: 8px;
                border-bottom: 2px solid {TIGO_COLORS['primary']};
            ">Tendencia Semanal</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Datos para gráfico de tendencia
    if st.session_state.upload_history:
        # Extraer fecha
        history_df = pd.DataFrame(st.session_state.upload_history)
        history_df['date'] = pd.to_datetime(history_df['timestamp']).dt.date

        # Contar cargas por fecha
        uploads_by_date = history_df.groupby('date').size().reset_index(name='count')

        # Llenar fechas faltantes con ceros
        dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).date() for i in range(6, -1, -1)]
        all_dates = pd.DataFrame({'date': dates})
        uploads_by_date = pd.merge(all_dates, uploads_by_date, on='date', how='left').fillna(0)

        # Crear gráfico de línea
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=uploads_by_date['date'],
            y=uploads_by_date['count'],
            mode='lines+markers',
            line=dict(color=TIGO_COLORS['secondary'], width=3),
            marker=dict(color=TIGO_COLORS['primary'], size=8),
            fill='tozeroy',
            fillcolor=f'rgba{tuple(int(TIGO_COLORS["secondary"][i:i+2], 16) for i in (1, 3, 5)) + (0.1,)}'
        ))

        fig.update_layout(
            title="",
            xaxis_title="Fecha",
            yaxis_title="Número de Cargas",
            template="plotly_white",
            margin=dict(t=0, b=50, l=50, r=20),
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        # Datos de ejemplo
        dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).date() for i in range(6, -1, -1)]
        counts = [3, 5, 4, 7, 2, 0, 1]

        # Crear dataframe de ejemplo
        example_df = pd.DataFrame({'date': dates, 'count': counts})

        # Crear gráfico de línea
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=example_df['date'],
            y=example_df['count'],
            mode='lines+markers',
            line=dict(color=TIGO_COLORS['secondary'], width=3),
            marker=dict(color=TIGO_COLORS['primary'], size=8),
            fill='tozeroy',
            fillcolor=f'rgba{tuple(int(TIGO_COLORS["secondary"][i:i+2], 16) for i in (1, 3, 5)) + (0.1,)}'
        ))

        fig.update_layout(
            title="",
            xaxis_title="Fecha",
            yaxis_title="Número de Cargas",
            template="plotly_white",
            margin=dict(t=0, b=50, l=50, r=20),
            height=300
        )

        st.caption("Vista previa de ejemplo:")
        st.plotly_chart(fig, use_container_width=True)

    # Cerrar el div de la tarjeta
    st.markdown("</div>", unsafe_allow_html=True)
