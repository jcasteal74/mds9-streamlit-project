import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import io

def general_tab(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.header("General")
    st.write("Vista previa del dataset:")
    st.write(df.head())
    st.write("Dimensiones del dataset:")
    st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    st.write("Información del dataset:")
    st.text(s)

def descriptiva_tab(df):
    st.header("Descriptiva")
    st.write("Descripción estadística del dataset:")
    st.write(df.describe(include='all').T)

def target_tab(df):
    st.subheader("Select target column:")    
    target_column = st.selectbox("", df.columns, index = len(df.columns) - 1)

    st.subheader("Histogram of target column")
    fig = px.histogram(df, x = target_column)
    c1, c2, c3 = st.columns([0.5, 2, 0.5])
    c2.plotly_chart(fig)



def numeric_variables_tab(df):
    st.header("Variables Numéricas")
    
    # Seleccionar columnas numéricas
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Si no hay columnas numéricas, mostrar un mensaje
    if len(numeric_cols) == 0:
        st.write("No hay variables numéricas en el DataFrame.")
        return
    
    # Mostrar descripción estadística de las variables numéricas
    st.write("Descripción estadística de las variables numéricas:")
       
    # Seleccionar una variable numérica
    selected_col = st.selectbox("Selecciona una variable numérica", numeric_cols)
    
    # Mostrar la distribución de la variable seleccionada
    st.write(f"Distribución de {selected_col}:")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df[selected_col], kde=True, ax=ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    st.write(df[numeric_cols].describe().T)


def categorical_variables_tab(df):
    st.header("Variables Categóricas")
    
    # Seleccionar columnas categóricas
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # Si no hay columnas categóricas, mostrar un mensaje
    if len(categorical_cols) == 0:
        st.write("No hay variables categóricas en el DataFrame.")
        return
    
    # Seleccionar una variable categórica
    selected_col = st.selectbox("Selecciona una variable categórica", categorical_cols)
    
    # Mostrar la tabla de frecuencias
    st.write(f"Frecuencia de {selected_col}:")
    st.write(df[selected_col].value_counts())
    
    # Graficar la variable seleccionada
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(y=df[selected_col], ax=ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def correlation_tab(df):
    st.header("Correlación")
    st.write("Matriz de correlación:")
    columnas_numericas = df.select_dtypes(include=['number']).columns
    corr_matrix = df[columnas_numericas].corr()
    st.write(corr_matrix)
    st.write("Mapa de calor de la matriz de correlación:")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)