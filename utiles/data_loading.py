import geopandas as gpd
import pandas as pd
import streamlit as st

@st.cache_data
def load_geodata(zip_path):
    return gpd.read_file(f"zip://{zip_path}")

@st.cache_data
def load_flats_data(excel_path):
    return pd.read_csv(excel_path, sep=';')