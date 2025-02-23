import streamlit as st
import pandas as pd
import altair as alt

# Título de la aplicación
st.title("Análisis Exploratorio de Datos (EDA) Sencillo")

# Subir archivo
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file)

    # Mostrar el DataFrame
    st.subheader(f"Datos del archivo: {uploaded_file.name}")
    st.write(df)

    # Mostrar información básica
    st.subheader("Información básica")
    st.write(df.info())

    # Mostrar estadísticas descriptivas
    st.subheader("Estadísticas descriptivas")
    st.write(df.describe().T)

    # Mostrar gráficos
    st.subheader("Gráficos")

    # Seleccionar columna para gráfico de barras
    column = st.selectbox("Selecciona una columna para el gráfico de barras", df.columns)
    st.bar_chart(df[column].value_counts())

    st.subheader("Gráfico de dispersión")

    # Selección de columnas numéricas
    num_columns = df.select_dtypes(include=['number']).columns.tolist()

    x_axis = st.selectbox("Selecciona la columna para el eje X", num_columns)
    y_axis = st.selectbox("Selecciona la columna para el eje Y", num_columns)

    st.write(f"Gráfico de dispersión entre {x_axis} y {y_axis}")

    # Crear gráfico con Altair
    scatter = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X(x_axis, title=x_axis),
        y=alt.Y(y_axis, title=y_axis),
        tooltip=[x_axis, y_axis]
    ).interactive()

    st.altair_chart(scatter, use_container_width=True)

else:
    st.write("Por favor, sube un archivo Excel para comenzar el análisis.")