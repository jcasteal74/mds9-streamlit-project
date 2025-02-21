import pandas as pd
from dotenv import load_dotenv
import os
import base64
import json
import urllib
import requests as rq

load_dotenv()


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


source2 = "./data/municipios.xlsx"

df = pd.read_excel(source2, decimal=',')

# Coordenadas de la ubicación (latitud, longitud)
latitud = 40.7128  # Nueva York
longitud = -74.0060  # Nueva York

radio = 5

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

url = ('https://api.idealista.com/3.5/'+country+'/search?operation='+operation+#"&locale="+locale+
           '&maxItems='+max_items+
           '&order='+order+
           '&center='+center+
           '&distance='+distance+
           '&propertyType='+property_type+
           '&sort='+sort+ 
           '&numPage=%s'+
           '&language='+language)

print(url)

tokkken = get_oauth_token()

print(f"{tokkken}")
