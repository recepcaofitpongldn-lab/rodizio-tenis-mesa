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
        jogador = st.session_state.fila.pop(0)
        st.session_state.partidas[jogador] = 0
        return jogador
    return "Livre"

def registrar_partida(j):
    st.session_state.partidas[j] = st.session_state.partidas.get(j,0)+1

def registrar_vitoria(j):
    st.session_state.vitorias[j] = st.session_state.vitorias.get(j,0)+1

def preencher_mesas():
    for mesa in st.session_state.mesas:
        for i in range(2):
            if mesa["players"][i] == "Livre":
                mesa["players"][i] = proximo()

# ---------------- REGRA CORRETA ----------------
def resultado(idx, vencedor, perdedor):
    mesa = st.session_state.mesas[idx]

    registrar_vitoria(vencedor)
    registrar_partida(vencedor)
    registrar_partida(perdedor)

    fila = len(st.session_state.fila)

    # 🔥 REGRA OFICIAL
    if fila >= 2:
        # ambos jogam no máximo 2 partidas
        sair_v = st.session_state.partidas[vencedor] >= 2
        sair_p = st.session_state.partidas[perdedor] >= 2

        novos = []

        # vencedor
        if sair_v:
            st.session_state.fila.append(vencedor)
            novos.append(proximo())
        else:
            novos.append(vencedor)

        # perdedor SEMPRE sai (entra novo)
        st.session_state.fila.append(perdedor)
        novos.append(proximo())

        mesa["players"] = novos

    else:
        # sem fila → vencedor continua
        st.session_state.fila.append(perdedor)
        mesa["players"] = [vencedor, proximo()]

    mesa["inicio"] = time.time()
    st.rerun()

# ---------------- TIMER ----------------
def verificar_tempo():
    agora = time.time()

    for mesa in st.session_state.mesas:
        if agora - mesa["inicio"] >= TEMPO:
            for p in mesa["players"]:
                if p != "Livre":
                    st.session_state.fila.append(p)

            mesa["players"] = ["Livre","Livre"]
            mesa["inicio"] = time.time()

# ---------------- MESAS ----------------
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

# ---------------- EXECUÇÃO ----------------
verificar_tempo()
preencher_mesas()

# ---------------- SETS ----------------
sets = "Melhor de 3" if len(st.session_state.fila) >= 2 else "Melhor de 5"
st.markdown(f"<h2 style='text-align:center;'>🎯 {sets}</h2>", unsafe_allow_html=True)

# ---------------- ADICIONAR ----------------
nome = st.text_input("Adicionar jogador")

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

        tempo_restante = max(0, int(TEMPO - (time.time() - mesa["inicio"])))
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

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Mesa extra"):
        add_mesa()

with col2:
    if st.button("➖ Remover mesa"):
        remove_mesa()

# ---------------- RANKING ----------------
st.markdown("---")
st.markdown("## 🏆 Ranking")

for j, v in sorted(st.session_state.vitorias.items(), key=lambda x:-x[1]):
    st.write(f"{j}: {v}")
