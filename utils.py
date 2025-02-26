# utils.py
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def convert_to_wgs84(df, x_col, y_col, original_crs):
    """
    Convierte las coordenadas de un DataFrame a WGS84.

    Parameters:
    df (pd.DataFrame): DataFrame original con columnas de coordenadas.
    x_col (str): Nombre de la columna que contiene las coordenadas x.
    y_col (str): Nombre de la columna que contiene las coordenadas y.
    original_crs (int): EPSG code del CRS original de las coordenadas.

    Returns:
    pd.DataFrame: DataFrame con columnas 'latitude' y 'longitude' en WGS84.
    """
    # Crear una columna 'geometry' con puntos a partir de las coordenadas 'x' y 'y'
    df['geometry'] = df.apply(lambda row: Point(row[x_col], row[y_col]), axis=1)

    # Convertir el DataFrame a un GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Definir el CRS original de las coordenadas
    gdf.set_crs(epsg=original_crs, inplace=True)

    # Convertir las coordenadas a WGS84
    gdf = gdf.to_crs(epsg=4326)

    # Extraer las coordenadas convertidas y añadirlas al DataFrame original
    df['latitude'] = gdf.geometry.y
    df['longitude'] = gdf.geometry.x

    # Eliminar la columna 'geometry' si no es necesaria
    df.drop(columns='geometry', inplace=True)

    return df

def calculate_map_center(df, lat_col='latitude', lon_col='longitude'):
    """
    Calcula el centro del mapa a partir de las coordenadas.

    Parameters:
    df (pd.DataFrame): DataFrame con columnas de coordenadas.
    lat_col (str): Nombre de la columna que contiene las latitudes.
    lon_col (str): Nombre de la columna que contiene las longitudes.

    Returns:
    tuple: Coordenadas del centro del mapa (latitud, longitud).
    """
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()
    return center_lat, center_lon