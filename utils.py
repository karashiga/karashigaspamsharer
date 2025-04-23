import streamlit as st
import re
import json
import os
import time
import uuid
import string
import random
import hashlib
import httpx
import requests
import asyncio
import aiohttp

def validate_cookie(cookie):
    """Validate if a Facebook cookie is properly formatted."""
    if not cookie:
        return False
    
    # Check for essential cookie components
    if 'c_user' not in cookie:
        return False
    
    return True

def validate_post_url(url):
    """Validate if the provided URL is a valid Facebook post URL."""
    if not url:
        return False
    
    # Basic validation for Facebook post URL
    if not url.startswith('https://www.facebook.com/'):
        return False
    
    return True

async def get_token_from_cookie(cookie, session):
    """Extract Facebook access token from a cookie."""
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
            return access_token
    except Exception as e:
        st.error(f"Error getting token: {str(e)}")
        return None

def load_users():
    """Load user data from JSON file."""
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": []}

def save_users(data):
    """Save user data to JSON file."""
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)

def verify_user(username, password):
    """Verify user credentials."""
    data = load_users()
    
    for user in data["users"]:
        if user["username"] == username:
            # Check if the user was created with the old system (no password)
            if "password" not in user:
                # Update to new password system
                user["password"] = hashlib.sha256(password.encode()).hexdigest()
                save_users(data)
                return {"success": True}
            
            # Verify password hash
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if user["password"] == password_hash:
                return {"success": True}
            else:
                return {"success": False, "message": "Invalid password"}
    
    return {"success": False, "message": "User not found"}

def add_user(username, password=None):
    """Add a new user to the system."""
    data = load_users()
    
    # Check if user already exists
    for user in data["users"]:
        if user["username"] == username:
            return False
    
    # Add new user
    new_user = {
        "username": username,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add password if provided
    if password:
        new_user["password"] = hashlib.sha256(password.encode()).hexdigest()
    
    data["users"].append(new_user)
    save_users(data)
    return True

def remove_user(username):
    """Remove a user from the system."""
    data = load_users()
    
    # Find and remove user
    for i, user in enumerate(data["users"]):
        if user["username"] == username:
            data["users"].pop(i)
            save_users(data)
            return True
    
    return False

def update_last_login(username):
    """Update the last login time for a user."""
    data = load_users()
    
    for user in data["users"]:
        if user["username"] == username:
            user["last_login"] = time.strftime("%Y-%m-%d %H:%M:%S")
            save_users(data)
            return True
    
    return False

def convert_to_cookie(username, password):
    """Convert Facebook username/password to a cookie."""
    try:
        session = requests.Session()
        headers = {
            'authority': 'free.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'dpr': '3',
            'origin': 'https://free.facebook.com',
            'referer': f'https://free.facebook.com/login/?email={username}',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.1"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            'viewport-width': '980',
        }
        
        getlog = session.get('https://free.facebook.com/login.php')
        idpass = {
            "lsd": re.search('name="lsd" value="(.*?)"', str(getlog.text)).group(1),
            "jazoest": re.search('name="jazoest" value="(.*?)"', str(getlog.text)).group(1),
            "m_ts": re.search('name="m_ts" value="(.*?)"', str(getlog.text)).group(1),
            "li": re.search('name="li" value="(.*?)"', str(getlog.text)).group(1),
            "try_number": "0",
            "unrecognized_tries": "0",
            "email": username,
            "pass": password,
            "login": "Log In",
            "bi_xrwh": re.search('name="bi_xrwh" value="(.*?)"', str(getlog.text)).group(1),
        }
        
        comp = session.post(
            "https://free.facebook.com/login/device-based/regular/login/?shbl=1&refsrc=deprecated",
            headers=headers,
            data=idpass,
            allow_redirects=False
        )
        
        jopl = session.cookies.get_dict().keys()
        cookie = ";".join([key+"="+value for key, value in session.cookies.get_dict().items()])
        
        if "c_user" in jopl:
            return {"success": True, "cookie": cookie}
        elif "checkpoint" in jopl:
            return {"success": False, "message": "Account checkpoint"}
        else:
            return {"success": False, "message": "Invalid username or password"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def get_cuser_cookie(username, password):
    """Get c_user cookie with token for Facebook."""
    try:
        access_token = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
        data = {
            'adid': f'{uuid.uuid4()}',
            'format': 'json',
            'device_id': f'{uuid.uuid4()}',
            'cpl': 'true',
            'family_device_id': f'{uuid.uuid4()}',
            'credentials_type': 'device_based_login_password',
            'error_detail_type': 'button_with_disabled',
            'source': 'device_based_login',
            'email': username,
            'password': password,
            'access_token': access_token,
            'generate_session_cookies': '1',
            'meta_inf_fbmeta': '',
            'advertiser_id': f'{uuid.uuid4()}',
            'currently_logged_in_userid': '0',
            'locale': 'en_US',
            'client_country_code': 'US',
            'method': 'auth.login',
            'fb_api_req_friendly_name': 'authenticate',
            'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
            'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
        }
        
        headers = {
            'User-Agent': "[FBAN/FB4A;FBAV/196.0.0.29.99;FBPN/com.facebook.katana;FBLC/en_US;FBBV/135374479;FBCR/SMART;FBMF/samsung;FBBD/samsung;FBDV/SM-A720F;FBSV/8.0.0;FBCA/armeabi-v7a:armeabi;FBDM/{density=3.0,width=1080,height=1920};FB_FW/1;]",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'graph.facebook.com',
            'X-FB-Net-HNI': str(random.randint(10000, 99999)),
            'X-FB-SIM-HNI': str(random.randint(10000, 99999)),
            'X-FB-Connection-Type': 'MOBILE.LTE',
            'X-Tigon-Is-Retry': 'False',
            'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;nc=1;fc=0;bc=0;cid=62f8ce9f74b12f84c123cc23437a4a32',
            'x-fb-device-group': str(random.randint(1000, 9999)),
            'X-FB-Friendly-Name': 'ViewerReactionsMutation',
            'X-FB-Request-Analytics-Tags': 'graphservice',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Connection-Bandwidth': str(random.randint(20000000, 30000000)),
            'X-FB-Server-Cluster': 'True',
            'x-fb-connection-token': f'62f8ce9f74b12f84c123cc23437a4a32'
        }
        
        response = httpx.post(
            "https://b-graph.facebook.com/auth/login",
            headers=headers,
            data=data,
            follow_redirects=False
        ).json()
        
        if "session_key" in response:
            sb_value = ''.join(random.choices(string.ascii_letters + string.digits + '_', k=24))
            cookie = f"sb={sb_value};" + ';'.join(i['name'] + '=' + i['value'] for i in response['session_cookies'])
            return {
                "success": True, 
                "cookie": cookie, 
                "access_token": response['access_token']
            }
        else:
            return {"success": False, "message": "Invalid credentials or account checkpoint"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def extract_cookie_from_appstate(appstate_json):
    """Extract cookie from Facebook appstate JSON."""
    try:
        appstate = json.loads(appstate_json)
        cookie_parts = []
        
        for item in appstate:
            cookie_parts.append(f"{item['key']}={item['value']};")
        
        cookie = ''.join(cookie_parts)
        return {"success": True, "cookie": cookie}
    except Exception as e:
        return {"success": False, "message": f"Error parsing appstate: {str(e)}"}
