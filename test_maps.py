import streamlit as st
import pandas as pd
import numpy as np
import pyproj

url = 'https://raw.githubusercontent.com/JimenaAreta/thevalley-MDS/refs/heads/jimena/datasets/sample-flats-madrid-synthetic-coords.csv'



@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

# Función para convertir UTM a geográficas
def utm_to_geographic(easting, northing, zone_number):
    # Crear el transformador de coordenadas UTM a geográficas
    wgs84 = pyproj.CRS("EPSG:4326")  # Sistema de coordenadas geográficas (lat/lon)
    utm = pyproj.CRS(f"EPSG:326{zone_number}")  # Sistema de coordenadas UTM (zona específica)
    
    # Crear un transformador para convertir de UTM a WGS84
    transformer = pyproj.Transformer.from_crs(utm, wgs84, always_xy=True)
    
    # Realizar la conversión
    lon, lat = transformer.transform(easting, northing)
    
    return lat, lon


df=load_data(url)

# Asumimos que la zona es la 30T (para Madrid)
zone_number = 30

# Convertir las coordenadas UTM a geográficas y agregar nuevas columnas
df[['Latitud', 'Longitud']] = df.apply(lambda row: pd.Series(utm_to_geographic(row['X'], row['Y'], zone_number)), axis=1)

# Visualización con pydeck (utilizando las coordenadas UTM)
st.title("Mapa interactivo🗺️")

# Crear un selector para elegir el LOCATIONNAME
location_name = st.selectbox(
    'Selecciona un lugar:',
    df['LOCATIONNAME'].unique()  # Extraemos todos los nombres únicos de LOCATIONNAME
)

# Filtramos el dataframe por el LOCATIONNAME seleccionado
df_filtered = df[df['LOCATIONNAME'] == location_name]


# Verifica si hay datos para el lugar seleccionado
if not df_filtered.empty:
    st.write(f"Mostrando {len(df_filtered)} puntos para {location_name}")
    
    st.map(df_filtered, longitude="Longitud", latitude="Latitud", size=15, color="#0044ff")
else:
    st.write(f"No hay datos para {location_name}.")

