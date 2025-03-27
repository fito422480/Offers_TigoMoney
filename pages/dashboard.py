import streamlit as st
import pandas as pd
import datetime
from components.cards import display_metric, render_card
from components.charts import create_pie_chart, create_weekly_trend_chart
from config.app_config import BUCKET_NAME
from pathlib import Path

def show_dashboard():
    """
    Muestra el dashboard con estadísticas y gráficos.
    """
    st.markdown("# Dashboard de Cargas")

    # Summary metrics
    st.markdown("## Métricas de Carga")

    # Get statistics from session state
    total_uploads = sum(sum(type_stats.values()) for date_stats in st.session_state.upload_stats.values() for type_stats in date_stats.values()) if st.session_state.upload_stats else 0

    # Get today's uploads
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_uploads = sum(st.session_state.upload_stats.get(today, {}).values()) if today in st.session_state.upload_stats else 0

    # Calculate mock metrics
    success_rate = "99.8%"
    avg_time = "45s"

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    display_metric(total_uploads, "Total de Cargas", col1)
    display_metric(today_uploads, "Cargas de Hoy", col2)
    display_metric(success_rate, "Tasa de Éxito", col3)
    display_metric(avg_time, "Tiempo Promedio", col4)

    st.markdown("---")

    # Recent activity and charts
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### Actividad Reciente")
        if st.session_state.upload_history:
            history_df = pd.DataFrame(st.session_state.upload_history[-5:])
            history_df['filename'] = history_df['filename'].apply(lambda x: Path(x).name)
            st.dataframe(
                history_df[['timestamp', 'filename', 'bucket']],
                hide_index=True,
                column_config={
                    "timestamp": "Fecha y Hora",
                    "filename": "Archivo",
                    "bucket": "Bucket"
                },
                use_container_width=True
            )
        else:
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

    with col2:
        st.markdown("### Distribución de Cargas")

        # Create pie chart data from upload stats
        if st.session_state.upload_stats:
            offer_counts = {}
            for date_stats in st.session_state.upload_stats.values():
                for offer_type, count in date_stats.items():
                    if offer_type not in offer_counts:
                        offer_counts[offer_type] = 0
                    offer_counts[offer_type] += count

            if offer_counts:
                fig = create_pie_chart(offer_counts, "Distribución por Tipo")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para la gráfica.")
        else:
            st.info("No hay datos suficientes para la gráfica.")

            # Mostrar datos de ejemplo
            sample_counts = {
                "Batch": 12,
                "Direct": 8,
                "Pago": 5,
                "Refinanciamiento": 3
            }

            fig = create_pie_chart(sample_counts, "Distribución por Tipo (Ejemplo)")
            st.caption("Vista previa de ejemplo:")
            st.plotly_chart(fig, use_container_width=True)

    # Weekly trend
    st.markdown("### Tendencia Semanal")

    # Get data for weekly trend
    if st.session_state.upload_history:
        # Extract date only from timestamp for grouping
        history_df = pd.DataFrame(st.session_state.upload_history)
        history_df['date'] = pd.to_datetime(history_df['timestamp']).dt.date

        # Count uploads by date
        uploads_by_date = history_df.groupby('date').size().reset_index(name='count')

        # Fill missing dates with zeros
        dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).date() for i in range(6, -1, -1)]
        all_dates = pd.DataFrame({'date': dates})
        uploads_by_date = pd.merge(all_dates, uploads_by_date, on='date', how='left').fillna(0)

        # Create chart
        fig = create_weekly_trend_chart(uploads_by_date['count'].tolist())
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Show example chart
        fig = create_weekly_trend_chart()
        st.caption("Vista previa de ejemplo:")
        st.plotly_chart(fig, use_container_width=True)
