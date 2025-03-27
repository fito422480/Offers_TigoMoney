# Tigo Money - Sistema de Carga de Ofertas

Aplicación moderna para la gestión y carga de diferentes tipos de ofertas de Tigo Money.

## Características principales

- **Dashboard informativo**: Visualización de métricas y estadísticas de cargas
- **Carga de ofertas**: Interfaz intuitiva para cargar ofertas de diferentes tipos
- **Historial de cargas**: Seguimiento detallado de las cargas realizadas
- **Configuración**: Personalización del sistema y parámetros

## Tipos de ofertas soportados

- Ofertas Batch
- Ofertas Direct
- Ofertas de Pago
- Ofertas de Refinanciamiento
- Ofertas de Micro Préstamos
- Archivos DA Collection

## Requisitos

- Python 3.8+
- Streamlit 1.31.0+
- Pandas, NumPy, Plotly
- Boto3 (para interacción con AWS)
- Pillow (para procesamiento de imágenes)

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tigomoney/carga-ofertas.git
cd tigo_money_app
```

2. Crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`.

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
│   ├── cards.py                # Componentes de tarjetas
│   ├── charts.py               # Componentes de gráficos
│   └── navigation.py           # Componentes de navegación
│
├── config/                     # Configuraciones
│   ├── app_config.py           # Configuración de la aplicación
│   └── aws_config.py           # Configuración de AWS
│
├── pages/                      # Páginas de la aplicación
│   ├── dashboard.py            # Página de dashboard
│   ├── offer_upload.py         # Página de carga de ofertas
│   ├── history.py              # Página de historial
│   └── settings.py             # Página de configuración
│
├── utils/                      # Utilidades
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

## Proceso de carga de ofertas

1. **Selección de tipo de oferta**: Elija el tipo de oferta a cargar
2. **Subida de archivo**: Cargue el archivo CSV correspondiente
3. **Validación**: Visualice la vista previa y valide los datos
4. **Procesamiento**: Inicie el proceso de validación, transformación y carga
5. **Confirmación**: Reciba la confirmación de carga exitosa

## Configuración

La aplicación puede configurarse a través de la interfaz de usuario en la sección "Configuración", donde podrá ajustar:

- Entorno (DEV, UAT, PROD)
- País
- Parámetros de conexión a AWS
- Tamaño de fragmentos para procesamiento
- Configuraciones específicas por tipo de oferta

## Paleta de colores

- **Amarillo Tigo**: #fac619
- **Azul Tigo**: #363856
- **Azul claro**: #4a4c6a
- **Amarillo claro**: #fad54d

## Licencia

Esta aplicación es propiedad exclusiva de Tigo Money. Todos los derechos reservados.
