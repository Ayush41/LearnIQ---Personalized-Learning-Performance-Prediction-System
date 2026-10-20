"""Simple login screen for the LearnIQ frontend prototype."""
import streamlit as st
USERNAME = 'admin'
PASSWORD = 'admin123'

def render_login() -> bool:
    """Render login form and return True when authentication succeeds."""
    st.markdown('\n        <div class="login-wrap">\n            <div class="login-card">\n                <div class="login-brand">Learn<span>IQ</span></div>\n                <div class="login-subtitle">Personalized Learning Analytics</div>\n                <div class="login-title">Welcome back</div>\n                <div class="login-help">Sign in to access your student analytics dashboard.</div>\n            </div>\n        </div>\n        ', unsafe_allow_html=True)
    left, center, right = st.columns([1, 1.15, 1])
    with center:
        with st.form('login_form'):
            username = st.text_input('Username / Email', placeholder='Enter your username')
            password = st.text_input('Password', type='password', placeholder='Enter your password')
            submitted = st.form_submit_button('Login', type='primary', use_container_width=True)
            if submitted:
                if username.strip().lower() == USERNAME and password == PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.logged_in_user = USERNAME
                    st.rerun()
                else:
                    st.error('Invalid username or password.')
    return st.session_state.get('authenticated', False)

def logout() -> None:
    """Log the current user out."""
    st.session_state.authenticated = False
    st.session_state.pop('logged_in_user', None)
    st.rerun()
