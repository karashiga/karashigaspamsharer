import streamlit as st
import json
import time
from utils import load_users, save_users, remove_user

def show_admin_login():
    """Display the admin login page."""
    st.markdown("""
    <div class="login-container admin-login">
        <h2 class="section-title">Admin Login</h2>
        <p>Enter administrator credentials to access the control panel</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        username = st.text_input("Admin Username", key="admin_username")
        password = st.text_input("Admin Password", type="password", key="admin_password")
        submit_button = st.button("Login", key="submit_admin_login", use_container_width=True)
        
        if submit_button:
            if username == "david143" and password == "david1433":
                st.session_state.admin_authenticated = True
                st.session_state.page = "admin"
                st.success("Admin login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid admin credentials")
    
    with col2:
        st.markdown("""
        <div class="login-info-card admin-info-card">
            <h3>Admin Panel</h3>
            <ul>
                <li>Access user management</li>
                <li>Monitor system performance</li>
                <li>Configure application settings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a back button
    if st.button("Back to Home", key="admin_back_btn"):
        st.session_state.page = "main"
        st.rerun()

def show_admin_dashboard():
    """Display the admin dashboard."""
    st.markdown("""
    <div class="admin-dashboard-header">
        <h2 class="section-title">Admin Dashboard</h2>
        <p>Manage users and system settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Management
    st.markdown("### User Management")
    
    # Load user data
    user_data = load_users()
    
    if not user_data["users"]:
        st.info("No users registered in the system")
    else:
        # Display user table
        st.markdown("<div class='user-table-container'>", unsafe_allow_html=True)
        
        user_table = "<table class='user-table'><thead><tr><th>Username</th><th>Created At</th><th>Last Login</th><th>Action</th></tr></thead><tbody>"
        
        for user in user_data["users"]:
            username = user.get("username", "N/A")
            created_at = user.get("created_at", "N/A")
            last_login = user.get("last_login", "N/A")
            
            user_table += f"<tr><td>{username}</td><td>{created_at}</td><td>{last_login}</td><td><button class='remove-user-btn' data-username='{username}'>Remove</button></td></tr>"
        
        user_table += "</tbody></table>"
        st.markdown(user_table, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # User removal implementation
        user_to_remove = st.selectbox("Select a user to remove:", 
                                    [user["username"] for user in user_data["users"]])
        
        if st.button("Remove Selected User", key="remove_user_btn"):
            if remove_user(user_to_remove):
                st.success(f"User '{user_to_remove}' successfully removed")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Failed to remove user '{user_to_remove}'")
    
    # System Statistics
    st.markdown("### System Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", len(user_data["users"]))
    with col2:
        st.metric("Active Today", sum(1 for user in user_data["users"] if "last_login" in user and user["last_login"].startswith(time.strftime("%Y-%m-%d"))))
    with col3:
        st.metric("New Users (Today)", sum(1 for user in user_data["users"] if "created_at" in user and user["created_at"].startswith(time.strftime("%Y-%m-%d"))))
