"""LearnIQ page route registry.

This module keeps all page definitions in one place, similar to a
route registration module in a FastAPI application.
"""
import streamlit as st
from routes import dashboard, explanation, knowledge_gaps, prediction, recommendations, segmentation, what_if

def register_routes():
    """Create and register all LearnIQ Streamlit pages."""
    return [st.Page(dashboard.render, title='Dashboard', icon=':material/dashboard:', url_path='dashboard', default=True), st.Page(prediction.render, title='Performance Prediction', icon=':material/query_stats:', url_path='prediction'), st.Page(segmentation.render, title='Student Segmentation', icon=':material/hub:', url_path='student-segmentation'), st.Page(knowledge_gaps.render, title='Knowledge Gaps', icon=':material/track_changes:', url_path='knowledge-gaps'), st.Page(recommendations.render, title='Study Recommendations', icon=':material/school:', url_path='study-recommendations'), st.Page(what_if.render, title='What-if Analysis', icon=':material/tune:', url_path='what-if'), st.Page(explanation.render, title='Explainable ML', icon=':material/lightbulb:', url_path='explainable-ml')]
__all__ = ['register_routes']
