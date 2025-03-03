import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_price_distribution(df):
    st.header("Distribución de Precios por Barrio y Distrito")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='barrio', y='PRICE', hue='distrito', data=df, ax=ax)
    ax.set_title('Distribución de Precios por Barrio y Distrito')
    ax.set_xlabel('Barrio')
    ax.set_ylabel('Precio')
    st.pyplot(fig)
    
def plot_area_vs_price(df):
    st.header("Relación entre Área y Precio")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='AREA', y='PRICE', data=df, ax=ax)
    ax.set_title('Relación entre Área y Precio')
    ax.set_xlabel('Área')
    ax.set_ylabel('Precio')
    st.pyplot(fig)
    
def plot_rooms_baths_vs_price(df):
    st.header("Número de Habitaciones y Baños por Precio")
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(df['ROOMNUMBER'], df['BATHNUMBER'], s=df['PRICE'] / 1000, alpha=0.5)
    ax.set_title('Número de Habitaciones y Baños por Precio')
    ax.set_xlabel('Número de Habitaciones')
    ax.set_ylabel('Número de Baños')
    st.pyplot(fig)
    
def plot_property_types(df):
    st.header("Distribución de Tipos de Propiedades")
    property_types = ['STUDIO', 'ISPENTHOUSE', 'DUPLEX']
    for prop in property_types:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(x=prop, hue='STATUS', data=df, ax=ax)
        ax.set_title(f'Distribución de {prop}')
        st.pyplot(fig)
        
def plot_amenities_vs_price(df):
    st.header("Impacto de Amenidades en el Precio")
    amenities = ['SWIMMINGPOOL', 'ELEVATOR']
    for amenity in amenities:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(x=amenity, y='PRICE', data=df, ax=ax)
        ax.set_title(f'Impacto de {amenity} en el Precio')
        st.pyplot(fig)
        
        