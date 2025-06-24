import streamlit as st
from database_manager import add_properties_from_csv, get_properties
from utils import login_form

st.set_page_config(page_title="Operator Dashboard", layout="wide")
st.title("🧑‍💻 Operator Dashboard")

if "user_email" not in st.session_state or st.session_state.get("user_role") != "operator":
    st.sidebar.header("Operator Login")
    login_form("operator")
    st.stop()

if st.sidebar.button("Logout"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()

st.subheader("Upload Properties (CSV)")
uploaded = st.file_uploader("Upload property CSV", type=["csv"])
if uploaded:
    add_properties_from_csv(uploaded, st.session_state["user_email"])
    st.success("Properties uploaded! Awaiting admin approval.")

st.subheader("My Uploaded Properties")
df = get_properties(operator_email=st.session_state["user_email"])
st.dataframe(df)
