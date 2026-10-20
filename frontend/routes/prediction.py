import streamlit as st
import pandas as pd
from data import api_client
from ui.components import card, render_lede, render_note, render_section_header

NUMERIC_BOUNDS = {
    'age': (10.0, 40.0),
    'previous_marks': (0.0, 100.0),
    'attendance_pct': (0.0, 100.0),
    'study_hours_per_week': (0.0, 60.0),
    'study_days_per_week': (0.0, 7.0),
    'study_consistency_pct': (0.0, 100.0),
    'sleep_hours_per_night': (0.0, 16.0),
    'quiz_average': (0.0, 100.0),
    'assignment_average': (0.0, 100.0),
    'missed_assignments': (0.0, 30.0),
    'average_attempts': (0.0, 20.0),
    'internet_access': (0.0, 1.0),
}

def render():
    try:
        model_info = api_client.get('model-info')
        defaults = model_info['feature_defaults']
        student_id = st.session_state.get('student_id')
        current_student = api_client.get(f'students/{student_id}')['student'] if student_id else {}
        students = api_client.get('students', params={'limit': 500})['items']
        comparison = api_client.get('model-comparison')
    except api_client.ApiClientError as error:
        st.error(f'Could not connect to the prediction API: {error}')
        return

    render_lede('Classify student performance using the trained model and actual academic inputs.')
    values = {key: current_student.get(key, value) for key, value in defaults.items()}
    with card('inputs'):
        render_section_header('Student Features', f'Model: {model_info["model"] or "Not trained"}')
        columns = st.columns(3)
        for index, (feature, default) in enumerate(values.items()):
            with columns[index % 3]:
                if isinstance(default, (int, float)) and not isinstance(default, bool):
                    low, high = NUMERIC_BOUNDS.get(feature, (float(default) - 10, float(default) + 10))
                    value = max(low, min(high, float(default)))
                    step = 1.0 if feature in {'age', 'study_days_per_week', 'missed_assignments', 'average_attempts', 'internet_access'} else 0.5
                    values[feature] = st.slider(feature.replace('_', ' ').title(), low, high, value, step=step, key=f'predict_{feature}')
                else:
                    options = sorted({str(student.get(feature)) for student in students if student.get(feature) is not None})
                    if str(default) not in options:
                        options.append(str(default))
                    values[feature] = st.selectbox(feature.replace('_', ' ').title(), options, index=options.index(str(default)), key=f'predict_{feature}')
        if st.button('Run Prediction', type='primary'):
            try:
                st.session_state.prediction = api_client.post('predict', {'features': values})
            except api_client.ApiClientError as error:
                st.error(f'Prediction failed: {error}')
    st.write('')
    if st.session_state.get('prediction'):
        result = st.session_state.prediction
        render_section_header('Prediction Result', 'Category prediction from the trained pipeline')
        st.metric('Performance Category', result['predicted_category'].title(), f"Risk: {result['risk_level']}")
        if result.get('confidence') is not None:
            st.progress(float(result['confidence']), text=f"Confidence: {result['confidence']:.1%}")
        if result.get('class_probabilities'):
            probabilities = pd.DataFrame([
                {'Performance Category': label.title(), 'Probability': probability}
                for label, probability in result['class_probabilities'].items()
            ]).sort_values('Probability', ascending=False)
            st.dataframe(probabilities, hide_index=True, use_container_width=True)
        render_note(f"Model artifact: {result['model']}. A category prediction is not a guaranteed final mark.")
    else:
        render_note('Adjust the feature values and run the model to see a prediction.')
    st.write('')
    with card('models'):
        render_section_header('Model Comparison', comparison.get('source', 'Held-out evaluation'))
        metric_frame = pd.DataFrame(comparison.get('models', []))
        if not metric_frame.empty and metric_frame.get('accuracy', pd.Series(dtype=float)).notna().any():
            st.dataframe(metric_frame, hide_index=True, use_container_width=True)
        else:
            render_note('Train the model notebooks to populate held-out model comparisons.')
