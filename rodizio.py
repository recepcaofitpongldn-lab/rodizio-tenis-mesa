import streamlit as st
import time

st.set_page_config(layout="wide")

# ---------------- ESTADO ----------------
if "fila" not in st.session_state:
    st.session_state.fila = []

if "mesas" not in st.session_state:
    st.session_state.mesas = [
        {"players": ["Livre","Livre"], "inicio": time.time()},
        {"players": ["Livre","Livre"], "inicio": time.time()}
    ]

if "vitorias" not in st.session_state:
    st.session_state.vitorias = {}

if "partidas" not in st.session_state:
    st.session_state.partidas = {}

TEMPO = 15 * 60

# ---------------- FUNÇÕES ----------------
def proximo():
    if st.session_state.fila:
        return st.session_state.fila.pop(0)
    return "Livre"

def preencher_mesas():
    for mesa in st.session_state.mesas:
        p1, p2 = mesa["players"]

        if p1 == "Livre":
            mesa["players"][0] = proximo()

        if p2 == "Livre":
            mesa["players"][1] = proximo()

def registrar_partida(j):
    st.session_state.partidas[j] = st.session_state.partidas.get(j,0)+1

def registrar_vitoria(j):
    st.session_state.vitorias[j] = st.session_state.vitorias.get(j,0)+1

def resultado(idx, vencedor, perdedor):
    mesa = st.session_state.mesas[idx]

    registrar_vitoria(vencedor)
    registrar_partida(vencedor)
    registrar_partida(perdedor)

    fila = len(st.session_state.fila)

    if fila >= 2:
        # vencedor pode jogar até 2
        if st.session_state.partidas.get(vencedor,0) >= 2:
            st.session_state.fila.append(vencedor)
            vencedor = proximo()

        # perdedor sempre sai
        st.session_state.fila.append(perdedor)
        perdedor = proximo()

    else:
        # pouca fila → vencedor continua
        st.session_state.fila.append(perdedor)
        perdedor = proximo()

    mesa["players"] = [vencedor, perdedor]
    mesa["inicio"] = time.time()

    st.rerun()

def verificar_tempo():
    agora = time.time()

    for mesa in st.session_state.mesas:
        if agora - mesa["inicio"] >= TEMPO:
            p1, p2 = mesa["players"]

            if p1 != "Livre":
                st.session_state.fila.append(p1)
            if p2 != "Livre":
                st.session_state.fila.append(p2)

            mesa["players"] = ["Livre","Livre"]
            mesa["inicio"] = time.time()

def add_mesa():
    st.session_state.mesas.append({
        "players":["Livre","Livre"],
        "inicio": time.time()
    })
    st.rerun()

def remove_mesa():
    if len(st.session_state.mesas) > 2:
        mesa = st.session_state.mesas.pop()

        for p in mesa["players"]:
            if p != "Livre":
                st.session_state.fila.append(p)

    st.rerun()

def reset():
    st.session_state.fila = []
    st.session_state.mesas = [
        {"players": ["Livre","Livre"], "inicio": time.time()},
        {"players": ["Livre","Livre"], "inicio": time.time()}
    ]
    st.session_state.vitorias = {}
    st.session_state.partidas = {}
    st.rerun()

# ---------------- EXECUÇÃO ----------------
verificar_tempo()
preencher_mesas()

# ---------------- SETS ----------------
if len(st.session_state.fila) >= 2:
    sets = "Melhor de 3 sets"
else:
    sets = "Melhor de 5 sets"

st.markdown(f"<h2 style='text-align:center;'>🎯 {sets}</h2>", unsafe_allow_html=True)

# ---------------- ADICIONAR ----------------
col1, col2 = st.columns([3,1])

with col1:
    nome = st.text_input("Adicionar jogador")

with col2:
    if st.button("Adicionar"):
        if nome:
            st.session_state.fila.append(nome)
            st.rerun()

# ---------------- MESAS ----------------
st.markdown("---")

cols = st.columns(len(st.session_state.mesas))

for i, mesa in enumerate(st.session_state.mesas):
    with cols[i]:
        p1, p2 = mesa["players"]

        tempo_restante = int(TEMPO - (time.time() - mesa["inicio"]))
        min = tempo_restante // 60
        sec = tempo_restante % 60

        st.markdown(f"## 🏓 Mesa {i+1}")
        st.markdown(f"⏱️ {min:02d}:{sec:02d}")
        st.markdown(f"### {p1} 🆚 {p2}")

        if st.button(f"{p1} venceu", key=f"{i}a"):
            resultado(i, p1, p2)

        if st.button(f"{p2} venceu", key=f"{i}b"):
            resultado(i, p2, p1)

# ---------------- FILA ----------------
st.markdown("---")
st.markdown("## ⏳ Fila")

for i, j in enumerate(st.session_state.fila):
    col1, col2, col3 = st.columns([4,1,1])

    with col1:
        st.write(f"{i+1}. {j}")

    with col2:
        if st.button("❌", key=f"del{i}"):
            st.session_state.fila.pop(i)
            st.rerun()

    with col3:
        if st.button("⬇️", key=f"down{i}"):
            jogador = st.session_state.fila.pop(i)
            st.session_state.fila.append(jogador)
            st.rerun()

# ---------------- CONTROLE ----------------
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
