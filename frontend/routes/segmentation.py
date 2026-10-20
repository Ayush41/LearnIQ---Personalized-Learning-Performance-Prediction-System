import streamlit as st
import pandas as pd
from data import api_client
from ui.components import card, render_insight_card, render_lede, render_note, render_section_header

def render():
    student_id = st.session_state.get('student_id')
    if not student_id:
        st.warning('Select a student to view student segments.')
        return
    try:
        data = api_client.get('segments', params={'clusters': 4})
    except api_client.ApiClientError as error:
        st.error(f'Could not calculate student segments: {error}')
        return
    render_lede('Explore groups found by K-Means using study behavior and academic inputs.')
    a, b, c = st.columns(3)
    with a:
        render_insight_card('Algorithm', 'K-Means', 'Unsupervised learning')
    with b:
        render_insight_card('Clusters', len(data['clusters']), 'Groups of similar students')
    with c:
        score = data['silhouette_score']
        render_insight_card('Silhouette Score', f'{score:.3f}' if score is not None else 'N/A', 'Cluster separation on this dataset', 'success')
    st.write('')
    with card('clusters'):
        render_section_header('Student Clusters', 'Study hours per week vs quiz average')
        points = pd.DataFrame(data['students'])
        if not points.empty:
            st.scatter_chart(points, x='study_hours_per_week', y='quiz_average', color='name', size='final_marks', height=420)
            st.caption(f'Selected student: {student_id}')
    st.write('')
    with card('cluster-summary'):
        render_section_header('Cluster Summary', 'Groups sorted by average final marks')
        st.dataframe(pd.DataFrame(data['clusters']), hide_index=True, use_container_width=True)
    render_note('Clusters are recomputed from the processed dataset. They describe similar student profiles and are not performance predictions.')
