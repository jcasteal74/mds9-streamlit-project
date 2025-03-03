import streamlit as st
import folium
from streamlit_folium import folium_static
from utiles.data_loading import load_geodata, load_flats_data
from utiles.data_processing import procesar_datos, get_median_df_byLOCATIONNAME
from utiles.visualization import mostrar_mapa_y_tabla
from utiles.constantes import OPCIONES
from utiles.geo_func import convert_to_wgs84, calculate_map_center

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
        list(OPCIONES.keys())
    )
    
    if opcion in OPCIONES:
        columna, mensaje = OPCIONES[opcion]
        lista = ['NOMBRE', columna]
        st.write(f"Has elegido {mensaje}:")
        median = get_median_df_byLOCATIONNAME(columna, df_flats)
        gdf = gdf.merge(median, on='NOMBRE', how='left')
        mostrar_mapa_y_tabla(gdf, lista, median, m)

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