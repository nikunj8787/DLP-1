import streamlit as st
from database_manager import add_properties_from_csv, get_properties

st.set_page_config(page_title="Operator Dashboard", layout="wide")
st.title("🧑‍💻 Operator Dashboard")

if "user_email" not in st.session_state or st.session_state.get("user_role") != "operator":
    st.error("Please login as operator via the sidebar.")
    st.stop()

st.subheader("Upload Properties (CSV)")
uploaded = st.file_uploader("Upload property CSV", type=["csv"])
if uploaded:
    add_properties_from_csv(uploaded, st.session_state["user_email"])
    st.success("Properties uploaded! Awaiting admin approval.")

st.subheader("My Uploaded Properties")
df = get_properties(operator_email=st.session_state["user_email"])
st.dataframe(df)
