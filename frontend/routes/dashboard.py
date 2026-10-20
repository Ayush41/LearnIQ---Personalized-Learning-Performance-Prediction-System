import pandas as pd
import streamlit as st
from data import api_client
from ui import charts
from ui.components import RISK_TONE, card, render_insight_card, render_kpi_card, render_lede, render_progress, render_section_header, render_table

def render():
    student_id = st.session_state.get('student_id')
    if not student_id:
        st.warning('Start the API and select a student to view live analytics.')
        return
    try:
        dashboard_data = api_client.get('dashboard')
        student_data = api_client.get(f'students/{student_id}')
        student = student_data['student']
        prediction = api_client.post('predict', {'features': student})
    except api_client.ApiClientError as error:
        st.error(f'Could not load live dashboard data: {error}')
        return

    render_lede('Live academic and learning analytics from the processed student dataset.')
    risk = student.get('risk_level', prediction['risk_level']).title()
    risk_tone = RISK_TONE.get(risk, 'info')
    confidence = prediction.get('confidence')
    confidence_text = f'{confidence:.0%}' if confidence is not None else 'N/A'
    kpis = [
        ('Predicted Category', prediction['predicted_category'].title(), 'Model output', '◎', 'primary'),
        ('Model Confidence', confidence_text, 'Probability for predicted category', '✓', 'success'),
        ('Risk Level', risk, 'Dataset risk category', '⚑', risk_tone),
        ('Study Hours', f"{student['study_hours_per_week']} hrs/week", 'Recorded weekly average', '◷', 'info'),
        ('Attendance', f"{student['attendance_pct']}%", 'Recorded attendance', '▣', 'primary'),
    ]
    for col, k in zip(st.columns(5), kpis):
        with col:
            render_kpi_card(*k)
    st.write('')
    left, right = st.columns([1.7, 1])
    with left:
        with card('trend'):
            render_section_header('Topic Performance', 'Scores across the selected student’s recorded topics')
            topics = pd.DataFrame(student_data['topics'])
            if not topics.empty:
                topic_chart = topics.sort_values('topic_score')
                st.bar_chart(topic_chart, x='topic', y='topic_score', color='#d65b32', height=300)
            else:
                st.info('No topic-attempt records are available for this student.')
    with right:
        with card('profile'):
            render_section_header('Learning Profile', 'Behaviour indicators')
            render_progress('Study consistency', student['study_consistency_pct'])
            render_progress('Quiz performance', student['quiz_average'])
            render_progress('Attendance', student['attendance_pct'])
            render_progress('Assignment performance', student['assignment_average'])
    st.write('')
    a, b, c = st.columns(3)
    with a:
        render_insight_card('Performance Prediction', prediction['predicted_category'].title(), 'Supervised model output')
    with b:
        render_insight_card('Students in dataset', f"{dashboard_data['student_count']:,}", 'Processed records', 'success')
    with c:
        weak_count = sum(topic['topic_score'] < 50 for topic in student_data['topics'])
        render_insight_card('Knowledge Gaps', weak_count, 'Topics below 50% score', 'warning')
    st.write('')
    with card('students'):
        render_section_header('Selected Student', 'Current record from the processed dataset')
        summary = pd.DataFrame([{
            'Student ID': student['student_id'],
            'Performance Category': student['performance_category'].title(),
            'Final Marks': student['final_marks'],
            'Attendance': f"{student['attendance_pct']}%",
            'Average Quiz': f"{student['quiz_average']}%",
            'Pass Rate (Dataset)': f"{dashboard_data['pass_rate']}%",
        }])
        render_table(summary)
