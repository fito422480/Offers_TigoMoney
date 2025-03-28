import streamlit as st
import pandas as pd
import datetime
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from config.app_config import BUCKET_NAME, TIGO_COLORS

def show_history():
    """
    Muestra la página de historial de cargas con el estilo Tigo Money.
    """
    # Título de la página
    st.markdown("<h1 style='color: #363856; margin-bottom: 1rem;'>Historial de Cargas</h1>", unsafe_allow_html=True)

    # Banner de sección
    st.markdown(
        f"""
        <div style="
            background-color: {TIGO_COLORS['primary']};
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h2 style="color: {TIGO_COLORS['secondary']}; margin: 0;">Historial de operaciones</h2>
            <p style="color: {TIGO_COLORS['secondary']}; margin-top: 5px;">
                Seguimiento detallado de todas las cargas realizadas en el sistema.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display upload history
    if st.session_state.upload_history:
        # Crear sección de historial reciente
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
            ">
                <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0;">Historial reciente</h3>
            """,
            unsafe_allow_html=True
        )

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

        # Cerrar div de la sección
        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        col1, col2 = st.columns([4, 1])
        with col2:
            csv = history_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Descargar CSV",
                csv,
                "historial_cargas.csv",
                "text/csv",
                key='download-csv',
                use_container_width=True
            )

        # Sección de análisis de actividad
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin: 20px 0;
            ">
                <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0;">Análisis de Actividad</h3>
            """,
            unsafe_allow_html=True
        )

        # Create visualization columns
        col1, col2 = st.columns(2)

        with col1:
            # Extract date only from timestamp for grouping
            history_df['date'] = pd.to_datetime(history_df['timestamp']).dt.date

            # Count uploads by date
            uploads_by_date = history_df.groupby('date').size().reset_index(name='count')
            uploads_by_date = uploads_by_date.sort_values('date')

            # Create bar chart
            fig = px.bar(
                uploads_by_date,
                x='date',
                y='count',
                labels={'date': 'Fecha', 'count': 'Número de Cargas'},
                color_discrete_sequence=[TIGO_COLORS['primary']]
            )

            fig.update_layout(
                title="Cargas por Día",
                template="plotly_white",
                margin=dict(l=40, r=20, t=40, b=40),
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Extract file type from filename
            def extract_offer_type(filename):
                filename = filename.lower()
                if "batch" in filename:
                    return "Batch"
                elif "direct" in filename or "lending_offers" in filename:
                    return "Direct"
                elif "deductions" in filename or "payment" in filename:
                    return "Pago"
                elif "refinancing" in filename:
                    return "Refinanciamiento"
                elif "micro" in filename:
                    return "Micro Préstamos"
                elif "da_collection" in filename:
                    return "DA Collection"
                else:
                    return "Otro"

            history_df['offer_type'] = history_df['filename'].apply(extract_offer_type)

            # Count by type
            type_counts = history_df.groupby('offer_type').size().reset_index(name='count')

            # Create pie chart for types
            fig = px.pie(
                type_counts,
                values='count',
                names='offer_type',
                color_discrete_sequence=[
                    TIGO_COLORS['primary'],
                    TIGO_COLORS['secondary'],
                    TIGO_COLORS['primary_light'],
                    TIGO_COLORS['secondary_light'],
                    "#10B981",
                    "#3B82F6"
                ],
                hole=0.4
            )

            fig.update_layout(
                title="Distribución por Tipo",
                template="plotly_white",
                margin=dict(l=20, r=20, t=40, b=20),
            )

            st.plotly_chart(fig, use_container_width=True)

        # Cerrar div de la sección de análisis
        st.markdown("</div>", unsafe_allow_html=True)

        # Sección de detalles
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin: 20px 0;
            ">
                <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0;">Detalles por tipo de oferta</h3>
            """,
            unsafe_allow_html=True
        )

        # Display summary by type
        type_stats = history_df.groupby('offer_type').agg(
            total_archivos=('filename', 'count'),
            primera_carga=('timestamp', 'min'),
            ultima_carga=('timestamp', 'max')
        ).reset_index()

        st.dataframe(
            type_stats,
            column_config={
                "offer_type": "Tipo de Oferta",
                "total_archivos": "Total Archivos",
                "primera_carga": "Primera Carga",
                "ultima_carga": "Última Carga"
            },
            hide_index=True,
            use_container_width=True
        )

        # Cerrar div de la sección de detalles
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Mostrar mensaje de historial vacío
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
                text-align: center;
            ">
                <img src="https://img.icons8.com/fluency/96/000000/empty-box.png" style="width: 64px; height: 64px; margin-bottom: 15px;">
                <h3 style="color: {TIGO_COLORS['secondary']}; margin-top: 0;">No hay historial disponible</h3>
                <p style="color: #4b4d6d;">No se han encontrado cargas anteriores. El historial se mostrará aquí una vez que realice cargas de archivos.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Mostrar datos de ejemplo
        st.markdown("<h3 style='color: #363856;'>Vista previa de ejemplo</h3>", unsafe_allow_html=True)

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

        st.info("Esta es una vista previa de muestra. El historial real se mostrará una vez que realice cargas de archivos.")

        # Mostrar gráficos de ejemplo
        col1, col2 = st.columns(2)

        with col1:
            # Sample data for bar chart
            dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).date() for i in range(6, -1, -1)]
            counts = [3, 5, 4, 7, 2, 0, 1]

            sample_df = pd.DataFrame({
                'date': dates,
                'count': counts
            })

            # Create bar chart
            fig = px.bar(
                sample_df,
                x='date',
                y='count',
                labels={'date': 'Fecha', 'count': 'Número de Cargas'},
                color_discrete_sequence=[TIGO_COLORS['primary']]
            )

            fig.update_layout(
                title="Cargas por Día (Ejemplo)",
                template="plotly_white",
                margin=dict(l=40, r=20, t=40, b=40),
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Sample data for pie chart
            sample_types = {
                "Batch": 12,
                "Direct": 8,
                "Pago": 5,
                "Refinanciamiento": 3
            }

            sample_type_df = pd.DataFrame({
                'offer_type': list(sample_types.keys()),
                'count': list(sample_types.values())
            })

            # Create pie chart
            fig = px.pie(
                sample_type_df,
                values='count',
                names='offer_type',
                color_discrete_sequence=[
                    TIGO_COLORS['primary'],
                    TIGO_COLORS['secondary'],
                    TIGO_COLORS['primary_light'],
                    TIGO_COLORS['secondary_light']
                ],
                hole=0.4
            )

            fig.update_layout(
                title="Distribución por Tipo (Ejemplo)",
                template="plotly_white",
                margin=dict(l=20, r=20, t=40, b=20),
            )

            st.plotly_chart(fig, use_container_width=True)
