import streamlit as st
import google.generativeai as genai
from prompts import SYSTEM_INSTRUCTION

# 1. Configuración de la Página
st.set_page_config(page_title="Asistente Chopan - Pre-Sales Tech ", page_icon="🧮", layout="wide")

# --- ESTILO CYBERPUNK ---
st.markdown("""
    <style>
    /* 1. Fondo Principal y Tipografía General */
    .stApp {
        background-color: #050505; /* Casi negro */
        color: #00FF41; /* Verde Terminal 'Matrix' */
        font-family: 'Courier New', Courier, monospace; /* Fuente monoespaciada */
    }

    /* 2. Títulos (H1, H2, H3) con efecto Glow */
    h1, h2, h3 {
        color: #00FF41 !important;
        text-shadow: 0 0 5px #00FF41, 0 0 10px #00FF41; /* Efecto neón */
        border-bottom: 1px dashed #00FF41;
        padding-bottom: 10px;
    }

    /* 3. Ajuste de Inputs (Text Areas, File Uploaders) */
    .stTextArea textarea, .stTextInput input {
        background-color: #111 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Etiqueta de los inputs */
    label, .stMarkdown p {
        color: #00FF41 !important;
    }

    /* 4. Botones Estilo Cyberpunk */
    div.stButton > button {
        background-color: #000000;
        color: #00FF41;
        border: 1px solid #00FF41;
        border-radius: 0px; /* Bordes cuadrados */
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-weight: bold;
        box-shadow: 0 0 5px #00FF41;
    }

    div.stButton > button:hover {
        background-color: #00FF41;
        color: #000000;
        box-shadow: 0 0 15px #00FF41;
    }

    /* 5. Ajuste de Alertas y Spinners */
    .stSpinner > div {
        border-top-color: #00FF41 !important;
    }
    
    /* Ocultar el menú hamburguesa superior derecho y footer para más inmersión (opcional) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
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
st.title("🤖 Chopan - Estimador de Requerimientos de Software")
st.markdown("""
Sube una transcripción de reunión o pega un requerimiento. 
La IA generará una estimación basada en las heurísticas históricas de la empresa.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Entrada de Datos")
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
    # --- NUEVO CÓDIGO: EL ROSTRO DEL ASISTENTE ---
    # Centramos la imagen usando columnas dentro de la columna para controlar el tamaño
    c_izq, c_centro, c_der = st.columns([1, 2, 1]) 
    
    with c_centro:
        # Reemplaza 'ai_assistant.gif' con el nombre real de tu archivo
        # Si usas un video mp4, cámbialo por st.video("video.mp4", loop=True, autoplay=True, muted=True)
        st.image("chopan.gif", use_container_width=True) 
        
        # Opcional: Un pequeño texto de estado debajo del rostro
        st.caption("🤖 *Hit me with something chum...*", help="Soy Chopan")

    st.divider()
    # ---------------------------------------------

           
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







