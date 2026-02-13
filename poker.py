import streamlit as st
import os
import sys
import subprocess
from PIL import Image

# --- SUA LÓGICA ORIGINAL ---
def open_image_externally(path):
    """Sua função original para abrir no visualizador do sistema"""
    if sys.platform.startswith('darwin'):
        subprocess.call(['open', path])
    elif os.name == 'nt':
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.call(['xdg-open', path])

# Suas listas originais
positions = ["SB", "BB", "EP", "MP", "HJ", "LJ", "CO", "Button"]
stacks = ["0-10", "10-20", "25+"]

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Poker Range Selector", page_icon="🃏")

st.title("🃏 Visualizador de Ranges")
st.markdown("Selecione os parâmetros e veja o range abaixo.")

# Criando colunas para os inputs
col1, col2, col3 = st.columns(3)

with col1:
    pos_choice = st.selectbox("Posição:", positions)

with col3:
    stack_choice = st.selectbox("Stack (Blinds):", stacks)

# Pega o caminho da pasta onde o seu arquivo .py está salvo
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Monta o caminho usando o diretório atual como base
image_path = os.path.join(diretorio_atual, "ranges", stack_choice, f"{pos_choice}.jpg")

st.divider()

# --- BOTÃO ÚNICO E CORRIGIDO ---
if st.button("Visualizar Range", use_container_width=True):
    if os.path.exists(image_path):
        # Caso a imagem exista
        st.subheader(f"Exibindo: {pos_choice}  | {stack_choice} BB")
        img = Image.open(image_path)
        st.image(img, caption=f"Caminho: {image_path}", use_container_width=True)
        
        # Opcional: Descomente a linha abaixo se quiser abrir no Windows também
        # open_image_externally(image_path) 
    else:
        # MENSAGEM AMIGÁVEL SE A IMAGEM NÃO EXISTIR
        st.warning(f"ℹ️ Não há ranges disponíveis para a combinação: **{pos_choice}** em mesa com **{stack_choice} BB**.")
        st.info("Essa jogada pode não estar mapeada ou não ser frequente nesta estratégia.")

# Rodapé com o status do ambiente
st.sidebar.header("Status do Ambiente")
st.sidebar.write(f"**OS:** {sys.platform}")
st.sidebar.write(f"**Python:** {sys.version.split()[0]}")