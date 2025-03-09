import pickle

# Función para cargar el modelo entrenado
def load_model(model_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# Función para cargar los encoders
def load_encoders(encoders_path):
    with open(encoders_path, 'rb') as encoders_file:
        encoders = pickle.load(encoders_file)
    return encoders