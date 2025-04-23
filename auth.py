import streamlit as st
import json
import os
import time
import uuid
from utils import load_users, add_user, update_last_login

def show_login_page():
    """Display the user login page."""
    st.markdown("""
    <div class="login-container">
        <h2 class="section-title">User Login</h2>
        <p>Enter your username to access the FB Share Booster Pro</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        username = st.text_input("Username", key="login_username")
        submit_button = st.button("Login", key="submit_login", use_container_width=True)
        
        if submit_button:
            if not username:
                st.error("Username cannot be empty")
            else:
                # Check if user exists
                users_data = load_users()
                user_exists = False
                
                for user in users_data["users"]:
                    if user["username"] == username:
                        user_exists = True
                        break
                
                if user_exists:
                    # Update last login time
                    update_last_login(username)
                    
                    # Set session state
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.session_state.page = "main"
                    
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    # Auto-register new users
                    add_user(username)
                    
                    # Set session state
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.session_state.page = "main"
                    
                    st.success("Account created and logged in successfully!")
                    time.sleep(1)
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="login-info-card">
            <h3>Quick Info</h3>
            <ul>
                <li>Enter any username to login</li>
                <li>New users are automatically registered</li>
                <li>Access share booster features after login</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a back button
    if st.button("Back to Home", key="back_btn"):
        st.session_state.page = "main"
        st.rerun()
