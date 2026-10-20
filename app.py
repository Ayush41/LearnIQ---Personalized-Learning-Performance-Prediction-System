import sys
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"
if str(FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(FRONTEND_DIR))

import streamlit as st
from routes import register_routes
from ui.components import render_page_header
from ui.auth import render_login
from ui.sidebar import render_sidebar
from ui.styles import load_css
st.set_page_config(page_title='LearnIQ', page_icon='🎓', layout='wide', initial_sidebar_state='expanded')
load_css()
st.session_state.setdefault('student', 'Aarav Sharma')
st.session_state.setdefault('authenticated', False)
if not st.session_state.authenticated:
    render_login()
    st.stop()
pages = register_routes()
pg = st.navigation(pages, position='hidden')
render_sidebar(pages)
render_page_header(pg.title)
pg.run()
