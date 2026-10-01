import streamlit as st
from data import mock_data
from ui import charts
from ui.components import card, render_lede, render_note, render_result_card, render_section_header, render_table

def render():
    render_lede('Estimate student performance using academic and learning behavior features.')
    with card('inputs'):
        render_section_header('Input Features', 'Academic and learning behaviour values for one student')
        c1, c2 = st.columns(2)
        prev = c1.slider('Previous Marks (%)', 0, 100, 75)
        quiz = c2.slider('Quiz Average (%)', 0, 100, 78)
        assign = c1.slider('Assignment Average (%)', 0, 100, 80)
        att = c2.slider('Attendance (%)', 0, 100, 91)
        hours = c1.slider('Study Hours (per week)', 0, 40, 14)
        freq = c2.slider('Study Frequency (days per week)', 0, 7, 5)
        if st.button('Run Prediction', type='primary'):
            st.session_state.prediction = mock_data.mock_predict(prev, quiz, assign, att, hours, freq)
    st.write('')
    if 'prediction' in st.session_state:
        render_result_card(st.session_state.prediction)
    else:
        render_note('Set the feature values above and choose Run Prediction to see the result.')
    st.write('')
    with card('models'):
        render_section_header('Model Comparison', 'Demonstration model results')
        left, right = st.columns([1.5, 1])
        with left:
            render_table(mock_data.MODEL_COMPARISON, best_cols=['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC'])
        with right:
            st.plotly_chart(charts.model_accuracy_chart(mock_data.MODEL_COMPARISON), use_container_width=True, config={'displayModeBar': False})
        render_note('Demonstration model results. These are placeholder numbers, not real trained results.')
