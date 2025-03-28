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
    # Título del dashboard
    st.markdown(
        """
        <div style="padding: 2rem 0 1rem 0;">
            <h1 style="color: #363856; font-size: 2rem; font-weight: 600; margin: 0; padding: 0;">
                Dashboard de Carga de Ofertas
            </h1>
            <p style="color: #4b4d6d; margin: 0.5rem 0 0 0; font-size: 1rem;">
                Visualiza y controla tus operaciones de carga de ofertas a un vistazo
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Métricas principales
    st.markdown("<h2 style='color: #363856; margin-bottom: 1rem;'>Métricas principales</h2>", unsafe_allow_html=True)

    # Crear una fila de métricas
    col1, col2, col3, col4 = st.columns(4)

    # Obtener datos de carga desde session_state
    total_uploads = sum(sum(type_stats.values()) for date_stats in st.session_state.upload_stats.values() for type_stats in date_stats.values()) if st.session_state.upload_stats else 0

    # Obtener datos de hoy
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_uploads = sum(st.session_state.upload_stats.get(today, {}).values()) if today in st.session_state.upload_stats else 0

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
            ">
                <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0; font-size: 1.25rem; margin-bottom: 1rem;">
                    Actividad Reciente
                </h3>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.upload_history:
            # Crear un dataframe para mostrar el historial
            history_df = pd.DataFrame(st.session_state.upload_history[-5:])
            history_df['filename'] = history_df['filename'].apply(lambda x: Path(x).name)

            # Mostrar historial de cargas recientes
            st.dataframe(
                history_df[['timestamp', 'filename', 'bucket']],
                column_config={
                    "timestamp": "Fecha y Hora",
                    "filename": "Archivo",
                    "bucket": "Bucket"
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            # Datos de ejemplo si no hay actividad
            st.info("No hay actividad reciente para mostrar.")

            # Mostrar datos de ejemplo
            sample_data = {
                'timestamp': [
                    '2025-03-27 09:15:32',
                    '2025-03-27 08:30:45',
                    '2025-03-26 14:22:18'
                ],
                'filename': [
                    'output_lending_offers.csv',
                    'campaign_deductions_debt_loans.csv',
                    'collection_refinancing_campaign.csv'
                ],
                'bucket': [BUCKET_NAME] * 3
            }

            sample_df = pd.DataFrame(sample_data)
            st.caption("Vista previa de ejemplo:")
            st.dataframe(
                sample_df,
                column_config={
                    "timestamp": "Fecha y Hora",
                    "filename": "Archivo",
                    "bucket": "Bucket"
                },
                hide_index=True,
                use_container_width=True
            )

        # Cerrar el div de la tarjeta
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Gráfico de distribución
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 1rem;
            ">
                <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0; font-size: 1.25rem; margin-bottom: 1rem;">
                    Distribución de Cargas
                </h3>
            """,
            unsafe_allow_html=True
        )

        # Crear datos para el gráfico
        if st.session_state.upload_stats:
            offer_counts = {}
            for date_stats in st.session_state.upload_stats.values():
                for offer_type, count in date_stats.items():
                    if offer_type not in offer_counts:
                        offer_counts[offer_type] = 0
                    offer_counts[offer_type] += count

            if offer_counts:
                fig = px.pie(
                    values=list(offer_counts.values()),
                    names=list(offer_counts.keys()),
                    color_discrete_sequence=[TIGO_COLORS['primary'], TIGO_COLORS['secondary'],
                                            TIGO_COLORS['primary_light'], TIGO_COLORS['secondary_light']],
                    hole=0.4
                )

                fig.update_layout(
                    margin=dict(t=0, b=0, l=0, r=0),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2)
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para la gráfica.")
        else:
            # Datos de ejemplo
            sample_counts = {
                "Batch": 12,
                "Direct": 8,
                "Pago": 5,
                "Refinanciamiento": 3
            }

            fig = px.pie(
                values=list(sample_counts.values()),
                names=list(sample_counts.keys()),
                color_discrete_sequence=[TIGO_COLORS['primary'], TIGO_COLORS['secondary'],
                                        TIGO_COLORS['primary_light'], TIGO_COLORS['secondary_light']],
                hole=0.4
            )

            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )

            st.caption("Vista previa de ejemplo:")
            st.plotly_chart(fig, use_container_width=True)

        # Cerrar el div de la tarjeta
        st.markdown("</div>", unsafe_allow_html=True)

    # Tendencia semanal
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
        ">
            <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0; font-size: 1.25rem; margin-bottom: 1rem;">
                Tendencia Semanal
            </h3>
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
