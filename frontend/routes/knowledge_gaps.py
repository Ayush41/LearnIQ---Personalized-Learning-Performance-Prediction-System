import streamlit as st
from data import mock_data
from ui.components import card, render_insight_card, render_lede, render_section_header, render_topic_card

def render():
    render_lede('Identify topics where the student needs additional practice.')
    topics = mock_data.KNOWLEDGE_GAPS
    for start in range(0, len(topics), 3):
        for col, t in zip(st.columns(3), topics[start:start + 3]):
            with col:
                render_topic_card(t)
    status = [mock_data.topic_status(t['accuracy']) for t in topics]
    critical = min(topics, key=lambda t: t['accuracy'])['topic']
    with card('summary'):
        render_section_header('Learning Gap Summary')
        a, b, c, d = st.columns(4)
        with a:
            render_insight_card('Strong Topics', status.count('Strong'), '75% accuracy or higher', 'success')
        with b:
            render_insight_card('Moderate', status.count('Moderate'), '50 to 74% accuracy', 'warning')
        with c:
            render_insight_card('Weak', status.count('Weak'), 'Below 50% accuracy', 'danger')
        with d:
            render_insight_card('Critical Attention', critical, 'Lowest accuracy', 'danger')
