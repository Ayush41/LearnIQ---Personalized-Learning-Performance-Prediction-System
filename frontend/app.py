import streamlit as st
import pandas as pd
import numpy as np
import time

# Page Configuration
st.set_page_config(page_title="LearnIQ Dashboard", page_icon="🧠", layout="wide")

# Sidebar Navigation
st.sidebar.title("LearnIQ Navigation")
page = st.sidebar.radio("Go to", ["Student Dashboard", "What-If Simulation", "Knowledge Gap Analysis"])

st.sidebar.markdown("---")
st.sidebar.info("Developed by Team Aura")

# ----------------------------------------
# PAGE 1: Student Dashboard
# ----------------------------------------
if page == "Student Dashboard":
    st.title("🧠 LearnIQ: Personalized Learning Dashboard")
    st.markdown("Welcome back! Here is an overview of your current academic trajectory.")
    
    # Mock Data Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Attendance", "78%", "-2%")
    col2.metric("Weekly Study Hours", "12 hrs", "+1.5 hrs")
    col3.metric("Quiz Average", "68%", "+5%")
    col4.metric("Predicted Pass Prob.", "82%", "+4%")
    
    st.markdown("---")
    st.subheader("Recent Performance Trends")
    
    # Mock line chart for quiz scores
    chart_data = pd.DataFrame(
        np.random.randn(10, 2) * 10 + [65, 70],
        columns=["Data Structures", "Operating Systems"]
    )
    st.line_chart(chart_data)

# ----------------------------------------
# PAGE 2: What-If Simulation
# ----------------------------------------
elif page == "What-If Simulation":
    st.title("📊 What-If Scenario Analysis")
    st.markdown("Adjust your academic habits below to see how they impact your predicted performance.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Adjust Parameters")
        attendance = st.slider("Target Attendance (%)", min_value=0, max_value=100, value=75)
        study_hours = st.slider("Weekly Self-Study Hours", min_value=0, max_value=40, value=10)
        quiz_avg = st.slider("Target Quiz Average (%)", min_value=0, max_value=100, value=65)
        study_freq = st.selectbox("Study Frequency", ["Daily", "3-4 Days/Week", "Only Before Exams"])
        
        run_sim = st.button("Run Simulation", type="primary")
        
    with col2:
        st.subheader("Simulation Results")
        if run_sim:
            with st.spinner("Running ensemble models and generating insights..."):
                time.sleep(1.5) # Simulate API latency
                
                # Simple mock logic for demonstration
                base_prob = 50
                prob = base_prob + (attendance * 0.2) + (study_hours * 0.8) + (quiz_avg * 0.15)
                prob = min(max(int(prob), 5), 99) # Clamp between 5 and 99
                
                if prob >= 75:
                    risk_category = "Low Risk"
                    st.success(f"**Predicted Pass Probability:** {prob}%")
                elif prob >= 50:
                    risk_category = "Moderate Risk"
                    st.warning(f"**Predicted Pass Probability:** {prob}%")
                else:
                    risk_category = "High Risk"
                    st.error(f"**Predicted Pass Probability:** {prob}%")
                
                st.metric("Performance Category", risk_category)
                
                # Mock LLM Interpretation
                st.markdown("### AI Advisor Insight")
                st.info(f"Based on your simulated inputs, your probability of passing is {prob}%. The model identifies your target study hours ({study_hours} hrs/week) as the strongest positive driver for this score. To move into a safer tier, focus on increasing your quiz average above {quiz_avg}%.")
        else:
            st.info("Adjust the sliders and click 'Run Simulation' to see your projected outcomes and AI insights.")

# ----------------------------------------
# PAGE 3: Knowledge Gap Analysis
# ----------------------------------------
elif page == "Knowledge Gap Analysis":
    st.title("🎯 Knowledge Gap & Recommendations")
    st.markdown("Identify specific weak points and get AI-driven learning paths.")
    
    subject = st.selectbox("Select Subject Module", ["Data Structures", "Database Management Systems", "Machine Learning"])
    
    st.subheader(f"Topic-Level Analysis: {subject}")
    
    # Mock horizontal bar chart for topic accuracy
    topic_data = pd.DataFrame({
        "Accuracy": [85, 45, 92, 30],
        "Topic": ["Arrays", "Linked Lists", "Trees", "Graphs"]
    }).set_index("Topic")
    
    st.bar_chart(topic_data, use_container_width=True)
    
    st.markdown("### 💡 Recommended Next Steps")
    st.warning("**High Priority:** Your accuracy in **Graphs (30%)** is critically low. This is a prerequisite for advanced pathfinding algorithms.")
    st.markdown("""
    1. **Review Theory:** Re-watch Lecture 4 (Graph Traversal BFS/DFS).
    2. **Practice:** Complete Assignment 3 (Basic Graph Implementations).
    3. **Re-evaluate:** Attempt the Graph Knowledge Check quiz again.
    """)