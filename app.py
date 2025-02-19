import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Análisis Exploratorio de Datos (EDA) Sencillo")

# Subir archivo
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file)

    # Mostrar el DataFrame
    st.subheader("Datos del archivo")
    st.write(df)

    # Mostrar información básica
    st.subheader("Información básica")
    st.write(df.info())

    # Mostrar estadísticas descriptivas
    st.subheader("Estadísticas descriptivas")
    st.write(df.describe())

    # Mostrar gráficos
    st.subheader("Gráficos")

    # Seleccionar columna para gráfico de barras
    column = st.selectbox("Selecciona una columna para el gráfico de barras", df.columns)
    st.bar_chart(df[column].value_counts())

    # Seleccionar columnas para gráfico de dispersión
    st.subheader("Gráfico de dispersión")
    x_axis = st.selectbox("Selecciona la columna para el eje X", df.columns)
    y_axis = st.selectbox("Selecciona la columna para el eje Y", df.columns)
    st.write("Gráfico de dispersión entre", x_axis, "y", y_axis)
    st.scatter_chart(df[[x_axis, y_axis]])

else:
    st.write("Por favor, sube un archivo Excel para comenzar el análisis.")