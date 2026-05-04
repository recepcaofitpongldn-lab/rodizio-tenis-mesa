import streamlit as st

st.set_page_config(layout="wide")

# ---------------- ESTADO ----------------
if "fila" not in st.session_state:
    st.session_state.fila = []

if "mesa1" not in st.session_state:
    st.session_state.mesa1 = ["Livre", "Livre"]

if "mesa2" not in st.session_state:
    st.session_state.mesa2 = ["Livre", "Livre"]

# ---------------- FUNÇÕES ----------------
def proximo():
    if st.session_state.fila:
        return st.session_state.fila.pop(0)
    return "Livre"

def resultado(mesa, vencedor, perdedor):
    st.session_state.fila.append(perdedor)
    novo = proximo()

    if mesa == 1:
        st.session_state.mesa1 = [vencedor, novo]
    else:
        st.session_state.mesa2 = [vencedor, novo]

def resetar():
    st.session_state.fila = []
    st.session_state.mesa1 = ["Livre", "Livre"]
    st.session_state.mesa2 = ["Livre", "Livre"]

# ---------------- TÍTULO ----------------
st.markdown("<h1 style='text-align:center;'>🏓 RODÍZIO - TÊNIS DE MESA</h1>", unsafe_allow_html=True)

# ---------------- CADASTRO ----------------
st.markdown("### ➕ Adicionar jogador")

col_add1, col_add2 = st.columns([3,1])

with col_add1:
    novo = st.text_input("Nome do jogador")

with col_add2:
    if st.button("Adicionar"):
        if novo:
            st.session_state.fila.append(novo)

# ---------------- MESAS ----------------
st.markdown("---")

col1, col2 = st.columns(2)

# MESA 1
with col1:
    st.markdown("## 🟦 Mesa 1")
    p1, p2 = st.session_state.mesa1

    st.markdown(f"### {p1}  🆚  {p2}")

    if st.button(f"{p1} venceu", key="m1p1"):
        resultado(1, p1, p2)

    if st.button(f"{p2} venceu", key="m1p2"):
        resultado(1, p2, p1)

# MESA 2
with col2:
    st.markdown("## 🟩 Mesa 2")
    p1, p2 = st.session_state.mesa2

    st.markdown(f"### {p1}  🆚  {p2}")

    if st.button(f"{p1} venceu", key="m2p1"):
        resultado(2, p1, p2)

    if st.button(f"{p2} venceu", key="m2p2"):
        resultado(2, p2, p1)

# ---------------- FILA ----------------
st.markdown("---")
st.markdown("## ⏳ Fila de Espera")

for i, jogador in enumerate(st.session_state.fila):
    st.markdown(f"*{i+1}. {jogador}*")

# ---------------- CONTROLES ----------------
st.markdown("---")

col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    if st.button("▶️ Colocar jogadores nas mesas"):
        if len(st.session_state.fila) >= 4:
            st.session_state.mesa1 = [proximo(), proximo()]
            st.session_state.mesa2 = [proximo(), proximo()]

with col_ctrl2:
    if st.button("🔄 Resetar sistema"):
        resetar()
