import streamlit as st
import json
import os
import time
from datetime import datetime

# Import custom modules
import utils
import auth
import admin
import cookie_getter
import share_booster
import style

# Page configuration
st.set_page_config(
    page_title="Boostify Pro",
    page_icon="🧿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
style.apply_custom_styles()

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Create users file if it doesn't exist
if not os.path.exists("data/users.json"):
    with open("data/users.json", "w") as f:
        json.dump({"users": []}, f)

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "main"

# Display logo and header
st.markdown("""
<div class="header-container">
    <div class="logo-container">
        <svg class="logo" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#7B68EE" />
                    <stop offset="100%" stop-color="#4B0082" />
                </linearGradient>
            </defs>
            <path d="M100,20 L180,90 L140,160 L60,160 L20,90 Z" fill="url(#logo-gradient)" />
            <text x="100" y="110" font-family="Arial" font-size="36" font-weight="bold" fill="white" text-anchor="middle">FB</text>
        </svg>
    </div>
    <h1 class="main-title">Boostify Pro v6.5</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar with navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        st.markdown(f"<div class='user-info'>Logged in as: {st.session_state.current_user}</div>", unsafe_allow_html=True)
        if st.button("Main Dashboard", key="nav_main"):
            st.session_state.page = "main"
        if st.button("Cookie Getter", key="nav_cookie"):
            st.session_state.page = "cookie_getter"
        if st.button("Logout", key="nav_logout"):
            st.session_state.authenticated = False
            st.session_state.admin_authenticated = False
            st.session_state.current_user = None
            st.session_state.page = "main"
            st.rerun()
    elif st.session_state.admin_authenticated:
        st.markdown("<div class='admin-info'>Logged in as Admin</div>", unsafe_allow_html=True)
        if st.button("Admin Dashboard", key="nav_admin"):
            st.session_state.page = "admin"
        if st.button("Logout", key="nav_admin_logout"):
            st.session_state.authenticated = False
            st.session_state.admin_authenticated = False
            st.session_state.current_user = None
            st.session_state.page = "main"
            st.rerun()
    else:
        if st.button("Login", key="nav_login"):
            st.session_state.page = "login"
        if st.button("Admin Login", key="nav_admin_login"):
            st.session_state.page = "admin_login"

# Main content area
main_container = st.container()

with main_container:
    # Handle different pages
    if st.session_state.page == "login":
        auth.show_login_page()
    
    elif st.session_state.page == "admin_login":
        admin.show_admin_login()
    
    elif st.session_state.page == "admin" and st.session_state.admin_authenticated:
        admin.show_admin_dashboard()
    
    elif st.session_state.page == "cookie_getter" and st.session_state.authenticated:
        cookie_getter.show_cookie_getter()
    
    elif st.session_state.authenticated:
        # Main dashboard with share booster
        share_booster.show_share_booster()
    
    else:
        # Welcome page with login options
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.markdown("""
            <div class="welcome-container">
                <h2 class="welcome-title">Welcome to FB Share Booster Pro</h2>
                <p class="welcome-text">
                    Boost your Facebook post reach with our professional tool.
                    Login to get started or try our cookie getter tool.
                </p>
                <div class="features-container">
    <div class="feature">
        <h3>🔒 Secure Login</h3>
        <p>Your data stays private and secure with end-to-end encryption and biometric support coming soon.</p>
    </div>
    <div class="feature">
        <h3>🚀 Fast Boosting</h3>
        <p>Instantly enhance your post visibility with AI-optimized delivery for maximum engagement in real time.</p>
    </div>
    <div class="feature">
        <h3>⚙️ Advanced Options</h3>
        <p>Tailor your boosts with smart scheduling, audience targeting, and future analytics dashboards.</p>
    </div>
    <div class="feature">
        <h3>📊 Real-Time Analytics</h3>
        <p>Track your boost performance live with dynamic graphs and future predictive metrics.</p>
    </div>
    <div class="feature">
        <h3>🤖 AI-Powered Recommendations</h3>
        <p>Let our intelligent engine suggest optimal boost times and content strategies—coming soon!</p>
    </div>
    <div class="feature">
        <h3>🌐 Multi-Platform Support</h3>
        <p>Boost across all your favorite platforms seamlessly. Future integrations with emerging networks are underway.</p>
    </div>
</div>
</div>
</div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", key="main_login_btn", use_container_width=True):
                    st.session_state.page = "login"
                    st.rerun()
            with col2:
                if st.button("Admin Login", key="main_admin_btn", use_container_width=True):
                    st.session_state.page = "admin_login"
                    st.rerun()

# Footer
st.markdown("""
<footer class="footer">
    <p>© 2023 FB Share Booster Pro. All rights reserved.</p>
</footer>
""", unsafe_allow_html=True)

# Execute JavaScript for animations and 3D effects
components_js = """
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Add 3D hover effect to buttons
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('mouseover', function() {
                this.style.transform = 'translateY(-3px)';
                this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.3)';
            });
            button.addEventListener('mouseout', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.2)';
            });
        });
    });
</script>
"""

st.components.v1.html(components_js)
