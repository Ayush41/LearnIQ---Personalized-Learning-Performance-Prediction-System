"""Reusable Plotly charts with one consistent look."""
import plotly.graph_objects as go
PRIMARY, MUTED, SUCCESS, DANGER = ('#4f46e5', '#94a3b8', '#16a34a', '#dc2626')

def _style(fig, height):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family='Plus Jakarta Sans, sans-serif', color='#475569', size=12), legend=dict(orientation='h', y=-0.2))
    fig.update_xaxes(gridcolor='#eef1f6', zeroline=False)
    fig.update_yaxes(gridcolor='#eef1f6', zeroline=False)
    return fig

def performance_chart(labels, scores):
    fig = go.Figure(go.Scatter(x=labels, y=scores, mode='lines+markers', line=dict(color=PRIMARY, width=3, shape='spline'), marker=dict(size=8, color='#fff', line=dict(color=PRIMARY, width=2)), fill='tozeroy', fillcolor='rgba(99,102,241,0.08)', hovertemplate='%{x}: %{y}%<extra></extra>'))
    fig.update_yaxes(range=[max(0, min(scores) - 15), 100], title='Score (%)')
    return _style(fig, 320)

def cluster_chart(points, clusters, student_name, student_x, student_y):
    fig = go.Figure()
    for i, c in enumerate(clusters):
        d = points[points['Cluster'] == i]
        fig.add_trace(go.Scatter(x=d['Study Hours'], y=d['Quiz Average'], mode='markers', name=c['name'], marker=dict(size=9, color=c['color'], opacity=0.65)))
    fig.add_trace(go.Scatter(x=[student_x], y=[student_y], mode='markers+text', name='Selected student', text=[student_name], textposition='top center', marker=dict(size=17, symbol='star', color='#0f172a', line=dict(color='#fff', width=1.5))))
    fig.update_xaxes(title='Study Hours (per week)')
    fig.update_yaxes(title='Quiz Average (%)')
    return _style(fig, 430)

def feature_importance_chart(contributions):
    items = sorted(contributions.items(), key=lambda kv: abs(kv[1]))
    names, vals = ([k for k, _ in items], [v for _, v in items])
    fig = go.Figure(go.Bar(x=vals, y=names, orientation='h', marker_color=[SUCCESS if v >= 0 else DANGER for v in vals], text=[f'{v:+.1f}' for v in vals], textposition='outside', cliponaxis=False, hovertemplate='%{y}: %{x:+.1f} marks<extra></extra>'))
    fig.update_xaxes(title='Contribution to predicted score (marks)')
    return _style(fig, 330)

def model_accuracy_chart(df):
    colors = [PRIMARY if a == df['Accuracy'].max() else MUTED for a in df['Accuracy']]
    fig = go.Figure(go.Bar(x=df['Model'], y=df['Accuracy'], marker_color=colors, text=[f'{a:.2f}' for a in df['Accuracy']], textposition='outside', cliponaxis=False))
    fig.update_yaxes(range=[0.5, 1.0], title='Accuracy')
    return _style(fig, 280)
