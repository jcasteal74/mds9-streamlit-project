import streamlit as st
import base64

# Función para convertir imagen a Base64
def image_to_base64(image_path):
    """Convierte una imagen en Base64 para incrustarla en HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
def set_config():
    # Configuración de la página
    st.set_page_config(
        page_title="Housevidsor",
        layout="centered",
        page_icon="./resources/precio200x200.png"
    )

def initialization_streamlit_page():
    # Obtener imagen en Base64
    banner_base64 = image_to_base64("./resources/banner.webp")
    # Mostrar el banner
    render_banner(banner_base64)

# HTML con la imagen en Base64
def render_banner(image_base64):
    """Renderiza un banner en HTML usando una imagen en Base64."""
    banner_html = f"""
    <style>
    .banner {{
        width: 100%;
        height: auto;
    }}
    </style>
    <img src="data:image/webp;base64,{image_base64}" class="banner">
    """
    st.markdown(banner_html, unsafe_allow_html=True)


