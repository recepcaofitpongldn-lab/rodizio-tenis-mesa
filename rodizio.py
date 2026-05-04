import streamlit as st

st.set_page_config(layout="wide")

# ---------------- ESTADO ----------------
if "fila" not in st.session_state:
    st.session_state.fila = []

if "mesas" not in st.session_state:
    st.session_state.mesas = [["Livre","Livre"], ["Livre","Livre"]]  # 2 fixas

if "vitorias" not in st.session_state:
    st.session_state.vitorias = {}

if "partidas_jogadas" not in st.session_state:
    st.session_state.partidas_jogadas = {}

# ---------------- FUNÇÕES ----------------
def proximo():
    if st.session_state.fila:
        return st.session_state.fila.pop(0)
    return "Livre"

def registrar_vitoria(jogador):
    if jogador not in st.session_state.vitorias:
        st.session_state.vitorias[jogador] = 0
    st.session_state.vitorias[jogador] += 1

def registrar_partida(jogador):
    if jogador not in st.session_state.partidas_jogadas:
        st.session_state.partidas_jogadas[jogador] = 0
    st.session_state.partidas_jogadas[jogador] += 1

def resultado(idx, vencedor, perdedor):
    fila = len(st.session_state.fila)

    registrar_vitoria(vencedor)
    registrar_partida(vencedor)
    registrar_partida(perdedor)

    # regra: 2+ na fila → 2 jogos e sai
    if fila >= 2:
        if st.session_state.partidas_jogadas.get(vencedor,0) >= 2:
            st.session_state.fila.append(vencedor)
            vencedor = proximo()

        if st.session_state.partidas_jogadas.get(perdedor,0) >= 2:
            st.session_state.fila.append(perdedor)
            perdedor = proximo()
        else:
            st.session_state.fila.append(perdedor)
            perdedor = proximo()
    else:
        st.session_state.fila.append(perdedor)
        perdedor = proximo()

    st.session_state.mesas[idx] = [vencedor, perdedor]

def adicionar_mesa():
    st.session_state.mesas.append(["Livre","Livre"])

def remover_mesa():
    if len(st.session_state.mesas) > 2:
        st.session_state.mesas.pop()

def resetar():
    st.session_state.fila = []
    st.session_state.mesas = [["Livre","Livre"], ["Livre","Livre"]]
    st.session_state.vitorias = {}
    st.session_state.partidas_jogadas = {}

# ---------------- TÍTULO ----------------
st.markdown("<h1 style='text-align:center;'>🏓 SISTEMA DE BATE-BOLA FITPONG</h1>", unsafe_allow_html=True)

# ---------------- CADASTRO ----------------
st.markdown("### ➕ Adicionar jogador")

col1, col2 = st.columns([3,1])

with col1:
    novo = st.text_input("Nome")

with col2:
    if st.button("Adicionar"):
        if novo:
            st.session_state.fila.append(novo)

# ---------------- CONTROLE DE MESAS ----------------
st.markdown("### 🛠️ Mesas")

c1, c2 = st.columns(2)

with c1:
    if st.button("➕ Adicionar mesa"):
        adicionar_mesa()

with c2:
    if st.button("➖ Remover mesa extra"):
        remover_mesa()

# ---------------- DEFINIÇÃO DE SETS ----------------
if len(st.session_state.fila) >= 2:
    sets = "Melhor de 3 sets"
else:
    sets = "Melhor de 5 sets"

st.markdown(f"### 🎯 Sistema atual: {sets}")

# ---------------- MESAS ----------------
st.markdown("---")

cols = st.columns(len(st.session_state.mesas))

for i, mesa in enumerate(st.session_state.mesas):
    with cols[i]:
        p1, p2 = mesa
        st.markdown(f"## 🏓 Mesa {i+1}")
        st.markdown(f"### {p1} 🆚 {p2}")

        if st.button(f"{p1} venceu", key=f"{i}a"):
            resultado(i, p1, p2)

        if st.button(f"{p2} venceu", key=f"{i}b"):
            resultado(i, p2, p1)

# ---------------- FILA ----------------
st.markdown("---")
st.markdown("## ⏳ Fila")

for i, j in enumerate(st.session_state.fila):
    st.write(f"{i+1}. {j}")

# ---------------- RANKING ----------------
st.markdown("---")
st.markdown("## 🏆 Ranking")

for jogador, v in sorted(st.session_state.vitorias.items(), key=lambda x: -x[1]):
    st.write(f"{jogador}: {v} vitórias")

# ---------------- RESET ----------------
st.markdown("---")
if st.button("🔄 Resetar tudo"):
    resetar()
