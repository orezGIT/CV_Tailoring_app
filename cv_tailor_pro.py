# cv_tailor_pro.py
"""
Professional CV Tailor - Summary, Skills, Cover Letter & LinkedIn
"""

import streamlit as st
import re
from typing import List, Dict

# ---------- CUSTOM STYLING ----------
st.set_page_config(page_title="CV Tailor Pro", layout="wide")

# Inject custom CSS for professional green styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
    }
    .main .block-container {
        background: white;
        border-radius: 15px;
        padding: 3rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        border-bottom: 3px solid #27ae60;
        padding-bottom: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #27ae60, #219653);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
        background: linear-gradient(135deg, #219653, #1e8449);
    }
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #27ae60;
        box-shadow: 0 0 0 2px rgba(39, 174, 96, 0.2);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #27ae60;
        box-shadow: 0 0 0 2px rgba(39, 174, 96, 0.2);
    }
    .success-box {
        background: linear-gradient(135deg, #27ae60, #219653);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2ecc71;
    }
    .info-box {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #27ae60;
    }
    .tab-container {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #e8f5e8;
    }
    .download-btn {
        background: linear-gradient(135deg, #27ae60, #219653) !important;
    }
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Professional CV Tailor")
st.markdown("### Transform your CV with tailored content for each job application")

# ---------- TEXT EXTRACTION ----------
def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    try:
        if uploaded_file.name.lower().endswith('.pdf'):
            from PyPDF2 import PdfReader
            from io import BytesIO
            reader = PdfReader(BytesIO(uploaded_file.read()))
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        else:
            return uploaded_file.getvalue().decode('utf-8')
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""

# ---------- SMART CONTENT GENERATION ----------
def extract_sections(text: str) -> Dict[str, List[str]]:
    """Extract summary and skills from CV"""
    sections = {'summary': [], 'skills': []}
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        lower_line = line.lower()
        if 'summary' in lower_line:
            current_section = 'summary'
        elif 'skills' in lower_line:
            current_section = 'skills'
        elif current_section and len(sections[current_section]) < 10:
            sections[current_section].append(line)
    
    return sections

def generate_tailored_summary(job_description: str, cv_text: str) -> str:
    """Generate a professional summary tailored to the job and CV content"""
    
    # Extract key technologies from job description
    jd_lower = job_description.lower()
    technologies = []
    
    # Tech stack detection
    tech_keywords = {
        'python': 'Python', 'sql': 'SQL', 'r ': 'R', 'java ': 'Java',
        'machine learning': 'Machine Learning', 'deep learning': 'Deep Learning',
        'nlp': 'NLP', 'computer vision': 'Computer Vision',
        'power bi': 'Power BI', 'tableau': 'Tableau', 'looker': 'Looker',
        'aws': 'AWS', 'azure': 'Azure', 'gcp': 'GCP', 'spark': 'Apache Spark',
        'hadoop': 'Hadoop', 'docker': 'Docker', 'kubernetes': 'Kubernetes'
    }
    
    for keyword, tech_name in tech_keywords.items():
        if keyword in jd_lower:
            technologies.append(tech_name)
    
    # Extract experience level from CV
    cv_lower = cv_text.lower()
    experience_keywords = []
    if any(word in cv_lower for word in ['senior', 'lead', 'manager', 'head of']):
        experience_keywords = ['senior-level', 'leadership', 'strategic']
    elif any(word in cv_lower for word in ['junior', 'entry', 'graduate', 'intern']):
        experience_keywords = ['emerging', 'enthusiastic', 'foundational']
    else:
        experience_keywords = ['experienced', 'proven', 'skilled']
    
    tech_text = ', '.join(technologies[:4]) if technologies else 'data science and analytics'
    exp_text = ' '.join(experience_keywords[:2])
    
    summary = f"""{exp_text.title()} Data Scientist with comprehensive expertise in {tech_text}. Proven ability to transform complex data into actionable insights that drive measurable business outcomes. Skilled in developing and deploying predictive models, creating interactive dashboards, and effectively communicating technical findings to diverse stakeholders. Strong background in data preprocessing, feature engineering, and statistical analysis with a demonstrated track record of delivering innovative solutions in fast-paced environments."""
    
    return summary

def generate_tailored_skills(job_description: str, cv_text: str) -> str:
    """Generate tailored skills section based on job requirements and CV content"""
    
    jd_lower = job_description.lower()
    cv_lower = cv_text.lower()
    skills = []
    
    # Detect what skills are already in CV
    cv_has_python = any(word in cv_lower for word in ['python', 'pandas', 'numpy'])
    cv_has_sql = any(word in cv_lower for word in ['sql', 'database', 'query'])
    cv_has_ml = any(word in cv_lower for word in ['machine learning', 'scikit', 'tensorflow', 'pytorch'])
    
    # Programming & Databases (only include if in CV)
    if cv_has_python and any(word in jd_lower for word in ['python', 'programming']):
        skills.append('Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)')
    if cv_has_sql and any(word in jd_lower for word in ['sql', 'database']):
        skills.append('SQL (Complex queries, database optimization, ETL processes)')
    if 'r' in cv_lower and 'r' in jd_lower:
        skills.append('R (tidyverse, ggplot2, statistical analysis, data visualization)')
    
    # Machine Learning (only include if in CV)
    if cv_has_ml:
        if any(word in jd_lower for word in ['machine learning', 'ml', 'predictive']):
            skills.append('Machine Learning (Regression, Classification, Clustering, Model Evaluation)')
        if any(word in jd_lower for word in ['deep learning', 'neural', 'tensorflow', 'pytorch']):
            skills.append('Deep Learning (Neural Networks, TensorFlow, PyTorch, Keras)')
        if any(word in jd_lower for word in ['nlp', 'natural language']):
            skills.append('Natural Language Processing (Sentiment Analysis, Text Classification, NLTK)')
    
    # Visualization & BI Tools
    if any(word in jd_lower for word in ['power bi', 'tableau', 'dashboard', 'visualization']):
        skills.append('Data Visualization (Power BI, Tableau, Matplotlib, Plotly)')
    
    # Cloud & Big Data
    if any(word in jd_lower for word in ['aws', 'azure', 'gcp', 'cloud']):
        skills.append('Cloud Platforms (AWS/Azure, Databricks, Cloud ML Services)')
    if any(word in jd_lower for word in ['spark', 'big data', 'hadoop']):
        skills.append('Big Data Technologies (Apache Spark, Hadoop, Distributed Computing)')
    
    # Essential data science skills (always include)
    essential_skills = [
        'Statistical Analysis & Hypothesis Testing',
        'Data Wrangling & Feature Engineering', 
        'Model Deployment & MLOps Practices',
        'Cross-functional Collaboration & Stakeholder Management',
        'Data Storytelling & Technical Communication'
    ]
    
    # Combine and limit to 10 skills
    all_skills = skills + essential_skills
    return "\n".join([f"• {skill}" for skill in all_skills[:10]])

def generate_cover_letter(job_description: str, cv_text: str, company: str, job_title: str) -> str:
    """Generate a professional cover letter tailored to the job and CV"""
    
    # Extract key requirements
    jd_lower = job_description.lower()
    
    # Build skills mention based on job requirements
    skills_mentioned = []
    if 'python' in jd_lower: skills_mentioned.append('Python programming')
    if 'sql' in jd_lower: skills_mentioned.append('SQL and database management')
    if 'machine learning' in jd_lower: skills_mentioned.append('machine learning model development')
    if 'power bi' in jd_lower or 'tableau' in jd_lower: skills_mentioned.append('data visualization')
    if 'aws' in jd_lower or 'azure' in jd_lower: skills_mentioned.append('cloud platform experience')
    
    skills_text = ', '.join(skills_mentioned) if skills_mentioned else 'data science and analytics'
    
    cover_letter = f"""
{company.upper()}
Hiring Manager
Data Science Department

Dear Hiring Manager,

I am writing to express my enthusiastic interest in the {job_title} position at {company}. With my comprehensive background in data science and my expertise in {skills_text}, I am confident in my ability to make significant contributions to your team.

{job_description[:120]}...

My qualifications align perfectly with your requirements:

• Technical Expertise: Advanced proficiency in the technical stack required for this role, with hands-on experience in developing and deploying data-driven solutions
• Business Impact: Proven ability to translate complex data into actionable insights that drive strategic decision-making and measurable business outcomes
• Collaboration: Strong communication skills with experience working in cross-functional teams to deliver projects that meet both technical and business requirements

I am particularly excited about the opportunity to contribute to {company}'s data initiatives and am impressed by your organization's commitment to innovation and excellence.

Thank you for considering my application. I have attached my CV for your review and would welcome the opportunity to discuss how my skills and experience can benefit your team.

Sincerely,

[Your Name]
[Your Phone Number]
[Your Email]
[Your LinkedIn Profile]
"""
    return cover_letter.strip()

def generate_linkedin_message(job_title: str, company: str, job_description: str) -> str:
    """Generate a professional LinkedIn connection message"""
    
    # Extract a key aspect from job description for personalization
    key_aspect = ""
    jd_lower = job_description.lower()
    if any(word in jd_lower for word in ['machine learning', 'ml']):
        key_aspect = "machine learning initiatives"
    elif any(word in jd_lower for word in ['data analysis', 'analytics']):
        key_aspect = "data analytics projects"
    elif any(word in jd_lower for word in ['data engineering', 'etl']):
        key_aspect = "data engineering work"
    else:
        key_aspect = "data science work"
    
    message = f"""
Hi [Hiring Manager Name],

I hope this message finds you well. I came across the {job_title} position at {company} and was particularly impressed by your team's focus on {key_aspect}.

With my background in data science and experience in [mention your most relevant skill from the job description], I believe I could bring valuable expertise to your team. I've been following {company}'s work in the industry and am excited about the opportunity to contribute to your data-driven initiatives.

Would you be open to a brief 15-minute chat next week to discuss how my experience aligns with your team's needs?

Looking forward to connecting.

Best regards,

[Your Name]
Data Scientist
[Your Phone Number] | [Your Email]
[Your LinkedIn Profile URL]
"""
    return message.strip()

# ---------- MAIN APPLICATION ----------
st.markdown('<div class="info-box">📝 Upload your CV and job details to get tailored content</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Your CV")
    uploaded_file = st.file_uploader("Choose PDF or text file", type=["pdf", "txt"], key="cv_upload")

with col2:
    st.header("2. Job Details")
    job_title = st.text_input("Job Title*", placeholder="e.g., Data Scientist, ML Engineer")
    company_name = st.text_input("Company Name*", placeholder="e.g., Google, Amazon, NHS")
    job_desc = st.text_area("Job Description*", height=150, placeholder="Paste the full job description here...")

if uploaded_file and job_desc and company_name and job_title:
    
    cv_text = extract_text_from_file(uploaded_file)
    
    if st.button("🚀 Generate Tailored Content", use_container_width=True):
        with st.spinner("Creating your professional application package..."):
            
            # Generate all tailored content
            new_summary = generate_tailored_summary(job_desc, cv_text)
            new_skills = generate_tailored_skills(job_desc, cv_text)
            cover_letter = generate_cover_letter(job_desc, cv_text, company_name, job_title)
            linkedin_msg = generate_linkedin_message(job_title, company_name, job_desc)
            
            st.markdown('<div class="success-box">✅ Your tailored content is ready! Copy and use these sections in your application.</div>', unsafe_allow_html=True)
            
            # Display in tabs for better organization
            tab1, tab2, tab3, tab4 = st.tabs(["🎯 Professional Summary", "🛠️ Skills Section", "✉️ Cover Letter", "💼 LinkedIn Message"])
            
            with tab1:
                st.markdown('<div class="tab-container">', unsafe_allow_html=True)
                st.subheader("Tailored Professional Summary")
                st.text_area("Copy this summary to your CV:", new_summary, height=200, key="summary_area")
                st.download_button("📄 Download Summary", new_summary, "professional_summary.txt", "text/plain", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with tab2:
                st.markdown('<div class="tab-container">', unsafe_allow_html=True)
                st.subheader("Tailored Skills Section")
                st.text_area("Copy these skills to your CV:", new_skills, height=200, key="skills_area")
                st.download_button("📄 Download Skills", new_skills, "tailored_skills.txt", "text/plain", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with tab3:
                st.markdown('<div class="tab-container">', unsafe_allow_html=True)
                st.subheader("Professional Cover Letter")
                st.text_area("Use this cover letter:", cover_letter, height=400, key="cover_area")
                st.download_button("📄 Download Cover Letter", cover_letter, "cover_letter.txt", "text/plain", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with tab4:
                st.markdown('<div class="tab-container">', unsafe_allow_html=True)
                st.subheader("LinkedIn Connection Message")
                st.text_area("Use this LinkedIn message:", linkedin_msg, height=300, key="linkedin_area")
                st.download_button("📄 Download LinkedIn Message", linkedin_msg, "linkedin_message.txt", "text/plain", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show original content for comparison
            with st.expander("🔍 View Original CV Content (for reference)"):
                original_sections = extract_sections(cv_text)
                if original_sections['summary']:
                    st.write("**Original Summary:**")
                    st.text(" ".join(original_sections['summary'][:3]))
                if original_sections['skills']:
                    st.write("**Original Skills (sample):**")
                    st.text("\n".join(original_sections['skills'][:5]))

else:
    st.info("👆 Please upload your CV and fill in all job details to get started.")

# Footer
st.markdown("---")
st.markdown("💡 **Pro Tip:** Always customize the generated content with your specific achievements and experiences!")