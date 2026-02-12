import streamlit as st

# MUST be first - before ANY other Streamlit commands
st.set_page_config(
    page_title="Recruitment Intelligence System",
    page_icon="🎯",
    layout="wide"
)

# All other imports AFTER set_page_config
import tempfile
import os
from models.job import Job
from orchestrator import RecruitmentOrchestrator

# Page title
st.title("Multi-Agent Recruitment Intelligence System")
st.markdown("---")

@st.cache_resource
def load_orchestrator():
    return RecruitmentOrchestrator()

if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = load_orchestrator()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.session_state.pdf_path = tmp_file.name
        st.success(f"Loaded: {uploaded_file.name}")

with col2:
    st.subheader("Job Description")
    
    job_title = st.text_input("Job Title", "Software Engineer")
    min_experience = st.number_input("Minimum Experience (years)", 0, 15, 3)
    
    required_skills_input = st.text_area(
        "Required Skills (one per line)",
        "Python\nSQL\nAWS"
    )
    preferred_skills_input = st.text_area(
        "Preferred Skills (one per line)",
        "Docker\nKubernetes\nReact"
    )
    
    required_skills = [s.strip() for s in required_skills_input.split('\n') if s.strip()]
    preferred_skills = [s.strip() for s in preferred_skills_input.split('\n') if s.strip()]
    
    job = Job(job_title, required_skills, preferred_skills, min_experience)

if st.button("Run Recruitment Pipeline", use_container_width=True):
    if 'pdf_path' not in st.session_state:
        st.error("Please upload a resume PDF")
        st.stop()
    
    with st.spinner("Running multi-agent analysis..."):
        result = st.session_state.orchestrator.run(st.session_state.pdf_path, job)
    
    st.markdown("---")
    
    if result.get("error"):
        st.error(f"Pipeline Error: {result['error']}")
        st.stop()
    
    col_a, col_b, col_c = st.columns(3)
    
    decision_data = result.get("decision", {})
    decision = decision_data.get("decision", "UNKNOWN")
    
    if decision == "INTERVIEW":
        st.success(f"### Decision: {decision}")
    elif decision == "REVIEW":
        st.warning(f"### Decision: {decision}")
    elif decision == "DEVELOP":
        st.info(f"### Decision: {decision}")
    else:
        st.error(f"### Decision: {decision}")
    
    col_a.metric("Decision", decision)
    
    candidate = result.get("candidate")
    if candidate:
        col_b.metric("Candidate", candidate.name if candidate.name else "Unknown")
        col_c.metric("Experience", f"{candidate.experience_years} years")
    
    match_result = result.get("match_result", {})
    if match_result:
        st.metric("Overall Match Score", f"{match_result.get('final_score', 0):.1%}")
        
        tab1, tab2, tab3 = st.tabs(["Match Analysis", "Skills", "Learning Path"])
        
        with tab1:
            st.subheader("Score Breakdown")
            score_col1, score_col2, score_col3 = st.columns(3)
            score_col1.metric("Skills Match", f"{match_result.get('skill_score', 0):.1%}")
            score_col2.metric("Experience Match", f"{match_result.get('experience_score', 0):.1%}")
            score_col3.metric("Semantic Match", f"{match_result.get('semantic_score', 0):.1%}")
            st.write("---")
            st.write(decision_data.get("reason", "No reason provided"))
        
        with tab2:
            col_skills1, col_skills2 = st.columns(2)
            with col_skills1:
                st.subheader("Skills Found")
                if candidate and candidate.skills:
                    st.write(", ".join(candidate.skills))
                else:
                    st.write("No skills detected")
            with col_skills2:
                st.subheader("Missing Required Skills")
                missing = match_result.get("missing_skills", [])
                if missing:
                    st.write(", ".join(missing))
                else:
                    st.write("All required skills present!")
        
        with tab3:
            recommendations = result.get("recommendations", [])
            if recommendations:
                st.subheader("Personalized Learning Recommendations")
                for i, course in enumerate(recommendations, 1):
                    st.markdown(f"""
                    **{i}. {course['title']}**  
                    - Skill: {course['skill']}  
                    - Platform: {course['platform']}  
                    - Duration: {course['hours']} hours  
                    - Level: {course['level']}
                    """)
            else:
                st.info("No learning recommendations needed at this time.")
    
    if os.path.exists(st.session_state.pdf_path):
        os.unlink(st.session_state.pdf_path)