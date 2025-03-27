import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime

def create_pie_chart(data_dict, title="Distribución"):
    """
    Crea un gráfico de pastel.

    Args:
        data_dict (dict): Diccionario con los datos (clave: valor).
        title (str): Título del gráfico.

    Returns:
        plotly.graph_objects.Figure: Gráfico de pastel.
    """
    fig = px.pie(
        values=list(data_dict.values()),
        names=list(data_dict.keys()),
        color_discrete_sequence=px.colors.sequential.Bluyl,
        hole=0.4
    )

    fig.update_layout(
        title=title,
        margin=dict(t=50, b=0, l=0, r=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )

    return fig

def create_bar_chart(df, x, y, title="", x_title="", y_title=""):
    """
    Crea un gráfico de barras.

    Args:
        df (pandas.DataFrame): DataFrame con los datos.
        x (str): Columna para el eje x.
        y (str): Columna para el eje y.
        title (str): Título del gráfico.
        x_title (str): Etiqueta para el eje x.
        y_title (str): Etiqueta para el eje y.

    Returns:
        plotly.graph_objects.Figure: Gráfico de barras.
    """
    fig = px.bar(
        df,
        x=x,
        y=y,
        labels={x: x_title or x, y: y_title or y},
        color_discrete_sequence=['#363856']
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_title or x,
        yaxis_title=y_title or y,
        template="plotly_white"
    )

    return fig

def create_line_chart(df, x, y, title="", x_title="", y_title=""):
    """
    Crea un gráfico de línea.

    Args:
        df (pandas.DataFrame): DataFrame con los datos.
        x (str): Columna para el eje x.
        y (str): Columna para el eje y.
        title (str): Título del gráfico.
        x_title (str): Etiqueta para el eje x.
        y_title (str): Etiqueta para el eje y.

    Returns:
        plotly.graph_objects.Figure: Gráfico de línea.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[x],
        y=df[y],
        mode='lines+markers',
        line=dict(color='#363856', width=3),
        marker=dict(color='#fac619', size=8),
        fill='tozeroy',
        fillcolor='rgba(54, 56, 86, 0.1)'
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_title or x,
        yaxis_title=y_title or y,
        template="plotly_white",
        margin=dict(t=50, b=0, l=0, r=0),
        height=300
    )

    return fig

def create_weekly_trend_chart(uploads_per_day=None):
    """
    Crea un gráfico de tendencia semanal.

    Args:
        uploads_per_day (list, optional): Lista con el número de cargas por día.

    Returns:
        plotly.graph_objects.Figure: Gráfico de tendencia semanal.
    """
    # Si no se proporcionan datos, usar datos de ejemplo
    if uploads_per_day is None:
        uploads_per_day = [3, 5, 4, 7, 2, 0, 1]

    # Crear fechas para la última semana
    dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

    # Crear DataFrame
    df = pd.DataFrame({
        'fecha': dates,
        'cargas': uploads_per_day
    })

    # Crear gráfico
    return create_line_chart(
        df,
        'fecha',
        'cargas',
        title="Cargas por Día",
        x_title="Fecha",
        y_title="Número de Cargas"
    )
