import streamlit as st
from data import mock_data
from ui.components import card, render_compare_bars, render_insight_card, render_lede, render_note, render_section_header, render_stat_tile

def render():
    cur = mock_data.WHAT_IF_DATA['current']
    dflt = mock_data.WHAT_IF_DATA['defaults']
    render_lede("Explore how changes in learning behavior may affect the model's predicted performance.")
    left, right = st.columns([1, 1.4])
    with left:
        with card('current'):
            render_section_header('Current State', 'Baseline used for the comparison')
            a, b = st.columns(2)
            with a:
                render_stat_tile('Predicted Score', f"{cur['score']}%")
                st.write('')
                render_stat_tile('Quiz Average', f"{cur['quiz']}%")
            with b:
                render_stat_tile('Study Hours', f"{cur['study_hours']}/day")
                st.write('')
                render_stat_tile('Attendance', f"{cur['attendance']}%")
    with right:
        with card('controls'):
            render_section_header('Scenario Controls', 'Change the inputs to build a scenario')
            c1, c2 = st.columns(2)
            hours = c1.slider('Study Hours (per day)', 0, 12, dflt['study_hours'])
            quiz = c2.slider('Quiz Average (%)', 0, 100, dflt['quiz'])
            att = c1.slider('Attendance (%)', 0, 100, dflt['attendance'])
            assign = c2.slider('Assignment Average (%)', 0, 100, dflt['assignment'])
            if st.button('Calculate Scenario', type='primary'):
                st.session_state.scenario = mock_data.mock_scenario(hours, quiz, att, assign)
    st.write('')
    scenario = st.session_state.get('scenario', mock_data.mock_scenario(**dflt))
    change = scenario - cur['score']
    with card('result'):
        render_section_header('Result', 'Current prediction compared with the scenario')
        a, b, c = st.columns([1, 1, 1])
        with a:
            render_insight_card('Current Prediction', f"{cur['score']}%", 'Baseline')
        with b:
            render_insight_card('Scenario Prediction', f'{scenario}%', 'With the changed inputs', 'success' if change >= 0 else 'danger')
        with c:
            kind = 'delta' if change >= 0 else 'delta neg'
            st.markdown(f'<div style="padding-top:1.3rem"><span class="{kind}">{change:+d} marks</span></div>', unsafe_allow_html=True)
        render_compare_bars(cur['score'], scenario)
        render_note('This is scenario analysis using model inputs. It does not represent a guaranteed future outcome.')
