import folium
from streamlit_folium import folium_static
import streamlit as st

def mostrar_mapa_y_tabla(gdf, lista, median, m):
    col1, col2 = st.columns(2, border=True)
    
    with col1:
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
    
    with col2:
        st.table(median)