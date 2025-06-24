import streamlit as st
from database_manager import get_properties, update_property_status, get_all_users, verify_user
from utils import login_form

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Dashboard")

if "user_email" not in st.session_state or st.session_state.get("user_role") != "admin":
    st.sidebar.header("Admin Login")
    login_form("admin")
    st.stop()

if st.sidebar.button("Logout"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()

st.subheader("Pending Property Approvals")
df = get_properties(status="pending")
if not df.empty:
    for idx, row in df.iterrows():
        st.write(f"{row['name']} - {row['address']} - {row['price']}")
        col1, col2 = st.columns(2)
        if col1.button("Approve", key=f"approve_{row['id']}"):
            update_property_status(row['id'], "approved")
            st.success("Approved!")
            st.experimental_rerun()
        if col2.button("Reject", key=f"reject_{row['id']}"):
            update_property_status(row['id'], "rejected")
            st.warning("Rejected!")
            st.experimental_rerun()
else:
    st.info("No pending properties.")

st.subheader("Operator Uploads")
ops = get_all_users(role="operator")
for _, op in ops.iterrows():
    st.write(f"Operator: {op['email']}")
    op_df = get_properties(operator_email=op['email'])
    st.dataframe(op_df)

st.subheader("Customer Verification")
custs = get_all_users(role="customer", verified=0)
for _, cust in custs.iterrows():
    st.write(f"{cust['email']}")
    if st.button(f"Verify {cust['email']}", key=f"verify_{cust['email']}"):
        verify_user(cust['email'])
        st.success("Customer verified!")
        st.experimental_rerun()
