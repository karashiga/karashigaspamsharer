import streamlit as st
import json
import os
import time
import uuid
import hashlib
from utils import load_users, add_user, update_last_login, verify_user

def show_login_page():
    """Display the user login page."""
    st.markdown("""
    <div class="login-container">
        <h2 class="section-title">User Login</h2>
        <p>Enter your credentials to access the FB Share Booster Pro</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and signup
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    
    with login_tab:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.button("Login", key="submit_login", use_container_width=True)
            
            if submit_button:
                if not username or not password:
                    st.error("Username and password cannot be empty")
                else:
                    # Verify user credentials
                    result = verify_user(username, password)
                    
                    if result["success"]:
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
                        st.error(result["message"])
        
        with col2:
            st.markdown("""
            <div class="login-info-card">
                <h3>Login Info</h3>
                <ul>
                    <li>Enter your username and password</li>
                    <li>Access all features after login</li>
                    <li>Need an account? Use the Sign Up tab</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with signup_tab:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_username = st.text_input("Choose Username", key="signup_username")
            new_password = st.text_input("Choose Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            signup_button = st.button("Create Account", key="submit_signup", use_container_width=True)
            
            if signup_button:
                if not new_username or not new_password or not confirm_password:
                    st.error("All fields are required")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # Check if username already exists
                    users_data = load_users()
                    user_exists = False
                    
                    for user in users_data["users"]:
                        if user["username"] == new_username:
                            user_exists = True
                            break
                    
                    if user_exists:
                        st.error(f"Username '{new_username}' is already taken")
                    else:
                        # Hash the password and create new user
                        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                        
                        # Create the user account
                        users_data["users"].append({
                            "username": new_username,
                            "password": password_hash,
                            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "last_login": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Save the updated user data
                        with open("data/users.json", "w") as f:
                            json.dump(users_data, f, indent=4)
                        
                        # Set session state
                        st.session_state.authenticated = True
                        st.session_state.current_user = new_username
                        st.session_state.page = "main"
                        
                        st.success("Account created and logged in successfully!")
                        time.sleep(1)
                        st.rerun()
        
        with col2:
            st.markdown("""
            <div class="login-info-card">
                <h3>Sign Up Info</h3>
                <ul>
                    <li>Choose a unique username</li>
                    <li>Create a strong password</li>
                    <li>Account is created instantly</li>
                    <li>Already have an account? Use the Login tab</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Add a back button
    if st.button("Back to Home", key="back_btn"):
        st.session_state.page = "main"
        st.rerun()
