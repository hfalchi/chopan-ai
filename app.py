import streamlit as st
import google.generativeai as genai
from prompts import SYSTEM_INSTRUCTION

# 1. Configuración de la Página
st.set_page_config(page_title="Asistente Chopan - Pre-Sales Tech ", page_icon="🧮", layout="wide")

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
    model_name="gemini-1.5-pro", # O usa "gemini-1.5-pro-latest"
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

st.caption("Sistema impulsado por Gemini 1.5 Pro - Configurado con Heurísticas Internas")
