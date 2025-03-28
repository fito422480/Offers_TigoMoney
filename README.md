# Tigo Money - Sistema de Carga de Ofertas

Aplicación moderna para la gestión y carga de diferentes tipos de ofertas de Tigo Money, con interfaz de usuario mejorada basada en Streamlit.

## Mejoras Implementadas

- **Interfaz renovada con colores corporativos** de Tigo Money (amarillo #fac619 y azul #363856)
- **Fondo blanco con texto azul** para una mejor legibilidad
- **Barra lateral funcional** con navegación clara
- **Dashboard con métricas visuales** para seguimiento de actividad
- **Pestañas de carga por tipo de oferta**
- **Área de arrastrar y soltar archivos** mejorada

## Requisitos

- Python 3.8 o superior
- Streamlit 1.31.0 o superior
- Pandas, NumPy
- Plotly para visualizaciones
- Boto3 para interacción con AWS

## Instalación

1. Clona el repositorio o copia los archivos en la estructura indicada
2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Crea la estructura de carpetas:
```bash
mkdir -p assets/css components config pages utils
```

5. Coloca cada archivo en su carpeta correspondiente según la estructura del proyecto

## Estructura del proyecto

```
tigo_money_app/
│
├── app.py                      # Aplicación principal de Streamlit
├── requirements.txt            # Dependencias del proyecto
│
├── assets/                     # Recursos estáticos
│   └── css/
│       └── styles.css          # Estilos personalizados
│
├── components/                 # Componentes reutilizables de la UI
│   ├── __init__.py
│   ├── cards.py                # Componentes de tarjetas
│   ├── charts.py               # Componentes de gráficos
│   └── navigation.py           # Componentes de navegación
│
├── config/                     # Configuraciones
│   ├── __init__.py
│   ├── app_config.py           # Configuración de la aplicación
│   └── aws_config.py           # Configuración de AWS
│
├── pages/                      # Páginas de la aplicación
│   ├── __init__.py
│   ├── dashboard.py            # Página de dashboard
│   ├── offer_upload.py         # Página de carga de ofertas
│   ├── history.py              # Página de historial
│   └── settings.py             # Página de configuración
│
├── utils/                      # Utilidades
│   ├── __init__.py
│   ├── file_processors.py      # Funciones para procesar archivos
│   ├── s3_utils.py             # Funciones para interactuar con S3
│   └── ui_helpers.py           # Funciones de ayuda para la UI
│
└── libs/                       # Lógica de negocio original
    ├── __init__.py
    ├── classes.py              # Clases (enums, excepciones)
    ├── discard_offers_functions.py  # Funciones de descarte
    └── transform_da_json.py    # Funciones de transformación
```

## Ejecución

Para ejecutar la aplicación:

```bash
streamlit run app.py
```

La aplicación estará disponible en http://localhost:8501

## Funcionalidades principales

1. **Dashboard**: Visualiza métricas y estadísticas de las cargas realizadas
2. **Carga de Ofertas**: Interfaz para subir archivos CSV dividida por tipo de oferta
   - Direct
   - Batch
   - Pago
   - Refinanciamiento
   - Micro Préstamos
   - DA Collection
3. **Historial**: Seguimiento detallado de todas las cargas realizadas
4. **Configuración**: Personalización de parámetros y ajustes

## Solución de problemas

Si encuentras errores al ejecutar la aplicación:

1. Asegúrate de tener todos los archivos `__init__.py` necesarios en cada carpeta
2. Verifica que estás ejecutando desde el directorio raíz del proyecto
3. Comprueba que la estructura de carpetas es correcta
4. Asegúrate de que todas las dependencias están instaladas correctamente
