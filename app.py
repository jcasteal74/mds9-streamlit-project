import streamlit as st
import folium
from streamlit_folium import folium_static
from utiles.data_loading import load_geodata, load_flats_data
from utiles.data_processing import procesar_datos, get_median_df_byLOCATIONNAME
from utiles.visualization import mostrar_mapa_y_tabla
from utiles.constantes import OPCIONES

st.set_page_config(
    page_title="Housevidsor",
    layout="wide",
    page_icon="./resources/precio200x200.png", 
)

# Carga de ficheros
zip_path = './datasource/Barrios.zip'
gdf = load_geodata(zip_path)

excel_path = './datasource/sample-flats-madrid-synthetic-coords.csv'
df_flats = load_flats_data(excel_path)

# Transformación fichero flats
gdf, df_flats, latitud, longitud = procesar_datos(gdf, df_flats)

# Crear mapa base
m = folium.Map(location=[latitud, longitud], zoom_start=10, tiles='CartoDB positron')

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