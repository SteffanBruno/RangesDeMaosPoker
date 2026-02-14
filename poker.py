import streamlit as st
import os
from PIL import Image

# --- configuracao base do buscador---
st.set_page_config(page_title="Poker Range Selector", page_icon="🃏", layout="wide")

positions = ["SB", "BB", "EP", "MP", "HJ", "LJ", "CO", "Button"]
stacks = ["0-10", "10-20", "25+"]
viloes = ["HJ", "CO", "EP", "MP", "BTN"]

st.title("🃏 Visualizador de Ranges")

# --- interface para visualizacao ---
col1, col2 = st.columns(2)
with col1:
    pos_choice = st.selectbox("Sua Posição:", positions)
with col2:
    stack_choice = st.selectbox("Stack (Blinds):", stacks)

vs_choice = None
if pos_choice in ["SB", "BB"]:
    st.markdown("---")
    opcoes_viloes = [v for v in viloes if v != pos_choice]
    vs_choice = st.selectbox("Versus (Oponente):", ["Nenhum"] + opcoes_viloes)

# --- logica para busca dos arquivos de imagem ---
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
image_path = None
nome_arquivo_encontrado = ""

if pos_choice in ["SB", "BB"] and vs_choice and vs_choice != "Nenhum":
    pasta_alvo = os.path.join(diretorio_atual, "ranges", "vs")
    termo_busca = f"{pos_choice}x{vs_choice}".lower().replace(" ", "")
    
    if os.path.exists(pasta_alvo):
        for f in os.listdir(pasta_alvo):
            f_limpo = f.lower().replace(" ", "").replace(".jpg", "").replace(".png", "")
            if f_limpo == termo_busca:
                image_path = os.path.join(pasta_alvo, f)
                nome_arquivo_encontrado = f
                break
else:
    nome_padrao = f"{pos_choice}.jpg"
    temp_path = os.path.join(diretorio_atual, "ranges", stack_choice, nome_padrao)
    if os.path.exists(temp_path):
        image_path = temp_path
        nome_arquivo_encontrado = nome_padrao

st.divider()

# --- exibicao da mensagem de erro caso nao haja uma imagem para exibir ---
if st.button("Visualizar Range", use_container_width=True):
    if image_path:
        st.subheader(f"📊 Exibindo: {nome_arquivo_encontrado.replace('.jpg', '')}")
        img = Image.open(image_path)
        
        col_esq, col_meio, col_dir = st.columns([1, 2, 1])
        
        with col_meio:
            st.image(img, width=600, use_container_width=False)
            
    else:
        msg = f"Não há ranges para a solicitação: **{pos_choice}** com **{stack_choice} BB**."
        
        st.warning(f"ℹ️ {msg}")

st.sidebar.header("🔍 Info Técnica")
st.sidebar.write(f"**Posição:** {pos_choice}")
if vs_choice: st.sidebar.write(f"**Versus:** {vs_choice}")
st.sidebar.write(f"**Status:** {'✅ Localizado' if image_path else '❌ Não encontrado'}")