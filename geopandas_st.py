import streamlit as st
import geopandas as gpd
import pandas as pd
import unicodedata
import folium
from streamlit_folium import folium_static
from utils import convert_to_wgs84, calculate_map_center  # Importar la función desde utils.py

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
    df_median_feature_sorted = df_median_feature.sort_values(by=f"{feature}", ascending=False)    
    return df_median_feature_sorted

st.set_page_config(
    page_title="Housevidsor",
    layout="wide",
    page_icon="./resources/precio200x200.png", 
)


# Función para cargar el GeoDataFrame
@st.cache_data
def load_geodata(zip_path):
    return gpd.read_file(f"zip://{zip_path}")

# Función para cargar el DataFrame de flats
@st.cache_data
def load_flats_data(excel_path):
    return pd.read_csv(excel_path, sep=';')

# Carga de ficheros
zip_path = './datasource/Barrios.zip'
gdf = load_geodata(zip_path)

excel_path = './datasource/sample-flats-madrid-synthetic-coords.csv'
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
st.sidebar.title("Housevidsor")

with st.sidebar:
  st.image("./resources/precio200x200.png", width=150)
seccion = st.sidebar.radio(
    "Selecciona una sección:",
    ("Visualización de datos medios", "Visualización por distritos", "Modelado predictivo", "Información", "Recursos")
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
        median = get_median_df_byLOCATIONNAME('PRICE', df_flats)
        gdf = gdf.merge(median, on='NOMBRE', how='left')
    elif opcion == 'mediana de NºHabitaciones/Barrio':
        lista = ['NOMBRE', 'ROOMNUMBER']
        st.write("Has elegido nº hab. medio / barrio:")
        median = get_median_df_byLOCATIONNAME('ROOMNUMBER', df_flats)
        gdf = gdf.merge(median, on='NOMBRE', how='left')
    elif opcion == 'superficie media inmueble':
        lista = ['NOMBRE', 'AREA']
        st.write("Has elegido superficie media inmueble")
        median = get_median_df_byLOCATIONNAME('AREA', df_flats)
        gdf = gdf.merge(median, on='NOMBRE', how='left')

    # Creamos las dos columnas donde descansa la información.
    col1, col2 = st.columns(2, border=True)
    
    with col1:
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
    
    with col2:
        st.table(median)


elif seccion == "Visualización por distritos":
    st.write("Aquí puedes agregar contenido específico para la visualización por distritos.")
    import altair as alt
    lista_distritos = df_flats.distrito.unique().tolist()
    opcion = st.selectbox(
        'Elige una opción:',
        (lista_distritos)
    )

    df_flats_filtered = df_flats[df_flats['distrito'] == opcion]
    
    col1, col2 = st.columns(2, border=True)
    
    # Columna 1: Gráficos de Altair
    with col1:
        # Gráfico de dispersión interactivo entre área y precio
        scatter = alt.Chart(df_flats_filtered).mark_circle(size=60).encode(
            x='PRICE',
            y='AREA',
            color='barrio',
            tooltip=['PRICE', 'AREA', 'barrio']
        ).properties(
            width=700,  # Ancho del gráfico
            height=400  # Alto del gráfico
        ).interactive()

        # Mostrar solo el gráfico de dispersión
        st.altair_chart(scatter, use_container_width=True)

    with col2:  
        st.write("Localización de outliers")
        # Convertir las coordenadas del DataFrame a WGS84
        original_crs = 25830  # Cambia esto por el EPSG de tu CRS original
        df_wgs84 = convert_to_wgs84(df_flats_filtered, 'X', 'Y', original_crs)

        # Identificar outliers usando el método IQR
        Q1 = df_wgs84['PRICE'].quantile(0.25)
        Q3 = df_wgs84['PRICE'].quantile(0.75)
        IQR = Q3 - Q1

        outliers = df_wgs84[(df_wgs84['PRICE'] < (Q1 - 1.5 * IQR)) | (df_wgs84['PRICE'] > (Q3 + 1.5 * IQR))]
        non_outliers = df_wgs84[(df_wgs84['PRICE'] >= (Q1 - 1.5 * IQR)) & (df_wgs84['PRICE'] <= (Q3 + 1.5 * IQR))]

        # Calcular el centro del mapa a partir de las coordenadas de todos los inmuebles
        center_lat, center_lon = calculate_map_center(df_wgs84)

        # Crear un mapa centrado en el centro calculado
        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Añadir marcadores para los outliers
        for idx, row in outliers.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Outlier - Precio: {row['PRICE']}, Área: {row['AREA']}",
                icon=folium.Icon(color='red')
            ).add_to(m2)

        # Añadir marcadores para los no outliers
        for idx, row in non_outliers.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Precio: {row['PRICE']}, Área: {row['AREA']}",
                icon=folium.Icon(color='blue')
            ).add_to(m2)

        # Renderizar el mapa en Streamlit
        folium_static(m2)
    
elif seccion == "Modelado predictivo":
    st.write("Aquí vendrá el modelado predictivo")
    
    # Leer el contenido del archivo markdown
    with open("./resources/wip.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # Mostrar el markdown en el sidebar
    st.markdown(markdown_text)
        
   
elif seccion == "Información":
    st.write("Información")
    
    # Leer el contenido del archivo markdown
    with open("./resources/info.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # Mostrar el markdown en el sidebar
    st.markdown(markdown_text)
    
elif seccion == "Recursos":
    st.write("Recursos")
    
        # Leer el contenido del archivo markdown
    with open("./resources/recursos.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # Mostrar el markdown en el sidebar
    st.markdown(markdown_text)
    

