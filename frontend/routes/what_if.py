import streamlit as st
from data import api_client
from ui.components import card, render_insight_card, render_lede, render_note, render_section_header, render_stat_tile

def render():
    student_id = st.session_state.get('student_id')
    if not student_id:
        st.warning('Select a student to run scenario analysis.')
        return
    if st.session_state.get('_scenario_student_id') != student_id:
        st.session_state.pop('scenario_current', None)
        st.session_state.pop('scenario_prediction', None)
        st.session_state._scenario_student_id = student_id
    try:
        student = api_client.get(f'students/{student_id}')['student']
    except api_client.ApiClientError as error:
        st.error(f'Could not load this student: {error}')
        return
    features = {
        key: value for key, value in student.items()
        if key not in {'student_id', 'performance_category', 'risk_level', 'final_marks', 'passed'}
    }
    current_result = st.session_state.get('scenario_current')
    scenario_result = st.session_state.get('scenario_prediction')
    render_lede("Compare the model's category prediction for this student with a changed study scenario.")
    left, right = st.columns([1, 1.4])
    with left:
        with card('current'):
            render_section_header('Current State', f'Student {student_id}')
            a, b = st.columns(2)
            with a:
                render_stat_tile('Previous Marks', f"{student['previous_marks']}%")
                st.write('')
                render_stat_tile('Quiz Average', f"{student['quiz_average']}%")
            with b:
                render_stat_tile('Study Hours', f"{student['study_hours_per_week']}/week")
                st.write('')
                render_stat_tile('Attendance', f"{student['attendance_pct']}%")
    with right:
        with card('controls'):
            render_section_header('Scenario Controls', 'Change the inputs to build a scenario')
            c1, c2 = st.columns(2)
            hours = c1.slider('Study Hours (per week)', 0.0, 60.0, float(student['study_hours_per_week']), step=0.5)
            quiz = c2.slider('Quiz Average (%)', 0.0, 100.0, float(student['quiz_average']), step=1.0)
            att = c1.slider('Attendance (%)', 0.0, 100.0, float(student['attendance_pct']), step=1.0)
            assign = c2.slider('Assignment Average (%)', 0.0, 100.0, float(student['assignment_average']), step=1.0)
            if st.button('Calculate Scenario', type='primary'):
                scenario_features = {**features, 'study_hours_per_week': hours, 'quiz_average': quiz, 'attendance_pct': att, 'assignment_average': assign}
                try:
                    results = api_client.post('what-if', {'current': features, 'scenario': scenario_features})
                    st.session_state.scenario_current = results['current']
                    st.session_state.scenario_prediction = results['scenario']
                except api_client.ApiClientError as error:
                    st.error(f'Scenario prediction failed: {error}')
    st.write('')
    with card('result'):
        render_section_header('Result', 'Current prediction compared with the scenario')
        a, b, c = st.columns([1, 1, 1])
        if current_result and scenario_result:
            with a:
                confidence = current_result.get('confidence')
                render_insight_card('Current Category', current_result['predicted_category'].title(), f'Confidence: {confidence:.1%}' if confidence is not None else 'Baseline')
            with b:
                confidence = scenario_result.get('confidence')
                render_insight_card('Scenario Category', scenario_result['predicted_category'].title(), f'Confidence: {confidence:.1%}' if confidence is not None else 'Changed inputs', 'success' if current_result['predicted_category'] == scenario_result['predicted_category'] else 'warning')
            with c:
                render_insight_card('Category Changed', 'Yes' if current_result['predicted_category'] != scenario_result['predicted_category'] else 'No', 'Model output only')
            render_note('Scenario changes show how this model responds to inputs; they are not a causal estimate or a guaranteed outcome.')
        else:
            st.info('Change one or more inputs and calculate a scenario to compare model outputs.')
