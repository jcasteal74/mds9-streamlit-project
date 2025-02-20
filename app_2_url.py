import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from dotenv import load_dotenv
from folium.plugins import MarkerCluster

load_dotenv()

url = 'https://raw.githubusercontent.com/JimenaAreta/thevalley-MDS/refs/heads/jimena/datasets/sample-flats-madrid-synthetic-coords.csv'



# Configuración de la página
st.set_page_config(page_title="Viviendas", page_icon="🏠")

st.image("./data/imagen_ppal.webp", caption="HouseFinder", use_container_width=True)

# Cargar el dataset

def load_data():
    # Aquí cambia la ruta a tu archivo CSV
    data = pd.read_csv(url)
    return data

# Cargar los datos
df = load_data()

# Visualización con pydeck (utilizando las coordenadas UTM)
st.title("Mapa interactivo de coordenadas UTM")

# Crear un selector para elegir el LOCATIONNAME
location_name = st.selectbox(
    'Selecciona un lugar:',
    df['LOCATIONNAME'].unique()  # Extraemos todos los nombres únicos de LOCATIONNAME
)

# Filtramos el dataframe por el LOCATIONNAME seleccionado
df_filtered = df[df['LOCATIONNAME'] == location_name]

st.write(df_filtered.columns)

# Verifica si hay datos para el lugar seleccionado
if not df_filtered.empty:
    st.write(f"Mostrando {len(df_filtered)} puntos para {location_name}")
    
    st.map(df_filtered, longitude="Y", latitude="X")
else:
    st.write(f"No hay datos para {location_name}.")