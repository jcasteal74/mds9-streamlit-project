import streamlit as st
import folium

#from streamlit_folium import folium_static
from utiles.data_loading import load_geodata, load_flats_data
from utiles.data_processing import procesar_datos, get_median_df_byLOCATIONNAME
from utiles.visualization import mostrar_mapa_y_tabla
from utiles.constantes import OPCIONES
#from utiles.geo_func import convert_to_wgs84, calculate_map_center
from utiles.eda_functions import general_tab, descriptiva_tab, numeric_variables_tab, categorical_variables_tab, correlation_tab, target_tab
from utiles.plot_functions import plot_price_distribution, plot_area_vs_price, plot_rooms_baths_vs_price, plot_property_types, plot_amenities_vs_price

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
        ("EDA", "Visualización de datos medios", "Insights visuales", "Modelado predictivo", "Información", "Recursos")
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

elif seccion == "EDA":
    st.write("Apartado relacionado con Análisis Exploratorio de los Datos.")
    # Crear las pestañas
    tabs = st.tabs(["General", "Descriptiva", "Variables Numéricas", "Variables Categóricas", "Correlación", "Target"])

    # Pestaña General
    with tabs[0]:
        general_tab(df_flats)

    # Pestaña Descriptiva
    with tabs[1]:
        descriptiva_tab(df_flats)

    # Pestaña Variables Numéricas
    with tabs[2]:
        numeric_variables_tab(df_flats)

    # Pestaña Variables Categóricas
    with tabs[3]:
        categorical_variables_tab(df_flats)

    # Pestaña Correlación
    with tabs[4]:
        correlation_tab(df_flats)

    # Target
    with tabs[5]:
        target_tab(df_flats)


elif seccion == "Insights visuales":
    st.write("Aquí puedes agregar contenido específico para la visualización de insights")
    # Crear un menú desplegable
    menu = ["Selecciona una opción", "Distribución de Precios", "Área vs Precio", "Habitaciones y Baños vs Precio", "Tipos de Propiedades", "Amenidades vs Precio"]
    choice = st.selectbox("Selecciona un gráfico para visualizar", menu)
    
    if choice == "Distribución de Precios":
        plot_price_distribution(df_flats)
    elif choice == "Área vs Precio":
        plot_area_vs_price(df_flats)
    elif choice == "Habitaciones y Baños vs Precio":
        plot_rooms_baths_vs_price(df_flats)
    elif choice == "Tipos de Propiedades":
        plot_property_types(df_flats)
    elif choice == "Amenidades vs Precio":
        plot_amenities_vs_price(df_flats)
    
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