import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import json
import urllib
import requests as rq
import base64
import os
from dotenv import load_dotenv

load_dotenv()



def obtener_coordenadas(df, localidad):
    df_filtrado = df[df['NOMBRE_ACTUAL'] == localidad]
    latitud = df_filtrado['LATITUD_ETRS89'].values[0]
    longitud = df_filtrado['LONGITUD_ETRS89'].values[0]
    return latitud, longitud  

def get_oauth_token(): 
    url = "https://api.idealista.com/oauth/token"    
    apikey = os.getenv('IDEALISTA_API_KEY')
    secret = os.getenv('IDEALISTA_SECRET')
    apikey_secret = apikey + ':' + secret
    auth = str(base64.b64encode(bytes(apikey_secret, 'utf-8')))[2:][:-1]
    headers = {'Authorization' : 'Basic ' + auth, 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    params = urllib.parse.urlencode({'grant_type':'client_credentials'})
    content = rq.post(url, headers=headers, params=params)
    if content.status_code != 200:
        st.error(f"Error al obtener el token de autenticación: {content.status_code} - {content.text}")
        return None
    bearer_token = json.loads(content.text)['access_token']
    return bearer_token

def search_api(token, URL):  
    headers = {'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + token}
    content = rq.post(URL, headers=headers)
    if content.status_code != 200:
        st.error(f"Error en la llamada a la API: {content.status_code} - {content.text}")
        return None
    try:
        result = json.loads(content.text)
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar la respuesta JSON: {e}")
        st.write(content.text)  # Mostrar la respuesta para depuración
        return None
    return result

# Configuración de la página
st.set_page_config(page_title="Viviendas", page_icon="🏠")

st.image("./data/imagen_ppal.webp", caption="HouseFinder", use_container_width=True)

# Cargar datos
df = pd.read_excel("./data/municipios.xlsx", engine="openpyxl")


# Seleccionar provincia
provincias = df['PROVINCIA'].unique()
provincia = st.selectbox('Selecciona una Provincia', provincias)

# Filtrar poblaciones según la provincia seleccionada
df_filtrado_provincia = df[df['PROVINCIA'] == provincia]
poblaciones = df_filtrado_provincia['NOMBRE_ACTUAL'].unique()
poblacion = st.selectbox('Selecciona una Población', poblaciones)

# Crear slider para seleccionar el radio
radio = st.slider('Radio (km)', min_value=5, max_value=50, step=5, value=10)

# Obtener coordenadas de la población seleccionada
latitud, longitud = obtener_coordenadas(df, poblacion)

# Parámetros de la API
country = 'es' #values: es, it, pt
locale = 'es' #values: es, it, pt, en, ca
language = 'es' #
max_items = '50'
operation = 'sale'  #operation = 'rent' 
property_type = 'homes'
order = 'priceDown' 
center = f'{latitud},{longitud}'
distance = f'{radio*1000}'
sort = 'desc'
bankOffer = 'false'

df_tot = pd.DataFrame()
limit = 10


 
    
for i in range(1,limit):
    url = ('https://api.idealista.com/3.5/'+country+'/search?operation='+operation+#"&locale="+locale+
           '&maxItems='+max_items+
           '&order='+order+
           '&center='+center+
           '&distance='+distance+
           '&propertyType='+property_type+
           '&sort='+sort+ 
           '&numPage=%s'+
           '&language='+language) %(i)  
    a = search_api(get_oauth_token(), url)
    df = pd.DataFrame.from_dict(a['elementList'])
    df_tot = pd.concat([df_tot,df])

# Mostrar resultados
# Crear un mapa centrado en la primera vivienda
if not df_tot.empty:
    m = folium.Map(location=[df_tot.iloc[0]["lat"], df_tot.iloc[0]["lon"]], zoom_start=12)

    # Agregar marcadores para cada vivienda
    for _, row in df_tot.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=row["name"],
        ).add_to(m)

    # Mostrar el mapa en Streamlit
    st_folium(m, width=700, height=500)
else:
    st.write("No hay viviendas para mostrar.")
