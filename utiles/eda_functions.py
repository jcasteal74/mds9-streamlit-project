import streamlit as st
import plotly.express as px
import io
import plotly.figure_factory as ff
import pandas as pd


def general_tab(df):
    df.columns = df.columns.str.replace(' ', '_')  
    df_summary = pd.DataFrame({
        'Column': df.columns,
        'Non-Null Count': df.notnull().sum(),
        'Data Type': df.dtypes.astype(str)
    }).reset_index(drop=True)
    
    return df_summary


def descriptiva_tab(df):
    st.header("Descriptiva")
    st.write("Descripción estadística del dataset:")
    st.write(df.describe(include='all').T)

def target_tab(df):
    st.subheader("Select target column:")    
    target_column = st.selectbox("", df.columns, index = len(df.columns) - 1)

    st.subheader(f"Histogram of target column: {target_column}")
    fig = px.histogram(df, x = target_column)
    c1, c2, c3 = st.columns([0.5, 2, 0.5])
    c2.plotly_chart(fig)



# def numeric_variables_tab(df):
#     st.subheader("Select numeric column:") 
    
#     # Seleccionar columnas numéricas
#     numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
#     # Si no hay columnas numéricas, mostrar un mensaje
#     if len(numeric_cols) == 0:
#         st.write("☢️Numerical columns doesn't exist!")
#         return
    
#     # Mostrar descripción estadística de las variables numéricas
#     st.write("Descripción estadística de las variables numéricas:")
       
#     # Seleccionar una variable numérica
#     selected_col = st.selectbox("Selecciona una variable numérica", numeric_cols)
    
#     # Mostrar la distribución de la variable seleccionada
#     st.subheader(f"Histogram of target column: {selected_col}")
#     fig = px.histogram(df, x = selected_col)
#     c1, c2, c3 = st.columns([0.5, 2, 0.5])
#     c2.plotly_chart(fig)


def numeric_variables_tab(df):
    st.subheader("Selecciona una columna numérica:") 
    
    # Seleccionar columnas numéricas
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Si no hay columnas numéricas, mostrar un mensaje y salir
    if len(numeric_cols) == 0:
        st.write("☢️ No existen columnas numéricas en el dataset.")
        return
    
    # Mostrar descripción estadística de las variables numéricas
    st.write("📊 **Descripción estadística de las variables numéricas:**")
    st.write(df[numeric_cols].describe().T.style.format("{:.2f}"))  # Formatear con 2 decimales

    # Seleccionar una variable numérica
    selected_col = st.selectbox("📌 **Selecciona una variable numérica**", numeric_cols)
    
    # Crear histogram + boxplot en columnas
    c1, c2 = st.columns(2)

    # Histograma
    with c1:
        st.subheader("📊 Histograma")
        fig_hist = px.histogram(df, x=selected_col, nbins=30, 
                                title=f"Distribución de {selected_col}", 
                                color_discrete_sequence=["royalblue"])
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)

    # Boxplot
    with c2:
        st.subheader("📦 Boxplot")
        fig_box = px.box(df, y=selected_col, 
                         title=f"Boxplot de {selected_col}", 
                         color_discrete_sequence=["indianred"])
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)


    
    #st.write(df[selected_col].describe().T)


def categorical_variables_tab(df):
    st.header("Variables Categóricas")
    
    # Seleccionar columnas categóricas
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # Si no hay columnas categóricas, mostrar un mensaje
    if len(categorical_cols) == 0:
        st.write("No hay variables categóricas en el DataFrame.")
        return
    
    # Aplicar formato solo a las columnas numéricas de la descripción
    desc = df[categorical_cols].describe().T
    st.write(desc.style.format({"count": "{:.0f}", "freq": "{:.0f}"}))  # Solo formateamos valores numéricos
    
    # Seleccionar una variable categórica
    selected_col = st.selectbox("Selecciona una variable categórica", categorical_cols)
    
    # Calcular frecuencias relativas
    value_counts = df[selected_col].value_counts(normalize=True).mul(100).reset_index()
    value_counts.columns = [selected_col, "Porcentaje"]


        # Crear gráfico de barras con Plotly
    fig = px.bar(
        value_counts, 
        x=selected_col, 
        y="Porcentaje", 
        text=value_counts["Porcentaje"].apply(lambda x: f"{x:.2f}%"),
        title=f"Distribución de {selected_col}",
        labels={selected_col: selected_col, "Porcentaje": "Porcentaje (%)"},
        color="Porcentaje",  # Color según valor
        color_continuous_scale="Blues",  # Paleta de colores
)

    # Ajustes adicionales
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)  # Rotar etiquetas si hay muchas categorías

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig)

    
def correlation_tab(df):
    st.header("Correlación")
    
    # Seleccionar solo columnas numéricas
    columnas_numericas = df.select_dtypes(include=['number']).columns
    corr_matrix = df[columnas_numericas].corr()

    # Mostrar la matriz de correlación en tabla
    #st.write("Matriz de correlación:")
    #st.write(corr_matrix.style.format("{:.2f}"))  # Formato con 2 decimales

    # Crear un heatmap interactivo con Plotly
    st.write("Mapa de calor de la matriz de correlación:")
    fig = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        annotation_text=corr_matrix.round(2).values,
        colorscale="RdBu_r",  # Escala de color rojo-azul inverso (útil para correlación)
        showscale=True
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

def nulls_tab(df):
    st.subheader('NA Value Information:')
    if df.isnull().sum().sum() == 0:
        st.write('There is not any NA value in your dataset.')
    else:
        c1, c2, c3 = st.columns([0.5, 2, 0.5])
        c2.dataframe(df_isnull(df), width=1500)
        space(2)

def df_isnull(df):
    res = pd.DataFrame(df.isnull().sum()).reset_index()
    res['Percentage'] = round(res[0] / df.shape[0] * 100, 2)
    res['Percentage'] = res['Percentage'].astype(str) + '%'
    return res.rename(columns = {'index':'Column', 0:'Number of null values'})

def outliers_tab(df):
    st.subheader('Outlier Analysis')
    c1, c2, c3 = st.columns([1, 2, 1])
    c2.dataframe(number_of_outliers(df))

def number_of_outliers(df):
    # Seleccionar solo columnas numéricas
    df_numeric = df.select_dtypes(exclude="object")
    
    # Calcular Q1, Q3 e IQR
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1

    # Determinar valores atípicos
    outliers = ((df_numeric < (Q1 - 1.5 * IQR)) | (df_numeric > (Q3 + 1.5 * IQR)))

    # Contar outliers por columna
    count_outliers = outliers.sum()
    
    # Calcular el porcentaje de outliers
    percentage_outliers = (count_outliers / len(df)) * 100

    # Crear DataFrame con resultados
    outliers_df = pd.DataFrame({
        "column": df_numeric.columns,
        "count_of_outliers": count_outliers.values,
        "percentage_of_outliers": percentage_outliers.values
    })

    # Formatear el porcentaje con 2 decimales
    outliers_df["percentage_of_outliers"] = outliers_df["percentage_of_outliers"].map("{:.2f}%".format)

    # Ordenar de menor a mayor porcentaje de outliers
    outliers_df = outliers_df.sort_values(by="percentage_of_outliers", ascending=False)

    return outliers_df

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")