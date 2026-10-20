from data import api_client
from ui.components import card, render_insight_card, render_lede, render_note, render_recommendation_card, render_section_header
import streamlit as st

def render():
    student_id = st.session_state.get('student_id')
    if not student_id:
        st.warning('Select a student to view recommendations.')
        return
    try:
        response = api_client.get(f'students/{student_id}/recommendations')
    except api_client.ApiClientError as error:
        st.error(f'Could not load study recommendations: {error}')
        return
    render_lede(f'Practice suggestions generated from topic scores for student {student_id}.')
    for index, item in enumerate(response['recommendations'], start=1):
        render_recommendation_card({
            'n': f'{index:02d}',
            'title': item['action'],
            'reason': f"{item['topic'].title()} score is {item['score']:.1f}%.",
            'priority': item['priority'],
            'time': f"{item['estimated_minutes']} minutes",
        })
    if not response['recommendations']:
        st.success('No topics need additional practice based on the current threshold.')
    with card('eval'):
        render_section_header('Recommendation Logic')
        render_insight_card('Priority Rule', 'Weak topics first', 'Below 50% is high priority; 50–74% is medium.')
        render_note('These score-based practice suggestions are an MVP, not a validated adaptive recommender.')
