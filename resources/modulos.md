1. Crear una estructura de directorios
Primero, organiza tu proyecto en una estructura de directorios clara. Por ejemplo:

mi_proyecto/
│
├── app.py
├── utils/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── visualization.py
│   └── constants.py
└── resources/
    └── precio200x200.png
2. Mover funciones a módulos
Luego, mueve las funciones a los módulos correspondientes. Por ejemplo, data_processing.py podría contener funciones relacionadas con el procesamiento de datos, y visualization.py podría contener funciones relacionadas con la visualización.

utils/data_processing.py
def get_median_df_byLOCATIONNAME(column, df):
    # Implementación de la función
    pass
utils/visualization.py
import folium
from streamlit_folium import folium_static
import streamlit as st

def mostrar_mapa_y_tabla(gdf, lista, median, m):
    col1, col2 = st.columns(2, border=True)
    
    with col1:
        folium.Choropleth(
            geo_data=gdf.to_json(),
            name='choropleth',
            data=gdf,
            columns=lista,
            key_on='feature.properties.NOMBRE',
            fill_color='OrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'{lista[1]} medio por barrio'
        ).add_to(m)
        folium.LayerControl().add_to(m)
        folium_static(m)
    
    with col2:
        st.table(median)
utils/constants.py
OPCIONES = {
    'mediana de Precios/Barrio': ('PRICE', 'precio medio / barrio'),
    'mediana de NºHabitaciones/Barrio': ('ROOMNUMBER', 'nº hab. medio / barrio'),
    'superficie media inmueble': ('AREA', 'superficie media inmueble')
}
3. Importar y usar los módulos en tu aplicación principal
Finalmente, importa y utiliza estas funciones en tu archivo principal app.py.

app.py
import streamlit as st
from utils.data_processing import get_median_df_byLOCATIONNAME
from utils.visualization import mostrar_mapa_y_tabla
from utils.constants import OPCIONES

with st.sidebar:
    st.image("./resources/precio200x200.png", width=150)
    seccion = st.sidebar.radio(
        "Selecciona una sección:",
        ("Visualización de datos medios", "Visualización por distritos", "Modelado predictivo", "Información", "Recursos")
    )

if seccion == "Visualización de datos medios":
    opcion = st.selectbox(
        'Elige una opción:',
        list(OPCIONES.keys())
    )
    
    if opcion in OPCIONES:
        columna, mensaje = OPCIONES[opcion]
        lista = ['NOMBRE', columna]
        st.write(f"Has elegido {mensaje}:")
        median = get_median_df_byLOCATIONNAME(columna, df_flats)
        gdf = gdf.merge(median, on='NOMBRE', how='left')
        mostrar_mapa_y_tabla(gdf, lista, median, m)
Beneficios de esta estructura:
Claridad: El código está organizado en módulos lógicos, lo que facilita la comprensión.
Reutilización: Las funciones pueden ser reutilizadas en diferentes partes del proyecto o en otros proyectos.
Mantenibilidad: Es más fácil mantener y actualizar el código cuando está bien organizado.
Colaboración: Facilita la colaboración en equipo, ya que los desarrolladores pueden trabajar en diferentes módulos sin interferir entre sí.
En resumen, modularizar tu código y organizarlo en diferentes archivos y directorios es una excelente práctica que puede mejorar significativamente la calidad de tu proyecto.