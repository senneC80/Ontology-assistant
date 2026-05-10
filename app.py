import streamlit as st

st.set_page_config(page_title="Ontology Assistant", layout="wide")


def check_password() -> bool:
    """Return True if user has entered the correct password."""
    if st.session_state.get("authenticated"):
        return True

    pw = st.text_input("Password", type="password")
    if pw and pw == st.secrets["app_password"]:
        st.session_state["authenticated"] = True
        st.rerun()
    elif pw:
        st.error("Wrong password.")
    return False


if not check_password():
    st.stop()

st.title("Ontology Assistant")
st.write("Authenticated. Hello world.")