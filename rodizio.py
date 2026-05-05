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

def resultado(idx, vencedor, perdedor):
    mesa = st.session_state.mesas[idx]

    registrar_vitoria(vencedor)
    registrar_partida(vencedor)
    registrar_partida(perdedor)

    fila = len(st.session_state.fila)

    if fila >= 2:
        sair_v = st.session_state.partidas[vencedor] >= 2

        if sair_v:
            st.session_state.fila.append(vencedor)
            novo_v = proximo()
        else:
            novo_v = vencedor

        st.session_state.fila.append(perdedor)
        novo_p = proximo()

        mesa["players"] = [novo_v, novo_p]

    else:
        st.session_state.fila.append(perdedor)
        mesa["players"] = [vencedor, proximo()]

    mesa["inicio"] = time.time()
    st.rerun()

def verificar_tempo():
    agora = time.time()

    for mesa in st.session_state.mesas:
        if agora - mesa["inicio"] >= TEMPO:
            for p in mesa["players"]:
                if p != "Livre":
                    st.session_state.fila.append(p)

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

# ---------------- TIMER DINÂMICO ----------------
timer_placeholder = st.empty()

# ---------------- MESAS ----------------
mesas_placeholder = st.empty()

def render():
    with mesas_placeholder.container():
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

# ---------------- CONFRONTOS INTELIGENTES ----------------
if len(st.session_state.fila) <= 1 and len(st.session_state.mesas) >= 2:
    st.markdown("---")
    st.markdown("## 🔄 Sugestões de Confronto")

    jogadores = []
    for mesa in st.session_state.mesas:
        jogadores.extend(mesa["players"])

    jogadores = [j for j in jogadores if j != "Livre"]

    for i in range(len(jogadores)):
        for j in range(i+1, len(jogadores)):
            a = jogadores[i]
            b = jogadores[j]

            if st.button(f"{a} vs {b}", key=f"conf{i}{j}"):

                restantes = [x for x in jogadores if x not in [a, b]]
                nova_lista = [a, b] + restantes

                idx = 0
                for mesa in st.session_state.mesas:
                    for k in range(2):
                        if idx < len(nova_lista):
                            mesa["players"][k] = nova_lista[idx]
                            idx += 1
                        else:
                            mesa["players"][k] = "Livre"

                st.rerun()

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

# ---------------- LOOP DO TIMER ----------------
for _ in range(100000):
    render()
    time.sleep(1)
