import streamlit as st

st.set_page_config(layout="wide")

# ---------------- ESTADO ----------------
if "fila" not in st.session_state:
    st.session_state.fila = []

if "mesas" not in st.session_state:
    st.session_state.mesas = [["Livre","Livre"], ["Livre","Livre"]]

if "vitorias" not in st.session_state:
    st.session_state.vitorias = {}

if "partidas" not in st.session_state:
    st.session_state.partidas = {}

# ---------------- FUNÇÕES ----------------
def proximo():
    if st.session_state.fila:
        return st.session_state.fila.pop(0)
    return "Livre"

def registrar_vitoria(j):
    st.session_state.vitorias[j] = st.session_state.vitorias.get(j,0)+1

def registrar_partida(j):
    st.session_state.partidas[j] = st.session_state.partidas.get(j,0)+1

def resultado(i, vencedor, perdedor):
    fila = len(st.session_state.fila)

    registrar_vitoria(vencedor)
    registrar_partida(vencedor)
    registrar_partida(perdedor)

    if fila >= 2:
        st.session_state.fila.append(vencedor)
        st.session_state.fila.append(perdedor)
        vencedor = proximo()
        perdedor = proximo()
    else:
        st.session_state.fila.append(perdedor)
        perdedor = proximo()

    st.session_state.mesas[i] = [vencedor, perdedor]

def add_mesa():
    st.session_state.mesas.append(["Livre","Livre"])

def remove_mesa():
    if len(st.session_state.mesas) > 2:
        st.session_state.mesas.pop()

def reset():
    st.session_state.fila = []
    st.session_state.mesas = [["Livre","Livre"], ["Livre","Livre"]]
    st.session_state.vitorias = {}
    st.session_state.partidas = {}

# ---------------- TÍTULO ----------------
st.markdown("<h1 style='text-align:center;'>🏓 SISTEMA BATE-BOLA FITPONG</h1>", unsafe_allow_html=True)

# ---------------- ADICIONAR ----------------
st.markdown("### ➕ Adicionar jogador")
col1, col2 = st.columns([3,1])

with col1:
    nome = st.text_input("Nome do jogador")

with col2:
    if st.button("Adicionar"):
        if nome:
            st.session_state.fila.append(nome)

# ---------------- INSERIR MANUAL ----------------
st.markdown("### 🎯 Inserir jogador na mesa")

colA, colB, colC = st.columns(3)

with colA:
    jogador = st.selectbox("Escolher jogador", st.session_state.fila if st.session_state.fila else [""])

with colB:
    mesa_idx = st.selectbox("Mesa", list(range(1,len(st.session_state.mesas)+1)))

with colC:
    if st.button("Inserir na mesa"):
        if jogador in st.session_state.fila:
            st.session_state.fila.remove(jogador)

            m = st.session_state.mesas[mesa_idx-1]
            if m[0] == "Livre":
                m[0] = jogador
            elif m[1] == "Livre":
                m[1] = jogador

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
    if st.button("➕ Nova mesa"):
        add_mesa()

with c2:
    if st.button("➖ Remover mesa"):
        remove_mesa()

# ---------------- RANKING ----------------
st.markdown("---")
st.markdown("## 🏆 Ranking")

for j, v in sorted(st.session_state.vitorias.items(), key=lambda x:-x[1]):
    st.write(f"{j}: {v} vitórias")

# ---------------- RESET ----------------
st.markdown("---")
if st.button("🔄 Resetar sistema"):
    reset()
