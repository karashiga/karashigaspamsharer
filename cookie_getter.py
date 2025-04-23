import streamlit as st
import re
import time
import uuid
import string
import random
import requests
import httpx
import json
from utils import convert_to_cookie, get_cuser_cookie, extract_cookie_from_appstate

def show_cookie_getter():
    """Display the cookie getter interface."""
    st.markdown("""
    <div class="cookie-getter-header">
        <h2 class="section-title">Facebook Cookie Getter</h2>
        <p>Get Facebook cookies for your accounts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different methods
    tab1, tab2, tab3 = st.tabs(["Standard Login", "Advanced (c_user w/ token)", "Appstate Method"])
    
    with tab1:
        st.markdown("""
        <div class="method-description">
            <h3>Standard Method</h3>
            <p>Get datr, fr, xs cookies using standard Facebook login</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("Use your dummy account for testing purposes only")
            username = st.text_input("Facebook Username/Email", key="standard_username")
            password = st.text_input("Facebook Password", type="password", key="standard_password")
            
            if st.button("Get Cookie", key="get_standard_cookie", use_container_width=True):
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    with st.spinner("Getting cookie..."):
                        result = convert_to_cookie(username, password)
                        
                        if result["success"]:
                            st.success("Cookie retrieved successfully!")
                            st.code(result["cookie"], language="plaintext")
                            st.markdown("""
                            <div class="cookie-info">
                                <p>✅ Copy this cookie for later use</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(result["message"])
        
        with col2:
            st.markdown("""
            <div class="cookie-info-card">
                <h3>Cookie Info</h3>
                <p>This method retrieves the standard Facebook cookie including:</p>
                <ul>
                    <li>datr</li>
                    <li>fr</li>
                    <li>xs</li>
                    <li>c_user</li>
                </ul>
                <p>Use this cookie for basic Facebook operations.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="method-description">
            <h3>Advanced Method</h3>
            <p>Get c_user cookie with access token for better performance</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("Use your dummy account for testing purposes only")
            username = st.text_input("Facebook Username/Email", key="advanced_username")
            password = st.text_input("Facebook Password", type="password", key="advanced_password")
            
            if st.button("Get Advanced Cookie", key="get_advanced_cookie", use_container_width=True):
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    with st.spinner("Getting advanced cookie and token..."):
                        result = get_cuser_cookie(username, password)
                        
                        if result["success"]:
                            st.success("Cookie and token retrieved successfully!")
                            
                            st.markdown("#### Cookie:")
                            st.code(result["cookie"], language="plaintext")
                            
                            st.markdown("#### Access Token:")
                            st.code(result["access_token"], language="plaintext")
                            
                            st.markdown("""
                            <div class="cookie-info">
                                <p>✅ Copy this data for later use</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(result["message"])
        
        with col2:
            st.markdown("""
            <div class="cookie-info-card advanced">
                <h3>Advanced Cookie Info</h3>
                <p>This method retrieves:</p>
                <ul>
                    <li>c_user cookie</li>
                    <li>Facebook access token</li>
                    <li>Other session cookies</li>
                </ul>
                <p>Better for advanced operations and longer session validity.</p>
            </div>
            """, unsafe_allow_html=True)
            
    with tab3:
        st.markdown("""
        <div class="method-description">
            <h3>Appstate Method</h3>
            <p>Convert Facebook appstate JSON to cookie</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            appstate = st.text_area("Facebook Appstate JSON", key="appstate_input",
                              help="Paste your Facebook appstate JSON here.")
            
            if st.button("Extract Cookie", key="extract_cookie_btn", use_container_width=True):
                if not appstate:
                    st.error("Please provide your Facebook appstate JSON.")
                else:
                    with st.spinner("Processing appstate..."):
                        try:
                            result = extract_cookie_from_appstate(appstate)
                            if result["success"]:
                                st.success("Cookie extracted successfully!")
                                st.code(result["cookie"], language="plaintext")
                                st.markdown("""
                                <div class="cookie-info">
                                    <p>✅ Copy this cookie for later use</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.error(result["message"])
                        except Exception as e:
                            st.error(f"Error processing appstate: {str(e)}")
        
        with col2:
            st.markdown("""
            <div class="cookie-info-card">
                <h3>Appstate Info</h3>
                <p>This method:</p>
                <ul>
                    <li>Converts appstate JSON to cookie</li>
                    <li>Extracts all cookie components</li>
                    <li>Works with exported appstate files</li>
                </ul>
                <p>Useful if you already have an appstate from another tool.</p>
            </div>
            """, unsafe_allow_html=True)
