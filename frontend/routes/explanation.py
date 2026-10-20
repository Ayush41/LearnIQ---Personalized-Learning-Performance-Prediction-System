import streamlit as st
import pandas as pd
from data import api_client
from ui import charts
from ui.components import card, render_insight_card, render_lede, render_note, render_section_header

def render():
    try:
        importance = api_client.get('feature-importance')
    except api_client.ApiClientError as error:
        st.error(f'Could not calculate feature importance: {error}')
        return
    render_lede('Review which inputs most affect held-out model performance.')
    with card('permutation-importance'):
        render_section_header('Permutation Importance', f"Model: {importance['model']}")
        rows = importance['importance']
        if rows:
            importance_frame = pd.DataFrame(rows)
            contributions = dict(zip(importance_frame['feature'], importance_frame['importance']))
            st.plotly_chart(charts.feature_importance_chart(contributions), use_container_width=True, config={'displayModeBar': False})
            st.dataframe(importance_frame, hide_index=True, use_container_width=True)
        else:
            st.info('No feature-importance data is available.')
        render_note('Permutation importance measures the change in held-out score after shuffling a feature; it is not a causal explanation.')
