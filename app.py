import streamlit as st
import google.generativeai as genai
import os
import base64 
import textwrap
from prompts import SYSTEM_INSTRUCTION

def get_img_as_base64(file_path):
    """Lee una imagen local y la convierte a base64."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# 1. Configuración de la Página
st.set_page_config(page_title="Asistente Chopan - Pre-Sales Tech ", page_icon="💀", layout="wide")

# --- ESTILO CYBERPUNK 2077 (ARASAKA RED) ---
st.markdown("""
    <style>
    /* Importamos la fuente 'Rajdhani' para que se vea igual al juego */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

    .block-container {
    padding-top: 2rem !important; /* Reduce el espacio arriba del título */
    padding-bottom: 2rem !important;
    }

    /* 1. Fondo Principal con efecto 'Scanline' sutil */
    .stApp {
        background-color: #050505;
        /* Un degradado sutil para simular pantalla vieja */
        background-image: linear-gradient(rgba(0, 0, 0, 0.1) 50%, rgba(0, 0, 0, 0.1) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%;
        color: #ff5f5f; /* Texto general en rojo suave */
        font-family: 'Rajdhani', sans-serif; /* Tipografía técnica */
    }

    /* 2. Títulos: Rojo intenso con borde lateral */
    h1, h2, h3 {
        color: #ff3838 !important; /* Rojo Neón */
        text-transform: uppercase;
        font-weight: 700;
        text-shadow: 0 0 10px #ff3838; /* Glow rojo */
        border-left: 5px solid #ff3838; /* Barra lateral estilo HUD */
        padding-left: 15px;
        background: linear-gradient(90deg, rgba(255,56,56,0.1) 0%, rgba(0,0,0,0) 100%);
    }

    /* 3. Cajas de Texto (Inputs): Fondo oscuro rojizo con texto Cian */
    .stTextArea textarea, .stTextInput input {
        background-color: #120505 !important; /* Casi negro rojizo */
        color: #2af5ff !important; /* Cian brillante para lo que escribe el usuario (Contrast) */
        border: 1px solid #ff3838 !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 18px;
    }
    
    /* Etiquetas y textos pequeños */
    label, .stMarkdown p, .stCaption {
        color: #ff5f5f !important;
        letter-spacing: 1px;
    }

    /* 4. Botones: Estilo 'Hacking' (Cian y Transparente) */
    div.stButton > button {
        background-color: transparent;
        color: #2af5ff; /* Texto Cian */
        border: 2px solid #2af5ff;
        border-radius: 0px; /* Bordes duros */
        padding: 10px 25px;
        text-transform: uppercase;
        font-weight: bold;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 0 5px #2af5ff;
    }

    div.stButton > button:hover {
        background-color: #2af5ff;
        color: #000; /* Texto negro al pasar el mouse */
        box-shadow: 0 0 20px #2af5ff, inset 0 0 10px #2af5ff;
        border-color: #2af5ff;
    }

    /* 5. Spinners y Barras de carga */
    .stSpinner > div {
        border-top-color: #2af5ff !important;
    }

    /* Input de texto: Hacerlo parecer una consola */
    .stTextArea textarea {
        background-color: #000000 !important;
        border: 1px dashed #ff3838 !important; /* Borde punteado rojo */
        color: #2af5ff !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Efecto de foco cuando escribes */
    .stTextArea textarea:focus {
        box-shadow: 0 0 15px rgba(255, 56, 56, 0.3);
        border-left: 5px solid #ff3838 !important;
    }
    
    /* Botón de acción principal: Estilo 'Glitch' */
    div.stButton > button {
        width: 100%; /* Botón ancho completo */
        background: linear-gradient(45deg, transparent 5%, #ff3838 5%);
        color: #000;
        font-weight: 900;
        letter-spacing: 2px;
        border: none;
        clip-path: polygon(0 0, 100% 0, 100% 80%, 95% 100%, 0 100%); /* Corte en la esquina */
    }
    
    div.stButton > button:hover {
        background: linear-gradient(45deg, transparent 5%, #2af5ff 5%); /* Cambia a azul al pasar mouse */
        color: #000;
    }

    /* Ocultar elementos de Streamlit por defecto */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)
# -------------------------

# 2. Gestión de Secretos (API Key)
# Intenta obtener la key de st.secrets (Prod) o del entorno local
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("No se encontró la API Key. Configúrala en los secrets de Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Configuración del Modelo
# Usamos los parámetros que definimos: Temperatura baja para precisión.
generation_config = {
  "temperature": 0.2, # Crítico para mantener la coherencia matemática
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

# Inicializamos el modelo con la instrucción del sistema importada
model = genai.GenerativeModel(
       
    # Alternativas de modelos
    # model_name="gemini-3-pro-preview", 
    # model_name="gemini-2.5-pro",
    model_name="gemini-flash-latest",
    
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. Interfaz de Usuario (UI)
st.title("Chopan - AI")
st.markdown("""
Estimador de Requerimientos de Software
Sube una transcripción de reunión o pega un requerimiento. 
Chopan generará una estimación basada en las heurísticas de Envision.
""")

col1, col2 = st.columns([1, 1])

# Barra de estado superior
m1, m2, m3, m4 = st.columns(4)
m1.metric("LATENCY", "12ms", "-2ms")
m2.metric("TOKENS", "8K Limit", "READY")
m3.metric("SECURITY", "ENCRYPTED", "OK")
m4.metric("ESTIMATION_ENGINE", "ONLINE", "GEMINI-PRO")

st.divider() # Una línea divisoria

with col1:
    st.subheader("Entrada de Datos")
    input_method = st.radio("Fuente de información:", ["Pegar Texto", "Subir Archivo (.txt)"])
    
    user_prompt = ""
    
    if input_method == "Pegar Texto":
        user_prompt = st.text_area("Descripción del requerimiento:", height=300)
    else:
        uploaded_file = st.file_uploader("Sube la transcripción", type=["txt"])
        if uploaded_file is not None:
            user_prompt = uploaded_file.read().decode("utf-8")
            st.success("Archivo cargado con éxito")

    generate_btn = st.button("Generar Estimación", type="primary")

with col2:
    # 1. Configuración de imagen
    local_image_filename = "chopan2.gif"  
    img_base64 = get_img_as_base64(local_image_filename)

    # Lógica de respaldo
    if img_base64:
        img_src = f"data:image/png;base64,{img_base64}"
        status_text = "LOCAL_SOURCE_FOUND"
    else:
        # Imagen de respaldo online (Cyberpunk GIF)
        img_src = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmhzcXN4bnB5bmd4emF4eXJ5eXJ5eXJ5/L1k6lS3q/giphy.gif"
        status_text = "REMOTE_UPLINK_ESTABLISHED"

    # 3. Renderizado HTML con textwrap para evitar el error de indentación
    st.markdown(f"""
<div style="border: 1px solid #ff3838; padding: 10px; background-color: #050505;">
    <div style="color: #ff3838; font-size: 10px; font-weight: bold; margin-bottom: 5px; border-bottom: 1px dashed #ff3838; display: flex; justify-content: space-between;">
        <span>SYSTEM_MONITOR</span>
        <span style="color: #2af5ff;">STATUS: {status_text}</span>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 10px; background-color: #000; padding: 5px; border: 1px solid #ff3838;">
            <img src="{img_src}" style="width: 100%; height: auto; max-height: 300px; object-fit: cover; border: 1px solid #2af5ff; filter: sepia(100%) hue-rotate(190deg) saturate(300%);">
    </div>
    <div style="margin-top: 10px; font-size: 12px; color: #2af5ff; font-family: 'Courier New';">
        > TARGET: LOCKED <br>
        > AI_CORE: ONLINE <br>
        > MODE: ESTIMATION_V3
    </div>
</div>
""", unsafe_allow_html=True)
# 5. Resultados ---------------------       
    st.subheader("📊 Resultado")
    
    if generate_btn and user_prompt:
        with st.spinner('Analizando heurísticas y calculando esfuerzos...'):
            try:
                # Llamada a la API
                response = model.generate_content(user_prompt)
                
                # Mostrar resultado
                st.markdown(response.text)
                
                # Botón para descargar el reporte (Opcional pero útil)
                st.download_button(
                    label="Descargar Estimación (MD)",
                    data=response.text,
                    file_name="estimacion_proyecto.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    elif generate_btn and not user_prompt:
        st.warning("Por favor ingresa un texto o sube un archivo.")

# Footer informativo
st.divider()

st.caption("Sistema impulsado por Gemini 3 Pro - Configurado con Heurísticas Internas")


