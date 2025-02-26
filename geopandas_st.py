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
    return df_median_feature

# Función para cargar el GeoDataFrame
@st.cache_data
def load_geodata(zip_path):
    return gpd.read_file(f"zip://{zip_path}")

# Función para cargar el DataFrame de flats
@st.cache_data
def load_flats_data(excel_path):
    return pd.read_csv(excel_path, sep=';')

# Carga de ficheros
zip_path = './data/Barrios.zip'
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
st.sidebar.title("Menú de navegación")
seccion = st.sidebar.radio(
    "Selecciona una sección:",
    ("Visualización de datos medios", "Visualización por distritos", "Información", "Recursos")
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

elif seccion == "Visualización por distritos":
    st.write("Aquí puedes agregar contenido específico para la visualización por distritos.")
    import altair as alt
    lista_distritos = df_flats.distrito.unique().tolist()
    opcion = st.selectbox(
        'Elige una opción:',
        (lista_distritos)
    )

    df_flats_filtered = df_flats[df_flats['distrito'] == opcion]
    
    # Gráfico de dispersión interactivo entre área y precio
    scatter = alt.Chart(df_flats_filtered).mark_circle(size=60).encode(
        x='PRICE',
        y='AREA',
        color='barrio',
        tooltip=['PRICE', 'AREA', 'barrio']
    ).interactive()

    # Gráfico de barras del número de pisos por barrio
    bar_chart = alt.Chart(df_flats_filtered).mark_bar().encode(
        x='barrio',
        y='count()',
        color='barrio',
        tooltip=['barrio', 'count()']
    ).interactive()

    # Gráfico de líneas del precio medio por área
    line_chart = alt.Chart(df_flats_filtered).mark_line().encode(
        x='AREA',
        y='mean(PRICE)',
        color='barrio',
        tooltip=['AREA', 'mean(PRICE)', 'barrio']
    ).interactive()

    # Combinar los gráficos verticalmente
    combined_chart = alt.vconcat(
        scatter,
        bar_chart,
        line_chart
    ).resolve_scale(
        color='independent'
    )

    st.altair_chart(combined_chart, use_container_width=True)
    
    
    st.write("Localización de outliers")
    
    # Convertir las coordenadas del DataFrame a WGS84
    original_crs = 25830  # Cambia esto por el EPSG de tu CRS original
    df_wgs84 = convert_to_wgs84(df_flats_filtered, 'X', 'Y', original_crs)


    
    # Identificar outliers usando el método IQR
    Q1 = df_wgs84['PRICE'].quantile(0.25)
    Q3 = df_wgs84['PRICE'].quantile(0.75)
    IQR = Q3 - Q1

    outliers = df_wgs84[(df_wgs84['PRICE'] < (Q1 - 1.5 * IQR)) | (df_wgs84['PRICE'] > (Q3 + 1.5 * IQR))]
    
    if outliers.empty:
        st.write("No se encontraron outliers.")
    else:
        # Calcular el centro del mapa a partir de las coordenadas de los outliers
        center_lat, center_lon = calculate_map_center(outliers)

        # Crear un mapa centrado en el centro calculado
        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Añadir marcadores para los outliers
        for idx, row in outliers.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],  # Ajusta según las columnas de latitud y longitud en tu DataFrame
                popup=f"Precio: {row['PRICE']}, Área: {row['AREA']}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m2)

        # Renderizar el mapa en Streamlit
        folium_static(m2)
        
        

    # Añadir marcadores para los outliers
    for idx, row in outliers.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],  # Ajusta según las columnas de latitud y longitud en tu DataFrame
            popup=f"Precio: {row['PRICE']}, Área: {row['AREA']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m2)
    
elif seccion == "Información":
    st.write("Información")
    
    # Leer el contenido del archivo markdown
    with open("./data/info.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # Mostrar el markdown en el sidebar
    st.markdown(markdown_text)
    
elif seccion == "Recursos":
    st.write("Recursos")
    
    # Mostrar el markdown en el sidebar
    st.markdown("### Esto es markdown ⬇️")

