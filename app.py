import streamlit as st
import pandas as pd
import json
import os

# ====================== ASISTENTE BÁSICO ======================
def asistente_basico(pregunta, momento="post"):
    if momento == "post":
        if "prote" in pregunta.lower() or "proteína" in pregunta.lower():
            return "Después de entrenar prioriza **proteína alta**: Pollo, Batido whey, Yogurt griego, Salmón o Pechuga."
        elif "cans" in pregunta.lower() or "fatiga" in pregunta.lower() or "cansado" in pregunta.lower():
            return "Estás cansado? Te recomiendo Batido de proteína + banana o Yogurt griego con miel."
        else:
            return "Después de entrenar combina **proteína + carbohidratos** en los primeros 60 minutos para recuperar mejor."
    else:
        return "Antes de entrenar carga energía con carbohidratos complejos: Avena con frutas, Banana con crema de maní o Arroz integral."

# ====================== CONFIGURACIÓN PWA ======================
st.set_page_config(
    page_title="NutriFit",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'About': "NutriFit v2.0 - Tu coach nutricional"}
)

# Meta tags para PWA
st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <link rel="manifest" href="/manifest.json">
        <meta name="theme-color" content="#00cc66">
    </head>
""", unsafe_allow_html=True)

# Estilo moderno tipo App
st.markdown("""
<style>
    .main {background-color: #0f0f0f; color: #ffffff;}
    .stButton>button {background-color: #00cc66; color: white; border-radius: 12px; height: 52px; font-size: 16px; font-weight: bold;}
    .stButton>button:hover {background-color: #00b35a;}
    .expander {border-radius: 12px; border: 1px solid #333333;}
    h1, h2, h3 {color: #ffffff;}
    .stTextInput>div>div>input {background-color: #1f1f1f; color: white; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

st.title("💪 NutriFit")
st.subheader("Tu coach nutricional")

# Cargar datos
df = pd.read_csv("alimentos.csv", encoding="utf-8")

# Sistema de favoritos
FAVORITES_FILE = "data/favoritos.json"

def cargar_favoritos():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_favoritos(favoritos):
    os.makedirs("data", exist_ok=True)
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(favoritos, f, ensure_ascii=False, indent=2)

if 'favoritos' not in st.session_state:
    st.session_state.favoritos = cargar_favoritos()

# Menú de navegación
pagina = st.sidebar.radio("Ir a", ["🏠 Inicio", "🔍 Buscar", "🧠 Asistente", "⭐ Favoritos"], label_visibility="collapsed")

# ====================== INICIO ======================
if pagina == "🏠 Inicio":
    st.image("https://source.unsplash.com/800x400/?fitness,gym,workout", use_container_width=True)
    st.markdown("### ¿Qué vas a entrenar hoy?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍗 Post-Entreno", use_container_width=True):
            st.success("Ve al Asistente para recomendaciones personalizadas")
    with col2:
        if st.button("🏋️ Pre-Entreno", use_container_width=True):
            st.success("Ve al Asistente para recomendaciones personalizadas")

# ====================== BUSCAR ======================
elif pagina == "🔍 Buscar":
    st.header("🔍 Buscar Alimentos")
    busqueda = st.text_input("Busca un alimento...", placeholder="pollo, avena, banana, salmón...")
    
    if busqueda:
        resultados = df[df['alimento'].str.contains(busqueda, case=False)]
        if not resultados.empty:
            for _, row in resultados.iterrows():
                with st.expander(f"🍽️ {row['alimento']}"):
                    st.write(f"**Proteínas:** {row['proteinas']}g | **Calorías:** {row['calorias']} kcal")
                    st.write(f"**Beneficio:** {row['beneficio']}")
                    st.success(f"**Recomendación:** {row['recomendacion']}")
                    
                    if row['alimento'] in st.session_state.favoritos:
                        if st.button("❤️ Quitar de favoritos", key=f"del_{row['alimento']}"):
                            st.session_state.favoritos.remove(row['alimento'])
                            guardar_favoritos(st.session_state.favoritos)
                            st.rerun()
                    else:
                        if st.button("⭐ Agregar a favoritos", key=f"add_{row['alimento']}"):
                            st.session_state.favoritos.append(row['alimento'])
                            guardar_favoritos(st.session_state.favoritos)
                            st.success("¡Agregado a favoritos!")
                            st.rerun()
        else:
            st.warning("No se encontró ese alimento.")

# ====================== ASISTENTE ======================
elif pagina == "🧠 Asistente":
    st.header("🧠 Habla con tu Coach")
    st.write("Pregúntame lo que necesites")
    
    pregunta = st.text_input("Escribe tu pregunta...", placeholder="¿Qué como después de entrenar piernas?")
    momento = st.selectbox("Momento del día", ["Después de entrenar", "Antes de entrenar"])
    
    if st.button("Consultar 💪", type="primary"):
        if pregunta:
            with st.spinner("Pensando..."):
                momento_key = "post" if momento.startswith("Después") else "pre"
                respuesta = asistente_basico(pregunta, momento_key)
                st.success(respuesta)
        else:
            st.warning("Escribe tu pregunta")

# ====================== FAVORITOS ======================
elif pagina == "⭐ Favoritos":
    st.header("⭐ Mis Favoritos")
    if st.session_state.favoritos:
        for alimento in st.session_state.favoritos:
            row = df[df['alimento'] == alimento].iloc[0]
            with st.expander(f"❤️ {alimento}"):
                st.write(f"**Proteínas:** {row['proteinas']}g | **Calorías:** {row['calorias']} kcal")
                st.write(f"**Beneficio:** {row['beneficio']}")
                if st.button("Eliminar ❌", key=f"remove_{alimento}"):
                    st.session_state.favoritos.remove(alimento)
                    guardar_favoritos(st.session_state.favoritos)
                    st.rerun()
    else:
        st.info("Todavía no tienes favoritos. Agrega desde la sección Buscar.")

st.caption("NutriFit © 2026 - Prototipo v2.0")
