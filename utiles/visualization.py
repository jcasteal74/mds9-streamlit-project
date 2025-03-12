import folium
from streamlit_folium import folium_static
import streamlit as st

def mostrar_mapa_y_tabla(gdf, lista, median, m):
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
    folium_static(m)
