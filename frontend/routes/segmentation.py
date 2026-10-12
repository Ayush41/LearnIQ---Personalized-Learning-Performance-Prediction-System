import streamlit as st
from data import mock_data
from ui import charts
from ui.components import card, render_cluster_card, render_insight_card, render_lede, render_note, render_section_header

def render():
    name = st.session_state.student
    s = mock_data.STUDENTS[name]
    data = mock_data.CLUSTER_DATA
    render_lede('Discover student groups using K-Means clustering.')
    a, b, c = st.columns(3)
    with a:
        render_insight_card('Algorithm', data['summary']['algorithm'], 'Unsupervised learning')
    with b:
        render_insight_card('Clusters', data['summary']['clusters'], 'Groups of similar students')
    with c:
        render_insight_card('Silhouette Score', data['summary']['silhouette'], 'Cluster separation (demo value)', 'success')
    st.write('')
    with card('clusters'):
        render_section_header('Cluster Visualization', 'Study hours vs quiz average')
        st.plotly_chart(charts.cluster_chart(data['points'], data['clusters'], name, s['hours'], s['quiz']), use_container_width=True, config={'displayModeBar': False})
    st.write('')
    selected = next((i for i, c in enumerate(data['clusters']) if c['name'] == s['segment']), None)
    for i, (col, cluster) in enumerate(zip(st.columns(4), data['clusters'])):
        with col:
            st.markdown(f'**Cluster {i + 1}**')
            render_cluster_card(cluster, is_selected=i == selected)
    render_note('These descriptions are demonstration interpretations of mock K-Means results. Real cluster meanings will be derived from the trained model.')
