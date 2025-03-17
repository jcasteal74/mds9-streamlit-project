import streamlit as st
import folium
import pandas as pd

from utiles.data_loading import load_geodata, load_flats_data
from utiles.data_processing import procesar_datos, get_median_df_byLOCATIONNAME
from utiles.visualization import mostrar_mapa_y_tabla
from utiles.constantes import OPCIONES
from utiles.eda_functions import descriptiva_tab, numeric_variables_tab, categorical_variables_tab, correlation_tab, target_tab,  nulls_tab, outliers_tab
from utiles.plot_functions import plot_price_distribution, plot_area_vs_price, plot_rooms_baths_vs_price, plot_property_types, plot_amenities_vs_price
from utiles.model_utils import load_model, load_encoders
from utiles.preprocessing import encode_categorical_columns, convert_binary_columns
from utiles.inicializar import initialization_streamlit_page


# Inicializamos la parte de estilo de la página
initialization_streamlit_page()

# Carga de ficheros
zip_path = './datasource/Barrios.zip'
gdf = load_geodata(zip_path)

excel_path = './datasource/sample-flats-madrid-synthetic-coords.csv'
df_flats = load_flats_data(excel_path)

# Transformación fichero flats
gdf, df_flats, latitud, longitud = procesar_datos(gdf, df_flats)



# Interfaz de usuario de Streamlit
st.title('Exploración datos inmobiliarios')

# Sidebar
st.sidebar.title("Housevidsor")

with st.sidebar:
    st.image("./resources/precio200x200.png", width=150)
    seccion = st.sidebar.radio(
        "Selecciona una sección:",
        ("EDA", "Visualización de datos medios", "Insights visuales", "Modelado predictivo", "Información")
    )

if seccion == "Visualización de datos medios":
    opcion = st.selectbox(
        'Elige una opción:',
        list(OPCIONES.keys())
    )
    
    if opcion in OPCIONES:
        # Crear mapa base
        m = folium.Map(location=[latitud, longitud], zoom_start=10, tiles='CartoDB positron')
        columna, mensaje = OPCIONES[opcion]
        lista = ['NOMBRE', columna]
        st.write(f"Has elegido {mensaje}:")
        median = get_median_df_byLOCATIONNAME(columna, df_flats)
        print(median.info())
        gdf = gdf.merge(median, on='NOMBRE', how='left')
        print(gdf.info())
        mostrar_mapa_y_tabla(gdf, lista, m)


elif seccion == "EDA":
    st.write("Apartado relacionado con Análisis Exploratorio de los Datos.")
    # Crear las pestañas
    tabs = st.tabs(["Descriptiva", "Variables Numéricas", "Variables Categóricas", "Correlación", "Target", "Nulos", "Outliers"])

    # Pestaña Descriptiva
    with tabs[0]:
        descriptiva_tab(df_flats)

    # Pestaña Variables Numéricas
    with tabs[1]:
        numeric_variables_tab(df_flats)

    # Pestaña Variables Categóricas
    with tabs[2]:
        categorical_variables_tab(df_flats)

    # Pestaña Correlación
    with tabs[3]:
        correlation_tab(df_flats)

    # Target
    with tabs[4]:
        target_tab(df_flats)

    # Nulos
    with tabs[5]:
        nulls_tab(df_flats)

    # Outliers
    with tabs[6]:
        outliers_tab(df_flats)

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
    model = load_model('./model/modelo_xgboost.pkl')
    encoders = load_encoders('./model/encoders.pkl')
    
    st.title('Predicción con XGBoost')
    st.write("Ingresa los datos para realizar una predicción")

    distrito_options = df_flats['distrito'].unique().tolist()
    status_options = df_flats['STATUS'].unique().tolist()
    area_max = float(df_flats['AREA'].max())
    area_min = float(df_flats['AREA'].min())
    area_median = float(df_flats['AREA'].median())
    room_max = df_flats['ROOMNUMBER'].max()
    bath_max = df_flats['BATHNUMBER'].max()
    
    # Valores de referencia para los sliders (ajusta según necesites)
    area_min = 20
    area_median = 50

    # Disposición de los sliders en una misma fila
    col1, col2, col3 = st.columns(3)

    with col1:
        area = st.slider('Área (m²)', min_value=area_min, max_value=area_median * 5, value=area_median)
    with col2:
        roomnumber = st.slider('Número de habitaciones', min_value=1, max_value=15, value=3)
    with col3:
        bathnumber = st.slider('Número de baños', min_value=1, max_value=10, value=2)

    # Espaciado entre secciones
    st.markdown("---")

    # Disposición de los radio buttons en otra fila
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        studio = st.radio('¿Es estudio?', ['Sí', 'No'], horizontal=True)
    with col2:
        ispenthouse = st.radio('¿Es ático?', ['Sí', 'No'], horizontal=True)
    with col3:
        duplex = st.radio('¿Es dúplex?', ['Sí', 'No'], horizontal=True)
    with col4:
        swimmingpool = st.radio('¿Tiene piscina?', ['Sí', 'No'], horizontal=True)
    with col5:
        elevator = st.radio('¿Tiene ascensor?', ['Sí', 'No'], horizontal=True)

    # Distribuir "Distrito" y "Barrio" en una misma línea
    col1, col2 = st.columns(2)

    with col1:
        distrito = st.selectbox('Distrito', distrito_options)

    with col2:
        # Filtrar barrios según el distrito seleccionado
        barrio_options = df_flats[df_flats['distrito'] == distrito]['barrio'].unique().tolist()
        barrio = st.selectbox('Barrio', barrio_options)

    # Espaciado entre secciones
    st.markdown("---")

    # Seleccionar status en una nueva línea
    status = st.selectbox('Status', status_options)

    # Crear un DataFrame con los datos de entrada
    input_data = pd.DataFrame([[area, roomnumber, bathnumber, studio, ispenthouse, duplex,
                                swimmingpool, elevator, barrio, distrito, status]],
                                columns=['area', 'roomnumber', 'bathnumber', 'studio', 'ispenthouse', 'duplex',
                                         'swimmingpool', 'elevator', 'barrio', 'distrito', 'status'])

    # Procesar los datos: convertir columnas binarias y codificar las categóricas
    input_data = convert_binary_columns(input_data)
    input_data = encode_categorical_columns(input_data, encoders)

    # Realizar la predicción cuando el usuario presione un botón
    if st.button('Realizar predicción'):
        # Realizar la predicción usando el modelo cargado
        prediction = model.predict(input_data)
        
        # Mostrar el resultado de la predicción
        st.write(f"Predicción: {prediction[0]}")
    
        
   
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