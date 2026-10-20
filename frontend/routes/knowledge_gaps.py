import streamlit as st
from data import api_client
from ui.components import card, render_insight_card, render_lede, render_section_header, render_topic_card

def render():
    student_id = st.session_state.get('student_id')
    if not student_id:
        st.warning('Select a student to view topic performance.')
        return
    try:
        topics = api_client.get(f'students/{student_id}/knowledge-gaps')['topics']
    except api_client.ApiClientError as error:
        st.error(f'Could not load knowledge gaps: {error}')
        return
    render_lede(f'Topic mastery and areas to work on for student {student_id}.')
    if not topics:
        st.info('No topic-attempt records are available for this student.')
        return
    topic_cards = [
        {
            'topic': topic['topic'].title(),
            'accuracy': round(float(topic['topic_score'])),
            'difficulty': topic['topic_difficulty'],
            'prerequisites': f"{topic['attempt_count']} attempts · {topic['study_minutes']} study minutes",
        }
        for topic in topics
    ]
    for start in range(0, len(topic_cards), 3):
        for col, topic in zip(st.columns(3), topic_cards[start:start + 3]):
            with col:
                render_topic_card(topic)
    status = [topic['status'] for topic in topics]
    critical = min(topics, key=lambda topic: topic['topic_score'])['topic'].title()
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
