import streamlit as st
import os
import sys
import subprocess
from PIL import Image

# --- FUNÇÃO PARA ABRIR EXTERNAMENTE (OPCIONAL) ---
def open_image_externally(path):
    if sys.platform.startswith('darwin'):
        subprocess.call(['open', path])
    elif os.name == 'nt':
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.call(['xdg-open', path])

# --- CONFIGURAÇÕES E LISTAS ---
st.set_page_config(page_title="Poker Range Selector", page_icon="🃏", layout="wide")

positions = ["SB", "BB", "EP", "MP", "HJ", "LJ", "CO", "Button"]
stacks = ["0-10", "10-20", "25+"]
viloes = ["SB", "BB", "HJ", "LJ", "CO", "EP", "MP", "Button"]

st.title("🃏 Visualizador de Ranges")

# --- INTERFACE DE USUÁRIO ---
col1, col2 = st.columns(2)

with col1:
    pos_choice = st.selectbox("Sua Posição:", positions)

with col2:
    stack_choice = st.selectbox("Stack (Blinds):", stacks)

# Lógica de Versus (Aparece apenas para SB e BB)
vs_choice = None
if pos_choice in ["SB", "BB"]:
    st.markdown("---")
    opcoes_viloes = [v for v in viloes if v != pos_choice]
    vs_choice = st.selectbox("Versus (Oponente):", ["Nenhum"] + opcoes_viloes)

# --- LÓGICA DE DIRETÓRIOS ---
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Se houver um Versus selecionado, muda a busca para a pasta "vs"
if pos_choice in ["SB", "BB"] and vs_choice and vs_choice != "Nenhum":
    nome_arquivo = f"{pos_choice} x {vs_choice}.jpg"
    image_path = os.path.join(diretorio_atual, "ranges", "vs", nome_arquivo)
else:
    # Caso contrário, busca nas pastas de stack (0-10, 10-20, etc)
    nome_arquivo = f"{pos_choice}.jpg"
    image_path = os.path.join(diretorio_atual, "ranges", stack_choice, nome_arquivo)

st.divider()

# --- BOTÃO DE EXIBIÇÃO ---
if st.button("Visualizar Range", use_container_width=True):
    if os.path.exists(image_path):
        exibicao = nome_arquivo.replace('.jpg', '')
        st.subheader(f"📊 {exibicao} | {stack_choice if 'vs' not in image_path else 'Confronto'} ")
        
        img = Image.open(image_path)
        st.image(img, use_container_width=True)
        
        # Opcional: Descomente para abrir no visualizador do Windows também
        # open_image_externally(image_path) 
    else:
        st.error(f"❌ Arquivo não encontrado!")
        st.info(f"O sistema buscou em: {image_path}")
        st.markdown(f"**Dica:** Verifique se o arquivo `{nome_arquivo}` está dentro da pasta correta.")

# --- SIDEBAR DE STATUS (DEBUG) ---
st.sidebar.header("Status do Ambiente")
st.sidebar.write(f"**Posição:** {pos_choice}")
st.sidebar.write(f"**Stack:** {stack_choice}")
if vs_choice:
    st.sidebar.write(f"**Versus:** {vs_choice}")
st.sidebar.write(f"**Arquivo Alvo:** {nome_arquivo}")