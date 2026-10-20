"""Small reusable UI pieces. Most functions draw HTML with st.markdown; the
*_html ones return a string so they can be nested inside other HTML."""
import streamlit as st
from data import api_client
from data import mock_data
BADGE_KIND = {'Low': 'success', 'Strong': 'success', 'Good': 'success', 'Medium': 'warning', 'Moderate': 'warning', 'High': 'danger', 'Weak': 'danger'}
RISK_TONE = {'Low': 'success', 'Medium': 'warning', 'High': 'danger'}

def _html(markup):
    st.markdown(markup, unsafe_allow_html=True)

def tone_for(value):
    return 'success' if value >= 75 else 'warning' if value >= 50 else 'danger'

def card(key):
    """A white card container (styled by the st-key-card_ CSS rule). Use with `with`."""
    return st.container(key=f'card_{key}')

def render_status_badge(text, kind=None):
    return f"""<span class="badge {kind or BADGE_KIND.get(text, 'info')}">{text}</span>"""

def render_page_header(title):
    left, mid, right = st.columns([3.2, 1.7, 1], vertical_alignment='center')
    left.markdown(
        f'<div class="page-title">{title}</div>'
        '<div class="page-tag">Machine Learning-Based Personalized Learning</div>',
        unsafe_allow_html=True,
    )
    try:
        students = api_client.get('students', params={'limit': 500})['items']
        student_ids = [student['student_id'] for student in students]
        if student_ids:
            current_id = st.session_state.get('student_id')
            if current_id not in student_ids:
                st.session_state.student_id = student_ids[0]
            mid.selectbox('Student', student_ids, key='student_id', label_visibility='collapsed')
        else:
            mid.caption('No student records')
        right.markdown('<span class="status"><i></i>API connected</span>', unsafe_allow_html=True)
    except api_client.ApiClientError:
        mid.caption('API unavailable')
        right.markdown('<span class="status"><i></i>Offline</span>', unsafe_allow_html=True)

def render_lede(text):
    _html(f'<div class="lede">{text}</div>')

def render_section_header(title, subtitle=''):
    sub = f'<div class="sec-sub">{subtitle}</div>' if subtitle else ''
    _html(f'<div class="sec"><div class="sec-title">{title}</div>{sub}</div>')

def render_note(text):
    _html(f'<div class="note">{text}</div>')

def render_kpi_card(label, value, sub, icon, tone='primary'):
    _html(f'<div class="kpi"><div class="kpi-top"><span class="kpi-label">{label}</span><span class="ico {tone}">{icon}</span></div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>')

def render_insight_card(label, value, sub='', tone='primary'):
    _html(f'<div class="insight {tone}"><div class="insight-label">{label}</div><div class="insight-value">{value}</div><div class="insight-sub">{sub}</div></div>')

def render_progress(label, value, tone=None):
    _html(f"""<div class="prog"><div class="prog-head"><span>{label}</span><b>{value}%</b></div><div class="bar"><span class="fill {tone or ''}" style="width:{value}%"></span></div></div>""")

def render_table(df, highlight=None, badge_cols=(), best_cols=()):
    """HTML table. `highlight` = value of the first column to highlight; best_cols get the max in bold."""
    best = {c: df[c].max() for c in best_cols}
    head = ''.join((f'<th>{c}</th>' for c in df.columns))
    rows = ''
    for _, r in df.iterrows():
        cells = ''
        for c in df.columns:
            v = r[c]
            if c in badge_cols:
                text = render_status_badge(str(v))
            else:
                text = f'{v:.2f}' if isinstance(v, float) else str(v)
                if c in best and v == best[c]:
                    text = f'<b>{text}</b>'
            cells += f'<td>{text}</td>'
        cls = ' class="hl"' if highlight is not None and r.iloc[0] == highlight else ''
        rows += f'<tr{cls}>{cells}</tr>'
    _html(f'<table class="tbl"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>')

def render_result_card(result):
    _html(f"""<div class="result-box"><div class="result-label">Predicted Score</div><div class="result-score">{result['score']} / 100</div><div class="result-row"><div><span>Performance</span><b>{result['performance']}</b></div><div><span>Risk</span><b>{result['risk']}</b></div><div><span>Pass Probability</span><b>{result['pass_prob']}%</b></div></div></div>""")

def render_stat_tile(label, value):
    _html(f'<div class="tile"><div class="tile-label">{label}</div><div class="tile-value">{value}</div></div>')

def render_topic_card(t):
    status = mock_data.topic_status(t['accuracy'])
    tone = BADGE_KIND[status]
    _html(f"""<div class="topic"><div class="topic-head"><span class="topic-name">{t['topic']}</span>{render_status_badge(status)}</div><div class="topic-acc">{t['accuracy']}%</div><div class="bar"><span class="fill {tone}" style="width:{t['accuracy']}%"></span></div><div class="topic-meta">Difficulty: {t['difficulty']}<br>Prerequisites: {t['prerequisites']}</div></div>""")

def render_cluster_card(c, is_selected=False):
    mark = ' ' + render_status_badge('Selected student', 'info') if is_selected else ''
    lines = ''.join((f'<div class="cluster-line">{x}</div>' for x in c['lines']))
    _html(f"""<div class="cluster" style="--c:{c['color']}"><div class="cluster-name">{c['name']}{mark}</div>{lines}</div>""")

def render_recommendation_card(r):
    _html(f"""<div class="rec"><div class="rec-n">{r['n']}</div><div class="rec-body"><div class="rec-title">{r['title']}</div><div class="rec-reason">Reason: {r['reason']}</div></div><div class="rec-meta">{render_status_badge(r['priority'])}<span>{r['time']}</span></div></div>""")

def render_compare_bars(current, scenario):
    pos = scenario >= current
    _html(f"""<div class="cmp-row"><span class="cmp-label">Current</span><div class="cmp-bar bar"><span class="fill" style="width:{current}%;background:#94a3b8"></span></div><b>{current}</b></div><div class="cmp-row"><span class="cmp-label">Scenario</span><div class="cmp-bar bar"><span class="fill {('success' if pos else 'danger')}" style="width:{scenario}%"></span></div><b>{scenario}</b></div>""")


