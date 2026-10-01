import pandas as pd
import streamlit as st
from data import mock_data
from ui import charts
from ui.components import RISK_TONE, card, render_insight_card, render_kpi_card, render_lede, render_progress, render_section_header, render_table

def render():
    name = st.session_state.student
    s = mock_data.STUDENTS[name]
    render_lede('Overview of academic performance, learning behavior and ML predictions.')
    kpis = [('Predicted Score', f"{s['predicted']} / 100", 'Model estimate', '◎', 'primary'), ('Pass Probability', f"{s['pass_prob']}%", 'Likelihood of passing', '✓', 'success'), ('Risk Level', s['risk'], 'Based on predicted score', '⚑', RISK_TONE[s['risk']]), ('Study Hours', f"{s['hours']} hrs/week", 'Weekly average', '◷', 'info'), ('Attendance', f"{s['attendance']}%", 'Current term', '▣', 'primary')]
    for col, k in zip(st.columns(5), kpis):
        with col:
            render_kpi_card(*k)
    st.write('')
    left, right = st.columns([1.7, 1])
    with left:
        with card('trend'):
            render_section_header('Performance Trend', 'Quiz / assessment performance over time')
            st.plotly_chart(charts.performance_chart(mock_data.PERFORMANCE_DATA['labels'], mock_data.PERFORMANCE_DATA['scores'][name]), use_container_width=True, config={'displayModeBar': False})
    with right:
        with card('profile'):
            render_section_header('Learning Profile', 'Behaviour indicators')
            render_progress('Study consistency', s['consistency'])
            render_progress('Quiz performance', s['quiz'])
            render_progress('Attendance', s['attendance'])
            render_progress('Assignment performance', s['assignment'])
    st.write('')
    a, b, c = st.columns(3)
    with a:
        render_insight_card('Performance Prediction', f"{s['predicted']} predicted marks", 'Supervised model output')
    with b:
        render_insight_card('Student Segment', s['segment'], 'K-Means cluster', 'success')
    with c:
        render_insight_card('Knowledge Status', f"{s['weak_topics']} topics need attention", 'Topics below 50% accuracy', 'warning')
    st.write('')
    with card('students'):
        render_section_header('Student Summary', 'Selected student is highlighted')
        df = pd.DataFrame([{'Student': n, 'Predicted Score': v['predicted'], 'Risk': v['risk'], 'Segment': v['segment'], 'Attendance': f"{v['attendance']}%"} for n, v in mock_data.STUDENTS.items()])
        render_table(df, highlight=name, badge_cols=('Risk',))
