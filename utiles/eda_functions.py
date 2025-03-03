import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def general_tab(df):
    st.header("General")
    st.write("Vista previa del dataset:")
    st.write(df.head())
    st.write("Dimensiones del dataset:")
    st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    st.write("Información del dataset:")
    st.write(df.info())

def descriptiva_tab(df):
    st.header("Descriptiva")
    st.write("Descripción estadística del dataset:")
    st.write(df.describe(include='all').T)

def numeric_variables_tab(df):
    st.header("Variables Numéricas")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    st.write("Descripción estadística de las variables numéricas:")
    st.write(df[numeric_cols].describe().T)
    st.write("Distribución de las variables numéricas:")
    for col in numeric_cols:
        st.write(f"Distribución de {col}:")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)

def categorical_variables_tab(df):
    st.header("Variables Categóricas")
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    st.write("Descripción de las variables categóricas:")
    for col in categorical_cols:
        st.write(f"Frecuencia de {col}:")
        st.write(df[col].value_counts())
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(y=df[col], ax=ax)
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