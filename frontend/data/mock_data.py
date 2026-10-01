"""All temporary demonstration data for LearnIQ lives here.

FUTURE BACKEND: every constant and mock_* function in this file is replaced by
an API call made by the backend team. The pages only read from this module.
"""
import math
import numpy as np
import pandas as pd
STUDENTS = {'Aarav Sharma': dict(id='S101', predicted=78, pass_prob=98, risk='Low', hours=14, attendance=91, segment='Consistent Learner', quiz=78, assignment=80, consistency=82, weak_topics=2), 'Meera Nair': dict(id='S102', predicted=85, pass_prob=99, risk='Low', hours=17, attendance=95, segment='High Performers', quiz=88, assignment=90, consistency=90, weak_topics=1), 'Rohan Verma': dict(id='S103', predicted=64, pass_prob=82, risk='Medium', hours=9, attendance=78, segment='Moderate Performers', quiz=62, assignment=65, consistency=64, weak_topics=3), 'Sana Iqbal': dict(id='S104', predicted=81, pass_prob=97, risk='Low', hours=8, attendance=88, segment='Efficient Learners', quiz=82, assignment=79, consistency=75, weak_topics=2), 'Kabir Singh': dict(id='S105', predicted=48, pass_prob=55, risk='High', hours=5, attendance=62, segment='Needs Support', quiz=44, assignment=50, consistency=40, weak_topics=4), 'Ananya Joshi': dict(id='S106', predicted=71, pass_prob=90, risk='Medium', hours=11, attendance=84, segment='Moderate Performers', quiz=70, assignment=72, consistency=70, weak_topics=2)}
PERFORMANCE_DATA = {'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Exam'], 'scores': {'Aarav Sharma': [62, 68, 71, 74, 77, 78], 'Meera Nair': [75, 79, 82, 84, 86, 85], 'Rohan Verma': [55, 52, 60, 58, 63, 64], 'Sana Iqbal': [70, 74, 76, 79, 80, 81], 'Kabir Singh': [50, 46, 52, 44, 47, 48], 'Ananya Joshi': [60, 64, 66, 68, 70, 71]}}
MODEL_COMPARISON = pd.DataFrame({'Model': ['Logistic Regression', 'Random Forest', 'SVM', 'XGBoost'], 'Accuracy': [0.82, 0.88, 0.85, 0.91], 'Precision': [0.8, 0.87, 0.84, 0.9], 'Recall': [0.79, 0.86, 0.82, 0.89], 'F1': [0.79, 0.86, 0.83, 0.89], 'ROC-AUC': [0.87, 0.93, 0.9, 0.95]})

def _make_cluster_points():
    rng = np.random.default_rng(7)
    centers = [(18, 85), (8, 80), (6, 45), (12, 65)]
    frames = []
    for i, (x, y) in enumerate(centers):
        frames.append(pd.DataFrame({'Study Hours': rng.normal(x, 1.8, 25).round(1), 'Quiz Average': np.clip(rng.normal(y, 5, 25), 0, 100).round(1), 'Cluster': i}))
    return pd.concat(frames, ignore_index=True)
CLUSTER_DATA = {'summary': {'algorithm': 'K-Means', 'clusters': 4, 'silhouette': 0.52}, 'clusters': [dict(name='High Performers', lines=['High marks', 'High consistency'], color='#4338ca'), dict(name='Efficient Learners', lines=['Good marks', 'Low study hours'], color='#0d9488'), dict(name='Needs Support', lines=['Low marks', 'Irregular study'], color='#d97706'), dict(name='Moderate Performers', lines=['Average marks', 'Good attendance'], color='#64748b')], 'points': _make_cluster_points()}
KNOWLEDGE_GAPS = [dict(topic='Arrays', accuracy=92, difficulty='Easy', prerequisites='Basic programming'), dict(topic='Linked List', accuracy=85, difficulty='Medium', prerequisites='Arrays, Pointers'), dict(topic='Stack', accuracy=66, difficulty='Medium', prerequisites='Arrays, Linked List'), dict(topic='Trees', accuracy=41, difficulty='Hard', prerequisites='Linked List, Recursion'), dict(topic='Graphs', accuracy=30, difficulty='Hard', prerequisites='Trees, Queues')]

def topic_status(accuracy):
    if accuracy >= 75:
        return 'Strong'
    return 'Moderate' if accuracy >= 50 else 'Weak'
RECOMMENDATIONS = [dict(n='01', title='Revise Stack', reason='Current accuracy is 66%.', priority='Medium', time='30 minutes'), dict(n='02', title='Study Binary Trees', reason='Trees accuracy is 41%.', priority='High', time='60 minutes'), dict(n='03', title='Practice Tree Traversal', reason='Strengthen weak subtopic.', priority='High', time='45 minutes'), dict(n='04', title='Study Graph Basics', reason='Graphs accuracy is 30%.', priority='High', time='60 minutes'), dict(n='05', title='Attempt Topic Quiz', reason='Measure improvement.', priority='Medium', time='20 minutes')]
RECOMMENDATION_METRICS = {'Precision@3': 0.74, 'Recall@3': 0.68}
SHAP_DATA = {'base_value': 64.1, 'contributions': {'Previous Marks': 3.6, 'Quiz Average': 3.5, 'Study Hours': 2.4, 'Assignment Average': 2.0, 'Attendance': 1.6, 'Study Frequency': 0.8}}

def get_contributions(student_name):
    """Scale the demo contributions so they add up to the selected student's score."""
    base = SHAP_DATA['base_value']
    values = SHAP_DATA['contributions']
    target = STUDENTS[student_name]['predicted'] - base
    factor = target / sum(values.values())
    return {k: round(v * factor, 1) for k, v in values.items()}
WHAT_IF_DATA = {'current': {'score': 62, 'study_hours': 2, 'quiz': 55, 'attendance': 70, 'assignment': 60}, 'defaults': {'study_hours': 4, 'quiz': 70, 'attendance': 80, 'assignment': 70}, 'weights': {'study_hours': 1.5, 'quiz': 0.3, 'attendance': 0.2, 'assignment': 0.2}}

def mock_scenario(study_hours, quiz, attendance, assignment):
    """FUTURE BACKEND: POST /api/what-if"""
    cur, w = (WHAT_IF_DATA['current'], WHAT_IF_DATA['weights'])
    gain = w['study_hours'] * (study_hours - cur['study_hours']) + w['quiz'] * (quiz - cur['quiz']) + w['attendance'] * (attendance - cur['attendance']) + w['assignment'] * (assignment - cur['assignment'])
    return int(round(min(100, max(0, cur['score'] + gain))))

def mock_predict(prev, quiz, assignment, attendance, hours, frequency):
    """FUTURE BACKEND: POST /api/predict"""
    score = 0.3 * prev + 0.3 * quiz + 0.15 * assignment + 0.1 * attendance + 0.5 * hours + 0.8 * frequency
    score = round(min(100.0, max(0.0, score)), 1)
    pass_prob = int(min(99, max(1, round(100 / (1 + math.exp(-(score - 50) / 8))))))
    risk = 'Low' if score >= 70 else 'Medium' if score >= 55 else 'High'
    perf = 'Excellent' if score >= 85 else 'Good' if score >= 70 else 'Average' if score >= 55 else 'Needs Improvement'
    return dict(score=score, performance=perf, risk=risk, pass_prob=pass_prob)
