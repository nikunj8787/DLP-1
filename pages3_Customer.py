import streamlit as st
from database_manager import get_properties, add_favorite, get_favorites
from utils import login_form

st.set_page_config(page_title="Customer Dashboard", layout="wide")
st.title("🏠 Customer Dashboard")

if "user_email" not in st.session_state or st.session_state.get("user_role") != "customer":
    st.sidebar.header("Customer Login")
    login_form("customer")
    st.stop()

if st.sidebar.button("Logout"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()

st.subheader("Search Properties")
df = get_properties(status="approved")
search = st.text_input("Search by area or price")
if search:
    df = df[df["address"].str.contains(search, case=False, na=False) | df["price"].str.contains(search, na=False)]

st.dataframe(df)
for idx, row in df.iterrows():
    st.write(f"{row['name']} - {row['address']} - {row['price']}")
    if st.button("Save to Favorites", key=f"fav_{row['id']}"):
        add_favorite(st.session_state["user_email"], row['id'])
        st.success("Added to favorites!")

st.subheader("My Favorites")
favs = get_favorites(st.session_state["user_email"])
st.dataframe(favs)
