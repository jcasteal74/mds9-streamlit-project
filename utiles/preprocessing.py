import pandas as pd

# Función para transformar las entradas categóricas usando los encoders
def encode_categorical_columns(input_data, encoders):
    input_data['barrio_encoded'] = encoders['barrio'].transform(input_data['barrio'])
    input_data['distrito_encoded'] = encoders['distrito'].transform(input_data['distrito'])
    input_data['status_encoded'] = encoders['status'].transform(input_data['status'])
    
    # Eliminar las columnas originales
    input_data = input_data.drop(columns=['barrio', 'distrito', 'status'])
    
    return input_data

# Función para convertir las respuestas 'Sí'/'No' a valores binarios
def convert_binary_columns(input_data):
    binary_columns = ['studio', 'ispenthouse', 'duplex', 'swimmingpool', 'elevator']
    for col in binary_columns:
        input_data[col] = input_data[col].map({'Sí': 1, 'No': 0})
    return input_data