import streamlit as st
import json
import streamlit.components.v1 as components

from models import ResumePayload, PersonalInfo, WorkExperience, Education, SkillCategory, ProjectItem
from ai_polisher import STARBulletPolisher
from pdf_renderer import HTMLPDFResumeRenderer

# Streamlit Page Setup
st.set_page_config(
    page_title="Resume-Maker | ResumeForge-API",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 14px;
        color: #94A3B8;
        margin-bottom: 20px;
    }
    .card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .badge {
        background: #6366F1;
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .badge-green {
        background: #10B981;
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Sample Preset Data
DEFAULT_SAMPLE_PAYLOAD = {
    "target_job_title": "Senior Backend & Infrastructure Engineer",
    "target_job_description": "Seeking Senior Engineer proficient in Python, FastAPI, AsyncIO, Pydantic, Microservices, Docker, AWS, and RAG pipelines.",
    "personal_info": {
        "full_name": "Alex Mercer",
        "email": "alex.mercer@example.com",
        "phone": "+1 (555) 345-6789",
        "location": "San Francisco, CA",
        "linkedin": "linkedin.com/in/alexmercer-dev",
        "github": "github.com/alexmercer",
        "portfolio": "alexmercer.dev"
    },
    "summary": "Results-driven Senior Software Engineer with 5+ years of experience designing high-throughput distributed microservices, async FastAPI pipelines, and cloud backend engines.",
    "experience": [
        {
            "company": "Apex Cloud Systems",
            "position": "Senior Backend Engineer",
            "location": "San Francisco, CA",
            "start_date": "Jan 2022",
            "end_date": "Present",
            "bullets": [
                "Architected async Python microservices using FastAPI and Pydantic v2, reducing p99 response latency by 42% across 10M daily requests.",
                "Engineered automated Jinja2 Jinja rendering engine for document compilation, scaling throughput to 1,500 PDF requests/min.",
                "Optimized Docker container build pipelines, cutting deployment footprint by 65% and reducing AWS ECS cold-start times."
            ]
        },
        {
            "company": "DataPulse AI",
            "position": "Software Engineer",
            "location": "Austin, TX",
            "start_date": "Jun 2019",
            "end_date": "Dec 2021",
            "bullets": [
                "Built high-performance RAG context retrieval pipeline using Python and vector indexing, improving semantic search relevance by 38%.",
                "Spearheaded database query optimization across PostgreSQL relational tables, lowering average query execution time from 450ms to 85ms."
            ]
        }
    ],
    "education": [
        {
            "institution": "University of California, Berkeley",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science & Engineering",
            "graduation_year": "2019",
            "gpa": "3.88 / 4.0"
        }
    ],
    "skills": [
        {
            "category_name": "Languages & Frameworks",
            "skills": ["Python 3.11", "FastAPI", "AsyncIO", "Pydantic v2", "Jinja2", "SQLAlchemy"]
        },
        {
            "category_name": "Infrastructure & Cloud",
            "skills": ["Docker", "Kubernetes", "AWS (Lambda, ECS)", "PostgreSQL", "Redis", "CI/CD"]
        }
    ],
    "projects": [
        {
            "title": "ResumeForge-API",
            "description": "Automated resume compilation microservice built with FastAPI, Pydantic schema validation, and GenAI bullet polishing.",
            "tech_stack": ["Python", "FastAPI", "Pydantic", "Jinja2", "Docker"],
            "link": "github.com/alexmercer/ResumeForge-API"
        }
    ]
}

# Initialize Session State
if "payload_data" not in st.session_state:
    st.session_state.payload_data = DEFAULT_SAMPLE_PAYLOAD

polisher = STARBulletPolisher()
renderer = HTMLPDFResumeRenderer()

# Header
st.markdown('<div class="main-header">📄 Resume-Maker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">ResumeForge-API — Automated Resume & Portfolio Generator with Pydantic & GenAI Polishing</div>', unsafe_allow_html=True)

# Top Navigation Tabs
tab_builder, tab_polisher, tab_preview, tab_schema, tab_arch = st.tabs([
    "📝 Resume Builder",
    "🤖 STAR Bullet Polisher",
    "📄 Live ATS Preview & Download",
    "⚡ FastAPI & Pydantic Tester",
    "🏗️ Architecture & Interview Guide"
])

# ==========================================
# TAB 1: RESUME BUILDER FORM
# ==========================================
with tab_builder:
    col_preset, col_info = st.columns([1, 3])
    with col_preset:
        if st.button("🔄 Reset to High-Impact Sample Data", type="secondary"):
            st.session_state.payload_data = DEFAULT_SAMPLE_PAYLOAD
            st.rerun()

    st.markdown("##### 👤 Personal & Career Profile")
    p_data = st.session_state.payload_data["personal_info"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        full_name = st.text_input("Full Name", value=p_data["full_name"])
        email = st.text_input("Email", value=p_data["email"])
    with col2:
        phone = st.text_input("Phone", value=p_data["phone"])
        location = st.text_input("Location", value=p_data["location"])
    with col3:
        linkedin = st.text_input("LinkedIn", value=p_data.get("linkedin", ""))
        github = st.text_input("GitHub", value=p_data.get("github", ""))

    summary = st.text_area("Professional Summary", value=st.session_state.payload_data["summary"], height=80)
    target_job = st.text_input("Target Job Title", value=st.session_state.payload_data["target_job_title"])
    target_desc = st.text_area("Target Job Description (for keyword alignment)", value=st.session_state.payload_data["target_job_description"], height=80)

    st.markdown("##### 💼 Work Experience (Bullet Points)")
    for idx, exp in enumerate(st.session_state.payload_data["experience"]):
        with st.expander(f"Experience #{idx+1}: {exp['position']} at {exp['company']}", expanded=(idx == 0)):
            exp["company"] = st.text_input(f"Company #{idx+1}", value=exp["company"], key=f"comp_{idx}")
            exp["position"] = st.text_input(f"Position #{idx+1}", value=exp["position"], key=f"pos_{idx}")
            exp["start_date"] = st.text_input(f"Start Date #{idx+1}", value=exp["start_date"], key=f"start_{idx}")
            exp["end_date"] = st.text_input(f"End Date #{idx+1}", value=exp["end_date"], key=f"end_{idx}")
            
            bullets_str = "\n".join(exp["bullets"])
            new_bullets = st.text_area(f"Bullet Points (One per line) #{idx+1}", value=bullets_str, key=f"bullets_{idx}", height=100)
            exp["bullets"] = [b.strip() for b in new_bullets.split("\n") if b.strip()]

    # Sync back to session state
    st.session_state.payload_data["personal_info"]["full_name"] = full_name
    st.session_state.payload_data["personal_info"]["email"] = email
    st.session_state.payload_data["personal_info"]["phone"] = phone
    st.session_state.payload_data["personal_info"]["location"] = location
    st.session_state.payload_data["personal_info"]["linkedin"] = linkedin
    st.session_state.payload_data["personal_info"]["github"] = github
    st.session_state.payload_data["summary"] = summary
    st.session_state.payload_data["target_job_title"] = target_job
    st.session_state.payload_data["target_job_description"] = target_desc

# ==========================================
# TAB 2: STAR BULLET POLISHER
# ==========================================
with tab_polisher:
    st.markdown("##### 🤖 GenAI STAR Bullet Point Optimizer")
    st.markdown("Rewrite raw achievement descriptions into STAR (Situation, Task, Action, Result) metric-driven bullet points.")

    raw_bullet_input = st.text_area(
        "Raw Achievement Description:",
        value="built Python backend microservice and made database queries faster",
        height=70
    )
    
    if st.button("✨ Optimize Bullet with STAR & Metrics", type="primary"):
        polished_result = polisher.polish_bullet(
            raw_bullet_input, 
            st.session_state.payload_data["target_job_description"]
        )
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("""
            <div class="card">
                <span class="badge">Original Input</span>
                <p style="color: #CBD5E1; font-size: 14px;">""" + polished_result["original"] + """</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_res2:
            st.markdown("""
            <div class="card">
                <span class="badge-green">STAR Optimized Output</span>
                <p style="color: #F8FAFC; font-weight: 600; font-size: 14px;">""" + polished_result["polished"] + """</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("###### 🔍 STAR Methodology & Keyword Alignment Breakdown")
        st.json(polished_result["star_breakdown"])

# ==========================================
# TAB 3: LIVE ATS PREVIEW & DOWNLOAD
# ==========================================
with tab_preview:
    st.markdown("##### 📄 ATS-Friendly Resume HTML Render")
    
    # Try validating payload via Pydantic
    try:
        validated_payload = ResumePayload(**st.session_state.payload_data)
        html_code = renderer.render_html(validated_payload.model_dump())
        
        st.markdown('<span class="badge-green">Pydantic v2 Schema Validated</span>', unsafe_allow_html=True)
        
        col_down1, col_down2 = st.columns([1, 4])
        with col_down1:
            st.download_button(
                label="📥 Download ATS Resume HTML",
                data=html_code,
                file_name=f"{validated_payload.personal_info.full_name.replace(' ', '_')}_Resume.html",
                mime="text/html",
                type="primary"
            )
            
        components.html(html_code, height=750, scrolling=True)
        
    except Exception as e:
        st.error(f"Schema Validation Error: {str(e)}")

# ==========================================
# TAB 4: FASTAPI & PYDANTIC TESTER
# ==========================================
with tab_schema:
    st.markdown("##### ⚡ Pydantic v2 Schema Inspector & REST Endpoint Test Bench")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("###### JSON Payload Payload Inspection")
        st.json(st.session_state.payload_data)
        
    with col_t2:
        st.markdown("###### Endpoint Simulator (`POST /api/v1/resume/generate`)")
        if st.button("⚡ Test Async Compilation Endpoint"):
            try:
                validated = ResumePayload(**st.session_state.payload_data)
                st.success("✅ FastAPI Validation Pass: HTTP 200 OK")
                st.json({
                    "status_code": 200,
                    "response_time_ms": 14.2,
                    "candidate": validated.personal_info.full_name,
                    "target_role": validated.target_job_title,
                    "schema_version": "Pydantic v2.10"
                })
            except Exception as e:
                st.error(f"❌ HTTP 422 Unprocessable Entity: {str(e)}")

# ==========================================
# TAB 5: ARCHITECTURE & INTERVIEW GUIDE
# ==========================================
with tab_arch:
    st.markdown("##### 🏗️ System Architecture & Interview Cheat Sheet")
    
    st.markdown("""
    ```
    +-----------------------------------------------------------------------------------+
    |                                RESUMEFORGE-API                                    |
    +-----------------------------------------------------------------------------------+
                                            |
           +--------------------------------+--------------------------------+
           |                                                                 |
           v                                                                 v
    +--------------------------------+                             +--------------------+
    |   PYDANTIC V2 SCHEMA LAYER     |                             |  GENAI STAR ENGINE |
    | - Strict type validation       |                             | - Keyword extraction|
    | - PersonalInfo & Experience    |                             | - STAR methodology |
    | - Non-blocking data parsing    |                             | - Metric injection |
    +--------------------------------+                             +--------------------+
                   |                                                         |
                   v                                                         v
    +-----------------------------------------------------------------------------------+
    |                         FASTAPI ASYNC COMPILATION PIPELINE                        |
    | - Jinja2 HTML Template Injection                                                  |
    | - Non-blocking async endpoints (/api/v1/resume/generate)                          |
    | - Headless ATS PDF compilation stream                                              |
    +-----------------------------------------------------------------------------------+
    ```
    """)
    
    st.markdown("""
    ### 🗣️ How to Talk About It in an Interview:

    #### **When asked about backend architecture:**
    > *"I structured ResumeForge-API using a clean separation of concerns: input data is strictly validated via Pydantic models, processed asynchronously through FastAPI, and rendered via a headless Jinja2-to-PDF pipeline. This ensures zero blocking on I/O-bound operations and guarantees schema integrity."*

    #### **When asked about scalability:**
    > *"Because the core engine is containerized with Docker and exposes an async FastAPI interface, it can easily scale horizontally behind an AWS ALB or be deployed as a serverless AWS Lambda function triggered by event queues."*
    """)
