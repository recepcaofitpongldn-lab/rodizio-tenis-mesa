import streamlit as st

st.set_page_config(layout="wide")

if "fila" not in st.session_state:
    st.session_state.fila = ["Lucas", "Marina", "Bruno", "Sofia", "Rafael"]

if "mesa1" not in st.session_state:
    st.session_state.mesa1 = ["João", "Carlos"]

if "mesa2" not in st.session_state:
    st.session_state.mesa2 = ["Ana", "Pedro"]

def proximo():
    if len(st.session_state.fila) > 0:
        return st.session_state.fila.pop(0)
    return "Livre"

def perdeu_sai(perdedor):
    st.session_state.fila.append(perdedor)

def resultado(vencedor, perdedor):
    perdeu_sai(perdedor)
    novo = proximo()
    return [vencedor, novo]

st.title("🏓 Rodízio de Tênis de Mesa")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Mesa 1")
    p1, p2 = st.session_state.mesa1
    st.write(f"{p1} vs {p2}")

    if st.button(f"{p1} venceu"):
        st.session_state.mesa1 = resultado(p1, p2)

    if st.button(f"{p2} venceu"):
        st.session_state.mesa1 = resultado(p2, p1)

with col2:
    st.subheader("Mesa 2")
    p1, p2 = st.session_state.mesa2
    st.write(f"{p1} vs {p2}")

    if st.button(f"{p1} venceu "):
        st.session_state.mesa2 = resultado(p1, p2)

    if st.button(f"{p2} venceu "):
        st.session_state.mesa2 = resultado(p2, p1)

st.markdown("---")
st.subheader("Fila")

for i, jogador in enumerate(st.session_state.fila):
    st.write(f"{i+1}. {jogador}")

novo = st.text_input("Novo jogador")
if st.button("Adicionar"):
    if novo:
        st.session_state.fila.append(novo)