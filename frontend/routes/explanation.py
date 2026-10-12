import streamlit as st
from data import mock_data
from ui import charts
from ui.components import RISK_TONE, card, render_insight_card, render_lede, render_note, render_section_header

def render():
    name = st.session_state.student
    s = mock_data.STUDENTS[name]
    render_lede('Understand which features contributed to the model prediction.')
    a, b = st.columns(2)
    with a:
        render_insight_card('Predicted Score', f"{s['predicted']}%", 'Prediction Summary')
    with b:
        render_insight_card('Risk', s['risk'], 'Prediction Summary', RISK_TONE[s['risk']])
    st.write('')
    with card('shap'):
        render_section_header('Feature Contributions', 'Marks added to (or taken from) the average prediction')
        st.plotly_chart(charts.feature_importance_chart(mock_data.get_contributions(name)), use_container_width=True, config={'displayModeBar': False})
        render_note('These values are demonstration SHAP-style feature contributions. Actual SHAP values will be supplied by the ML backend.')
