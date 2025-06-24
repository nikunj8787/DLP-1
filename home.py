import streamlit as st
from database_manager import init_db, seed_users

st.set_page_config(page_title="Real Estate Platform", layout="wide")
init_db()
seed_users()

st.title("🏢 Real Estate Management Platform")
st.markdown("""
Welcome!  
- Use the sidebar to select your role and login.
- Admin, Operator, and Customer dashboards are available as separate pages.
- Data is stored in a local SQLite database (resets on redeploy).
""")
