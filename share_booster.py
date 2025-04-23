import streamlit as st
import re
import time
import aiohttp
import asyncio
import os
from utils import validate_cookie, validate_post_url, get_token_from_cookie, extract_cookie_from_appstate

def share_post(cookie, post, share_count, delay):
    """Execute the post sharing operation."""
    
    class Share:
        async def get_token(self, session):
            """Extract Facebook access token from cookie."""
            try:
                head = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': "Windows",
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'cookie': cookie
                }
                
                async with session.get('https://business.facebook.com/content_management', headers=head) as response:
                    data = await response.text()
                    access_token = 'EAAG' + re.search('EAAG(.*?)","', data).group(1)
                    return access_token, head['cookie']
            except Exception as er:
                st.error(f"Cookie blocked or invalid: {str(er)}")
                return None, None
        
        async def share(self, session, token, cookie):
            """Share the post multiple times."""
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Windows",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "cookie": cookie,
                "accept-encoding": "gzip, deflate",
                "host": "b-graph.facebook.com"
            }
            
            count = 0
            share_api_url = f'https://graph.facebook.com/v13.0/me/feed?link={post}&published=0&access_token={token}'
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            while count < share_count:
                time.sleep(delay)
                
                try:
                    async with session.post(share_api_url, headers=headers) as response:
                        data = await response.json()
                        
                        if 'id' in data:
                            count += 1
                            progress = int(count / share_count * 100)
                            progress_bar.progress(progress)
                            status_text.markdown(f"<div class='share-progress'>✅ ({count}/{share_count}) Successfully shared</div>", unsafe_allow_html=True)
                        else:
                            status_text.markdown(f"<div class='share-error'>❌ Cookie blocked or invalid. Total successful shares: {count}</div>", unsafe_allow_html=True)
                            return
                except Exception as e:
                    status_text.markdown(f"<div class='share-error'>❌ Error: {str(e)}</div>", unsafe_allow_html=True)
                    time.sleep(1)
            
            status_text.markdown(f"<div class='share-complete'>✅ Share operation completed! Total shares: {count}</div>", unsafe_allow_html=True)
    
    async def main():
        """Main async function to handle sharing."""
        async with aiohttp.ClientSession() as session:
            share = Share()
            token, updated_cookie = await share.get_token(session)
            
            if token and updated_cookie:
                await share.share(session, token, updated_cookie)
            else:
                st.error("Failed to retrieve token. Please check your cookie.")
    
    # Run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

def show_share_booster():
    """Display the share booster interface."""
    st.markdown("""
    <div class="share-booster-header">
        <h2 class="section-title">Facebook Share Booster</h2>
        <p>Boost your post reach by increasing share count</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["Cookie Method", "Appstate Method", "Login Method"])
    
    with tab1:
        st.markdown("""
        <div class="method-description">
            <h3>Cookie Method</h3>
            <p>Use your Facebook cookie to boost post shares</p>
        </div>
        """, unsafe_allow_html=True)
        
        cookie = st.text_area("Facebook Cookie", key="cookie_input", 
                              help="Paste your Facebook cookie here. Must contain c_user.")
        post_url = st.text_input("Post URL", key="post_url_cookie", 
                                help="Facebook post URL to boost shares. Must start with https://www.facebook.com/")
        
        col1, col2 = st.columns(2)
        with col1:
            share_count = st.number_input("Share Count", min_value=1, max_value=1000, value=10, key="share_count_cookie",
                                        help="Number of shares to generate")
        with col2:
            delay = st.number_input("Delay (seconds)", min_value=0, max_value=10, value=1, key="delay_cookie",
                                   help="Delay between shares to avoid rate limiting")
        
        if st.button("Start Boosting", key="start_cookie", use_container_width=True):
            if not validate_cookie(cookie):
                st.error("Invalid cookie format. Cookie must contain c_user.")
            elif not validate_post_url(post_url):
                st.error("Invalid post URL. URL must start with https://www.facebook.com/")
            else:
                with st.spinner("Initializing share booster..."):
                    with st.container(border=True):
                        share_post(cookie, post_url, share_count, delay)
    
    with tab2:
        st.markdown("""
        <div class="method-description">
            <h3>Appstate Method</h3>
            <p>Use Facebook appstate JSON to boost post shares</p>
        </div>
        """, unsafe_allow_html=True)
        
        appstate = st.text_area("Facebook Appstate JSON", key="appstate_input_share",
                               help="Paste your Facebook appstate JSON here.")
        post_url = st.text_input("Post URL", key="post_url_appstate",
                               help="Facebook post URL to boost shares. Must start with https://www.facebook.com/")
        
        col1, col2 = st.columns(2)
        with col1:
            share_count = st.number_input("Share Count", min_value=1, max_value=1000, value=10, key="share_count_appstate",
                                        help="Number of shares to generate")
        with col2:
            delay = st.number_input("Delay (seconds)", min_value=0, max_value=10, value=1, key="delay_appstate",
                                   help="Delay between shares to avoid rate limiting")
        
        if st.button("Start Boosting", key="start_appstate", use_container_width=True):
            if not appstate:
                st.error("Please provide your Facebook appstate JSON.")
            elif not validate_post_url(post_url):
                st.error("Invalid post URL. URL must start with https://www.facebook.com/")
            else:
                with st.spinner("Processing appstate..."):
                    result = extract_cookie_from_appstate(appstate)
                    if result["success"]:
                        with st.container(border=True):
                            share_post(result["cookie"], post_url, share_count, delay)
                    else:
                        st.error(result["message"])
    
    with tab3:
        st.markdown("""
        <div class="method-description">
            <h3>Login Method</h3>
            <p>Use Facebook username and password to boost post shares</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("Use your dummy account for testing purposes only")
            username = st.text_input("Facebook Username/Email", key="login_username_boost")
            password = st.text_input("Facebook Password", type="password", key="login_password_boost")
            post_url = st.text_input("Post URL", key="post_url_login",
                                   help="Facebook post URL to boost shares. Must start with https://www.facebook.com/")
            
            col3, col4 = st.columns(2)
            with col3:
                share_count = st.number_input("Share Count", min_value=1, max_value=1000, value=10, key="share_count_login",
                                           help="Number of shares to generate")
            with col4:
                delay = st.number_input("Delay (seconds)", min_value=0, max_value=10, value=1, key="delay_login",
                                      help="Delay between shares to avoid rate limiting")
            
            if st.button("Start Boosting", key="start_login", use_container_width=True):
                if not username or not password:
                    st.error("Please enter both username and password")
                elif not validate_post_url(post_url):
                    st.error("Invalid post URL. URL must start with https://www.facebook.com/")
                else:
                    with st.spinner("Logging in..."):
                        from utils import convert_to_cookie
                        result = convert_to_cookie(username, password)
                        
                        if result["success"]:
                            with st.container(border=True):
                                share_post(result["cookie"], post_url, share_count, delay)
                        else:
                            st.error(result["message"])
        
        with col2:
            st.markdown("""
            <div class="login-info-card">
                <h3>Login Method Info</h3>
                <p>This method:</p>
                <ul>
                    <li>Securely logs into Facebook</li>
                    <li>Converts credentials to cookie</li>
                    <li>Uses cookie for sharing</li>
                    <li>Doesn't store your password</li>
                </ul>
                <p>Best for users without technical knowledge.</p>
            </div>
            """, unsafe_allow_html=True)
