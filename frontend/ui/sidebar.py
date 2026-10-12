"""Custom LearnIQ sidebar navigation."""
import streamlit as st
from ui.auth import logout

def render_sidebar(pages):
    """Render the custom sidebar using the registered Streamlit pages."""
    with st.sidebar:
        st.markdown('\n            <div class="brand">\n                <div class="brand-name">\n                    Learn<span>IQ</span>\n                </div>\n                <div class="brand-sub">\n                    Personalized Learning Analytics\n                </div>\n            </div>\n            ', unsafe_allow_html=True)
        for page in pages:
            st.page_link(page, label=page.title, icon=page.icon, use_container_width=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        if st.button('Logout', key='logout_button', use_container_width=True):
            logout()
