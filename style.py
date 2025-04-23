import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the application."""
    st.markdown("""
    <style>
        /* Global Styles */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-color: #7B68EE;
            --secondary-color: #4B0082;
            --background-color: #121212;
            --card-background: #1E1E1E;
            --text-color: #FFFFFF;
            --accent-color: #FF4500;
            --success-color: #4CAF50;
            --error-color: #F44336;
            --border-radius: 10px;
            --box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* 3D Effects */
        .stButton > button {
            background: linear-gradient(145deg, #2a2a2a, #232323);
            color: white;
            border-radius: var(--border-radius);
            border: none;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(1px);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        /* Header */
        .header-container {
            display: flex;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .logo-container {
            width: 60px;
            height: 60px;
            margin-right: 20px;
        }
        
        .logo {
            filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.5));
        }
        
        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            margin: 0;
        }
        
        /* Sections */
        .section-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
            position: relative;
            padding-left: 15px;
        }
        
        .section-title::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, var(--primary-color), var(--secondary-color));
            border-radius: 10px;
        }
        
        /* Welcome Screen */
        .welcome-container {
            background: rgba(30, 30, 30, 0.6);
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--box-shadow);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 2rem;
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        .welcome-title {
            font-size: 2rem;
            margin-bottom: 1rem;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .welcome-text {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .features-container {
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
        }
        
        .feature {
            flex: 1;
            background: rgba(30, 30, 30, 0.8);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin: 0 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transform: translateZ(10px);
            transition: transform 0.3s ease;
        }
        
        .feature:hover {
            transform: translateZ(20px) scale(1.03);
        }
        
        .feature h3 {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        
        /* Login/Admin Containers */
        .login-container, .admin-login {
            background: rgba(30, 30, 30, 0.6);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--box-shadow);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .admin-login {
            border-left: 4px solid var(--accent-color);
        }
        
        .login-info-card, .admin-info-card {
            background: rgba(40, 40, 40, 0.6);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            height: 100%;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .admin-info-card {
            border-left: 4px solid var(--accent-color);
        }
        
        .login-info-card h3, .admin-info-card h3 {
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        
        .login-info-card ul, .admin-info-card ul {
            padding-left: 1.2rem;
        }
        
        .login-info-card li, .admin-info-card li {
            margin-bottom: 0.5rem;
        }
        
        /* User Dashboard */
        .user-info, .admin-info {
            background: rgba(30, 30, 30, 0.7);
            padding: 0.8rem;
            border-radius: var(--border-radius);
            margin-bottom: 1.5rem;
            font-weight: 500;
            border-left: 3px solid var(--primary-color);
        }
        
        .admin-info {
            border-left: 3px solid var(--accent-color);
        }
        
        /* Cookie Getter */
        .cookie-getter-header, .share-booster-header, .admin-dashboard-header {
            margin-bottom: 2rem;
        }
        
        .method-description {
            background: rgba(30, 30, 30, 0.6);
            border-radius: var(--border-radius);
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-left: 3px solid var(--primary-color);
        }
        
        .method-description h3 {
            margin-bottom: 0.5rem;
        }
        
        .cookie-info {
            background: rgba(40, 40, 40, 0.6);
            padding: 1rem;
            border-radius: var(--border-radius);
            margin-top: 1rem;
            border-left: 3px solid var(--success-color);
        }
        
        .cookie-info-card {
            background: rgba(40, 40, 40, 0.6);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            height: 100%;
            border-left: 3px solid var(--primary-color);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .cookie-info-card.advanced {
            border-left: 3px solid var(--accent-color);
        }
        
        /* Share Booster */
        .share-progress {
            font-size: 1.1rem;
            padding: 0.8rem;
            background: rgba(76, 175, 80, 0.1);
            border-left: 3px solid var(--success-color);
            border-radius: var(--border-radius);
            margin: 0.5rem 0;
        }
        
        .share-error {
            font-size: 1.1rem;
            padding: 0.8rem;
            background: rgba(244, 67, 54, 0.1);
            border-left: 3px solid var(--error-color);
            border-radius: var(--border-radius);
            margin: 0.5rem 0;
        }
        
        .share-complete {
            font-size: 1.2rem;
            padding: 1rem;
            background: rgba(76, 175, 80, 0.15);
            border-left: 3px solid var(--success-color);
            border-radius: var(--border-radius);
            margin: 1rem 0;
            font-weight: 500;
        }
        
        /* Admin Dashboard */
        .user-table-container {
            overflow-x: auto;
            margin-bottom: 2rem;
        }
        
        .user-table {
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            background: rgba(30, 30, 30, 0.6);
            border-radius: var(--border-radius);
            overflow: hidden;
        }
        
        .user-table thead {
            background: rgba(40, 40, 40, 0.8);
        }
        
        .user-table th, .user-table td {
            padding: 0.8rem 1rem;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .user-table tr:last-child td {
            border-bottom: none;
        }
        
        .remove-user-btn {
            background: rgba(244, 67, 54, 0.2);
            color: white;
            border: 1px solid rgba(244, 67, 54, 0.5);
            padding: 0.3rem 0.6rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .remove-user-btn:hover {
            background: rgba(244, 67, 54, 0.4);
        }
        
        /* Footer */
        .footer {
            margin-top: 3rem;
            padding: 1rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .features-container {
                flex-direction: column;
            }
            
            .feature {
                margin: 0.5rem 0;
            }
            
            .header-container {
                flex-direction: column;
                text-align: center;
            }
            
            .logo-container {
                margin-right: 0;
                margin-bottom: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
