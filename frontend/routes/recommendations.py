from data import mock_data
from ui.components import card, render_insight_card, render_lede, render_note, render_recommendation_card, render_section_header
import streamlit as st

def render():
    render_lede('Recommended learning actions based on performance and knowledge gaps.')
    for rec in mock_data.RECOMMENDATIONS:
        render_recommendation_card(rec)
    with card('eval'):
        render_section_header('Recommendation Evaluation')
        a, b = st.columns(2)
        metrics = mock_data.RECOMMENDATION_METRICS
        with a:
            render_insight_card('Precision@3', metrics['Precision@3'], 'Relevant items in top 3')
        with b:
            render_insight_card('Recall@3', metrics['Recall@3'], 'Relevant items found in top 3')
        render_note('Demonstration evaluation metrics.')
