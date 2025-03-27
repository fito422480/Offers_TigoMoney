import streamlit as st
import pandas as pd
import datetime
from pathlib import Path
from components.charts import create_bar_chart
from config.app_config import BUCKET_NAME

def show_history():
    """
    Muestra la página de historial de cargas.
    """
    st.markdown("# Historial de Cargas")

    # Display upload history
    if st.session_state.upload_history:
        st.markdown("## Historial reciente")

        # Create DataFrame from upload history
        history_df = pd.DataFrame(st.session_state.upload_history)
        history_df['filename'] = history_df['filename'].apply(lambda x: Path(x).name)

        # Add a status column (always success for this demo)
        history_df['estado'] = 'Éxito'

        # Sort by timestamp, most recent first
        history_df = history_df.sort_values('timestamp', ascending=False)

        # Display as a styled table
        st.dataframe(
            history_df[['timestamp', 'filename', 'bucket', 'estado']],
            column_config={
                "timestamp": "Fecha y Hora",
                "filename": "Archivo",
                "bucket": "Bucket",
                "estado": "Estado"
            },
            hide_index=True,
            use_container_width=True
        )

        # Download button
        csv = history_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Descargar historial como CSV",
            csv,
            "historial_cargas.csv",
            "text/csv",
            key='download-csv'
        )

        # Activity charts
        st.markdown("## Actividad de Cargas")

        # Extract date only from timestamp for grouping
        history_df['date'] = pd.to_datetime(history_df['timestamp']).dt.date

        # Count uploads by date
        uploads_by_date = history_df.groupby('date').size().reset_index(name='count')
        uploads_by_date = uploads_by_date.sort_values('date')

        # Create bar chart
        fig = create_bar_chart(
            uploads_by_date,
            'date',
            'count',
            title="Cargas por Día",
            x_title="Fecha",
            y_title="Número de Cargas"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Agregar detalles adicionales
        st.markdown("## Detalles de cargas por tipo")

        # Extraer el tipo de oferta del nombre del archivo
        def extract_offer_type(filename):
            if "batch" in filename.lower():
                return "Batch"
            elif "direct" in filename.lower() or "lending_offers.csv" in filename.lower():
                return "Direct"
            elif "deductions" in filename.lower() or "payment" in filename.lower():
                return "Pago"
            elif "refinancing" in filename.lower():
                return "Refinanciamiento"
            elif "micro" in filename.lower():
                return "Micro Préstamos"
            elif "da_collection" in filename.lower():
                return "DA Collection"
            else:
                return "Otro"

        history_df['offer_type'] = history_df['filename'].apply(extract_offer_type)

        # Contar por tipo
        type_counts = history_df.groupby('offer_type').size().reset_index(name='count')

        # Crear gráfico
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### Cargas por tipo")
            st.dataframe(
                type_counts,
                column_config={
                    "offer_type": "Tipo de Oferta",
                    "count": "Cantidad"
                },
                hide_index=True,
                use_container_width=True
            )

        with col2:
            st.markdown("### Distribución por tipo")
            # Crear gráfico de barras
            fig = create_bar_chart(
                type_counts,
                'offer_type',
                'count',
                x_title="Tipo de Oferta",
                y_title="Cantidad"
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No hay historial de cargas disponible.")

        # Show a sample of what the history would look like
        st.markdown("### Vista previa del historial (muestra)")

        # Create sample data
        sample_data = {
            'timestamp': [
                '2025-03-27 09:15:32',
                '2025-03-27 08:30:45',
                '2025-03-26 14:22:18',
                '2025-03-26 11:05:33',
                '2025-03-25 16:40:21'
            ],
            'filename': [
                'output_lending_offers.csv',
                'campaign_deductions_debt_loans.csv',
                'collection_refinancing_campaign.csv',
                'output_lending_offers_batch.csv',
                'output_micro_loan_offers.csv'
            ],
            'bucket': [BUCKET_NAME] * 5,
            'estado': ['Éxito'] * 5
        }

        sample_df = pd.DataFrame(sample_data)

        st.dataframe(
            sample_df,
            column_config={
                "timestamp": "Fecha y Hora",
                "filename": "Archivo",
                "bucket": "Bucket",
                "estado": "Estado"
            },
            hide_index=True,
            use_container_width=True
        )

        st.markdown("""
        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border: 1px solid #ffeeba;">
            <p style="color: #856404; margin: 0;">
                <b>Nota:</b> Esta es una vista previa de muestra. El historial real se mostrará una vez que realice cargas de archivos.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar un gráfico de ejemplo
        st.markdown("### Ejemplo de visualización de actividad")

        # Datos de ejemplo para gráfico
        dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).date() for i in range(6, -1, -1)]
        counts = [3, 5, 4, 7, 2, 0, 1]

        sample_df = pd.DataFrame({
            'date': dates,
            'count': counts
        })

        # Crear gráfico
        fig = create_bar_chart(
            sample_df,
            'date',
            'count',
            title="Cargas por Día (Ejemplo)",
            x_title="Fecha",
            y_title="Número de Cargas"
        )

        st.plotly_chart(fig, use_container_width=True)
