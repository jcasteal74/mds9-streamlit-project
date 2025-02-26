import streamlit as st
import geopandas as gpd
import pandas as pd
import unicodedata
import folium
from streamlit_folium import folium_static

# Función para eliminar acentos
def eliminar_acentos(texto):
    if isinstance(texto, str):
        texto = unicodedata.normalize('NFKD', texto)
        texto = ''.join([c for c in texto if not unicodedata.combining(c)])
    return texto

def get_median_df_byLOCATIONNAME(feature, df):
    median_feature = df.groupby('barrio')[feature].median()
    df_median_feature = median_feature.reset_index()
    df_median_feature.columns = ['NOMBRE', f"{feature}"]
    return df_median_feature

# Función para cargar el GeoDataFrame
@st.cache_data
def load_geodata(zip_path):
    return gpd.read_file(f"zip://{zip_path}")

# Función para cargar el DataFrame de flats
@st.cache_data
def load_flats_data(excel_path):
    return pd.read_excel(excel_path, engine='openpyxl')

# Carga de ficheros
zip_path = './data/Barrios.zip'
gdf = load_geodata(zip_path)

excel_path = './data/sample-flats-madrid-synthetic-coords.xlsx'
df_flats = load_flats_data(excel_path)

# Transformación fichero flats
gdf['NOMBRE'] = gdf['NOMBRE'].str.lower().apply(eliminar_acentos)
df_flats['barrio'] = df_flats['barrio'].str.lower().apply(eliminar_acentos)


# Convertir CRS
gdf = gdf.to_crs(epsg=4326)

# Obtener centroide
centroide = gdf.geometry.centroid
latitud = centroide.y.mean()
longitud = centroide.x.mean()

# Crear mapa base
m = folium.Map(location=[latitud, longitud], zoom_start=10, tiles='CartoDB positron')

# Interfaz de usuario de Streamlit
st.title('Exploración datos inmobiliarios')

# Sidebar
st.sidebar.title("Menú de navegación")
seccion = st.sidebar.radio(
    "Selecciona una sección:",
    ("Visualización de datos medios", "Visualización por barrios", "Información")
)

if seccion == "Visualización de datos medios":
    opcion = st.selectbox(
        'Elige una opción:',
        ('mediana de Precios/Barrio', 'mediana de NºHabitaciones/Barrio', 'superficie media inmueble')
    )

    if opcion == 'mediana de Precios/Barrio':
        lista = ['NOMBRE', 'PRICE']
        st.write("Has elegido precio medio / barrio:")
        # Generamos datos agrupados
        median_price_byLocationame = get_median_df_byLOCATIONNAME('PRICE', df_flats)
        gdf = gdf.merge(median_price_byLocationame, on='NOMBRE', how='left')
    elif opcion == 'mediana de NºHabitaciones/Barrio':
        lista = ['NOMBRE', 'ROOMNUMBER']
        st.write("Has elegido nº hab. medio / barrio:")
        median_rooms_byLocationame = get_median_df_byLOCATIONNAME('ROOMNUMBER', df_flats)
        gdf = gdf.merge(median_rooms_byLocationame, on='NOMBRE', how='left')
    elif opcion == 'superficie media inmueble':
        lista = ['NOMBRE', 'AREA']
        st.write("Has elegido superficie media inmueble")
        median_area_byLocationame = get_median_df_byLOCATIONNAME('AREA', df_flats)
        gdf = gdf.merge(median_area_byLocationame, on='NOMBRE', how='left')

    # Crear Choropleth
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

    # Mostrar mapa en Streamlit
    folium_static(m)

elif seccion == "Visualización por barrios":
    st.write("Aquí puedes agregar contenido específico para la visualización por barrios.")
    # Aquí puedes agregar más cosicas #
    
elif seccion == "Información":
    st.write("Información")
    
    # Leer el contenido del archivo markdown
    with open("./data/info.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # Mostrar el markdown en el sidebar
    st.markdown(markdown_text)

