import streamlit as st
import time

st.set_page_config(layout="wide")

# ---------------- ESTADO ----------------
if "fila" not in st.session_state:
    st.session_state.fila = []

if "mesas" not in st.session_state:
    st.session_state.mesas = [["Livre","Livre"], ["Livre","Livre"]]

if "vitorias" not in st.session_state:
    st.session_state.vitorias = {}

if "tempo_inicio" not in st.session_state:
    st.session_state.tempo_inicio = time.time()

TEMPO_PARTIDA = 15 * 60  # 15 minutos

# ---------------- FUNÇÕES ----------------
def proximo():
    if st.session_state.fila:
        return st.session_state.fila.pop(0)
    return "Livre"

def preencher_mesas():
    for i in range(len(st.session_state.mesas)):
        p1, p2 = st.session_state.mesas[i]

        if p1 == "Livre":
            st.session_state.mesas[i][0] = proximo()

        if p2 == "Livre":
            st.session_state.mesas[i][1] = proximo()

def registrar_vitoria(j):
    st.session_state.vitorias[j] = st.session_state.vitorias.get(j,0)+1

def resultado(idx, vencedor, perdedor):
    registrar_vitoria(vencedor)

    st.session_state.fila.append(perdedor)

    novo = proximo()
    st.session_state.mesas[idx] = [vencedor, novo]

def trocar_todas_mesas():
    for i in range(len(st.session_state.mesas)):
        p1, p2 = st.session_state.mesas[i]

        if p1 != "Livre":
            st.session_state.fila.append(p1)
        if p2 != "Livre":
            st.session_state.fila.append(p2)

        st.session_state.mesas[i] = ["Livre","Livre"]

    preencher_mesas()
    st.session_state.tempo_inicio = time.time()

def add_mesa():
    st.session_state.mesas.append(["Livre","Livre"])

def remove_mesa():
    if len(st.session_state.mesas) > 2:
        st.session_state.mesas.pop()

def reset():
    st.session_state.fila = []
    st.session_state.mesas = [["Livre","Livre"], ["Livre","Livre"]]
    st.session_state.vitorias = {}
    st.session_state.tempo_inicio = time.time()

# ---------------- TIMER ----------------
tempo_passado = time.time() - st.session_state.tempo_inicio
tempo_restante = int(TEMPO_PARTIDA - tempo_passado)

if tempo_restante <= 0:
    trocar_todas_mesas()
    st.rerun()

minutos = tempo_restante // 60
segundos = tempo_restante % 60

st.markdown(f"<h1 style='text-align:center;'>⏱️ {minutos:02d}:{segundos:02d}</h1>", unsafe_allow_html=True)

# ---------------- TÍTULO ----------------
st.markdown("<h1 style='text-align:center;'>🏓 FITPONG - BATE-BOLA</h1>", unsafe_allow_html=True)

# ---------------- ADICIONAR ----------------
st.markdown("### ➕ Adicionar jogador")

col1, col2 = st.columns([3,1])

with col1:
    nome = st.text_input("Nome")

with col2:
    if st.button("Adicionar"):
        if nome:
            st.session_state.fila.append(nome)

# ---------------- AUTO PREENCHER ----------------
preencher_mesas()

# ---------------- MESAS ----------------
st.markdown("---")

cols = st.columns(len(st.session_state.mesas))

for i, mesa in enumerate(st.session_state.mesas):
    with cols[i]:
        p1, p2 = mesa
        st.markdown(f"## 🏓 Mesa {i+1}")
        st.markdown(f"### {p1} 🆚 {p2}")

        if st.button(f"{p1} venceu", key=f"{i}_a"):
            resultado(i, p1, p2)
            st.rerun()

        if st.button(f"{p2} venceu", key=f"{i}_b"):
            resultado(i, p2, p1)
            st.rerun()

# ---------------- FILA ----------------
st.markdown("---")
st.markdown("## ⏳ Fila")

for i, j in enumerate(st.session_state.fila):
    col1, col2 = st.columns([4,1])

    with col1:
        st.write(f"{i+1}. {j}")

    with col2:
        if st.button("❌", key=f"del{i}"):
            st.session_state.fila.pop(i)
            st.rerun()

# ---------------- CONTROLE MESAS ----------------
st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    if st.button("➕ Mesa extra"):
        add_mesa()

with c2:
    if st.button("➖ Remover mesa"):
        remove_mesa()

# ---------------- RANKING ----------------
st.markdown("---")
st.markdown("## 🏆 Ranking")

for j, v in sorted(st.session_state.vitorias.items(), key=lambda x:-x[1]):
    st.write(f"{j}: {v}")

# ---------------- RESET ----------------
st.markdown("---")
if st.button("🔄 Resetar sistema"):
    reset()
