import tempfile
import re
import json
import joblib
import pickle
import pandas as pd
import streamlit as st
from pathlib import Path
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
import docx2txt
import sys
import os

# Add parent directory to path to import db_config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from db_config import get_db_connection


st.set_page_config(page_title="Upload Resumé", layout="wide")


def clean_text(text: str) -> str:
    text = text.lower()
    text = text.replace('"', '').replace("'s", '')
    text = text.replace('\t', ' ').replace('\n', ' ')
    text = re.sub(r'[;?.:!,]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in text.split() if word not in stop_words]
    return ' '.join(tokens)


def extract_text(uploaded_file, temp_path: Path) -> str:
    content = ''
    uploaded_bytes = uploaded_file.getvalue()
    temp_path.write_bytes(uploaded_bytes)

    if uploaded_file.type == 'text/plain':
        content = uploaded_bytes.decode('utf-8', errors='ignore')
    elif uploaded_file.type == 'application/pdf':
        with open(temp_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                content += page.extract_text() or ''
    elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        content = docx2txt.process(str(temp_path))

    return content


def fetch_hr_position(cursor):
    cursor.execute("SELECT POSITION, job_description FROM HR")
    row = cursor.fetchone()
    return (row[0], row[1]) if row else ('', '')


def fetch_skills(cursor, position):
    try:
        cursor.execute("SELECT skill FROM skills WHERE LOWER(position) = %s", (position.lower(),))
        row = cursor.fetchone()
        return row[0] if row else ''
    except mysql.connector.errors.ProgrammingError:
        # If skills table doesn't exist or has wrong schema, return default skills
        default_skills = {
            'python developer': 'python, django, flask, fastapi, requests, pandas, numpy, scikit-learn',
            'java developer': 'java, spring, spring boot, maven, gradle, junit, hibernate',
            'data science': 'python, r, sql, machine learning, deep learning, tensorflow, pytorch, statistics',
            'devops engineer': 'docker, kubernetes, jenkins, aws, gcp, azure, terraform, ci/cd',
            'web designing': 'html, css, javascript, react, vue, figma, ui/ux, responsive design'
        }
        return default_skills.get(position.lower(), 'python, sql, communication skills')


def load_categories():
    categories_file = Path(__file__).parent.parent / 'categories.json'
    if not categories_file.exists():
        categories_file = Path(__file__).parent / 'categories.json'

    if not categories_file.exists():
        st.error("❌ categories.json not found. Please place categories.json in the project root or pages directory.")
        st.stop()

    with open(categories_file, 'r') as f:
        return json.load(f)


def calculate_match_score(resume_text, job_description, vectorizer):
    """Calculate cosine similarity between resume and job description"""
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Vectorize both texts
    resume_vector = vectorizer.transform([resume_text])
    job_vector = vectorizer.transform([job_description])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(resume_vector, job_vector)[0][0]
    return similarity * 100  # Convert to percentage


def identify_missing_skills(resume_text, job_description):
    """Identify keywords from job description that are missing in resume"""
    # Simple keyword extraction (can be improved with NLP)
    job_words = set(clean_text(job_description).split())
    resume_words = set(clean_text(resume_text).split())
    
    # Remove common stop words and short words
    stop_words = set(stopwords.words('english'))
    job_words = {word for word in job_words if len(word) > 3 and word not in stop_words}
    resume_words = {word for word in resume_words if len(word) > 3 and word not in stop_words}
    
    missing = job_words - resume_words
    return list(missing)[:10]  # Return top 10 missing skills


# Initialize database connection
try:
    mydb = get_db_connection()
    cur = mydb.cursor()
    position, job_description = fetch_hr_position(cur)
    skill_text = fetch_skills(cur, position) if position else ''
    cur.close()
    mydb.close()
except Exception as e:
    st.error(f"❌ Database connection error: {str(e)}")
    st.stop()

# Header section
st.title("📄 Resumé Screening Application")
st.markdown("---")

if not position:
    st.warning("⚠️ No HR position is set yet. Please contact the HR administrator to configure a job position first.")
    st.stop()

# Display job requirement details
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader(f"🎯 Position: {position.upper()}")
    if job_description:
        st.markdown("**📄 Job Description:**")
        st.info(job_description)
with col2:
    st.info(f"📌 **File Formats Accepted**\n- PDF\n- DOCX\n- TXT")

st.markdown("---")

# Upload form
st.subheader("📝 Candidate Information & Resume Upload")

with st.form("Registration Form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input(
            label='📧 Email Address',
            placeholder='your.email@example.com',
            help='A valid email address for communication'
        )
        location = st.text_input(
            label='📍 Location',
            placeholder='City, Country',
            help='Your current location or preferred work location'
        )
    
    with col2:
        fullName = st.text_input(
            label='👤 Full Name',
            placeholder='John Doe',
            help='Your full name as it appears in the resume'
        )
        mobile = st.text_input(
            label='📞 Mobile Number',
            placeholder='+1 234 567 8900',
            help='Contact number for follow-up'
        )
    
    st.markdown("**Upload your Resume:**")
    uploaded_file = st.file_uploader(
        label='Resume File',
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=False,
        help='Select a resume file in PDF, DOCX, or TXT format'
    )
    
    submitted = st.form_submit_button('🚀 Submit Resume', use_container_width=True)

# Process submission
if submitted:
    email = email.strip()
    fullName = fullName.strip()
    mobile = mobile.strip()
    location = location.strip()
    
    # Validation
    if not email:
        st.error("❌ Email address is required.")
    elif not fullName:
        st.error("❌ Full name is required.")
    elif not mobile:
        st.error("❌ Mobile number is required.")
    elif not location:
        st.error("❌ Location is required.")
    elif uploaded_file is None:
        st.error("❌ Please upload a resume file.")
    else:
        # Process resume
        with st.spinner("⏳ Processing your resume..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    temp_path = Path(tmp_file.name)
                    content = extract_text(uploaded_file, temp_path)

                if not content.strip():
                    st.error("❌ Unable to read the uploaded resume. Please try another file format.")
                else:
                    # Clean resume text
                    cleaned_resume = clean_text(content)
                    
                    # Load TF-IDF vectorizer
                    with open('cv.pickle', 'rb') as f:
                        vectorizer = pickle.load(f)
                    
                    # Calculate match score against job description
                    match_percentage = calculate_match_score(cleaned_resume, clean_text(job_description), vectorizer)
                    
                    # Identify missing skills
                    missing_skills = identify_missing_skills(content, job_description)
                    missing_skills_text = ', '.join(missing_skills) if missing_skills else 'None identified'
                    
                    # Load model and predict category (keeping for compatibility)
                    model = joblib.load('RF.joblib')
                    X = vectorizer.transform([cleaned_resume])
                    pred = model.predict(X)
                    
                    dict_category = load_categories()
                    predicted_category = dict_category.get(str(pred[0]), 'UNKNOWN')

                    # Display results
                    st.markdown("---")
                    st.subheader("📊 Screening Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Job Match Score", value=f"{match_percentage:.1f}%")
                    with col2:
                        st.metric(label="Predicted Category", value=predicted_category)
                    with col3:
                        match_status = "✅ HIGH MATCH" if match_percentage >= 70 else "⚠️ MODERATE MATCH" if match_percentage >= 50 else "❌ LOW MATCH"
                        st.metric(label="Match Status", value=match_status)
                    
                    # Show missing skills
                    if missing_skills:
                        st.warning(f"💡 **Skills/Keywords to improve:** {missing_skills_text}")
                        st.info("Consider adding these skills to your resume to improve your match score.")
                    else:
                        st.success("✅ Your resume covers all key requirements from the job description!")

                    # Save to database if match score is good enough
                    if match_percentage >= 50:  # Threshold for shortlisting
                        try:
                            mydb = get_db_connection()
                            cur = mydb.cursor()
                            
                            # Insert into employees table
                            query = """INSERT INTO employees (Name, Email, Resume, score, location, category, match_percentage, missing_skills, position_applied_for, mobile_number) 
                                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                            values = (fullName, email, content, match_percentage, location, predicted_category, match_percentage, missing_skills_text, position, mobile)
                            cur.execute(query, values)
                            
                            # Also insert into applications_history table for tracking
                            history_query = """INSERT INTO applications_history (candidate_email, candidate_name, position_applied_for, match_percentage, application_status) 
                                             VALUES (%s, %s, %s, %s, %s)"""
                            history_values = (email, fullName, position, match_percentage, 'Shortlisted')
                            cur.execute(history_query, history_values)
                            
                            mydb.commit()
                            cur.close()
                            mydb.close()
                            
                            st.success(f"✅ **Congratulations!** Your resume matches the job requirements with a {match_percentage:.1f}% score and has been added to the shortlist.")
                            st.info(f"📌 **Next Steps:** The HR team will review your profile and contact you at {email} soon.")
                        except Exception as db_error:
                            st.error(f"❌ Database error: {str(db_error)}")
                    else:
                        st.warning(f"⚠️ Your resume has a {match_percentage:.1f}% match score, which is below our threshold for automatic shortlisting.")
                        st.info("💡 Review the missing skills above and consider updating your resume before reapplying.")
            
            except Exception as e:
                st.error(f"❌ Error processing resume: {str(e)}")

st.markdown("---")

st.subheader("ℹ️ How It Works")
with st.expander("📖 View Instructions"):
    st.markdown("""
    **1. Review Job Description**
       - Read the job description and requirements above
       - Understand what skills and experience are needed
    
    **2. Fill in Your Information**
       - Provide your email, name, phone, and location
    
    **3. Upload Your Resume**
       - Upload in PDF, DOCX, or TXT format
       - Your resume will be analyzed against the job description
    
    **4. Get Detailed Results**
       - See your match percentage against the job description
       - View your predicted job category
       - Get specific feedback on missing skills to improve
    
    **5. Next Steps**
       - If your match score is 50% or higher, you're shortlisted
       - HR will contact you within 2-3 business days
       - Use the feedback to improve your resume for better matches
    """)

st.markdown("---")
st.subheader("📋 Track Your Applications")
st.markdown("""
Want to see where you've applied and track the status of your applications?
Click the button below to view your complete application history!
""")

if st.button("📊 View My Applications", use_container_width=True, key="view_applications"):
    st.switch_page("pages/Application_History.py")


