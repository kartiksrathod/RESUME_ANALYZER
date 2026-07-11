import streamlit as st
import pandas as pd
from db_config import get_db_connection


def ensure_hr_table_schema(cursor):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'HR'"
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """
            CREATE TABLE HR (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Position VARCHAR(255) NOT NULL,
                Experience INT DEFAULT 0,
                job_description LONGTEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        return

    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'HR' AND COLUMN_NAME = 'Experience'"
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute("ALTER TABLE HR ADD COLUMN Experience INT DEFAULT 0")

    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'HR' AND COLUMN_NAME = 'job_description'"
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute("ALTER TABLE HR ADD COLUMN job_description LONGTEXT")


st.set_page_config(page_title="AI Resume Screening System", layout="wide")

st.title("🎯 AI Resume Screening System")
st.markdown("---")

# Role selection
role = st.radio(
    "Select your role:",
    ["👨‍💼 HR Manager", "👤 Job Candidate"],
    horizontal=True,
    help="Choose your role to access the appropriate features"
)

st.markdown("---")

if role == "👨‍💼 HR Manager":
    st.header("HR Dashboard")
    st.markdown("""
    ### Configure Job Positions
    Set up job postings and requirements for resume screening.
    """)

    st.markdown("""
    ### Set the Job Position and Description
    Configure the job position and upload a detailed job description. This will be used to analyze candidate resumes and provide detailed matching scores.
    """)

    with st.form("HR form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            position = st.text_input(
                label="📋 Job Position", 
                placeholder="e.g., Python Developer, Data Science, etc.",
                help="Enter the job position you are hiring for"
            )
        
        with col2:
            exp = st.text_input(
                label="📅 Minimum Experience (years)", 
                placeholder="e.g., 2, 5, 10",
                help="Minimum years of experience required"
            )
        
        job_description = st.text_area(
            label="📄 Job Description",
            placeholder="Enter detailed job description including requirements, responsibilities, skills needed, etc.",
            help="Provide a comprehensive job description that will be used to match against candidate resumes",
            height=200
        )
        
        submitted = st.form_submit_button("💾 Save Position & Description", use_container_width=True)

    if submitted:
        position = position.strip()
        exp = exp.strip()
        job_description = job_description.strip()

        if not position:
            st.error("❌ Position is required.")
        elif not exp:
            st.error("❌ Experience is required.")
        elif not job_description:
            st.error("❌ Job description is required.")
        else:
            try:
                exp_value = int(exp)
            except ValueError:
                st.error("❌ Experience must be a numeric value.")
            else:
                try:
                    mydb = get_db_connection()
                    cur = mydb.cursor()
                    ensure_hr_table_schema(cur)
                    position_lower = position.lower()
                    query0 = """TRUNCATE TABLE HR"""
                    cur.execute(query0)
                    mydb.commit()
                    query = """INSERT INTO HR (Position,Experience,job_description) VALUES (%s,%s,%s)"""
                    value = (position_lower, exp_value, job_description)
                    cur.execute(query, value)
                    mydb.commit()
                    cur.close()
                    mydb.close()
                    st.success(f"✅ Position '{position}' and job description saved successfully!")
                    st.info(f"📌 Candidates will now be screened for: **{position}** (Min exp: {exp_value} years)")
                except Exception as e:
                    st.error(f"❌ Database error: {str(e)}")

    st.markdown("---")

    st.subheader("📊 Current Configuration")
    try:
        mydb = get_db_connection()
        cur = mydb.cursor()
        ensure_hr_table_schema(cur)
        cur.execute("SELECT Position, Experience, job_description FROM HR LIMIT 1")
        row = cur.fetchone()
        cur.close()
        mydb.close()
        
        if row:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Position", value=row[0].upper())
            with col2:
                st.metric(label="Min Experience", value=f"{row[1]} years")
            
            st.markdown("**📄 Job Description:**")
            st.info(row[2])
        else:
            st.warning("⚠️  No position configured yet. Set a position above to get started.")
    except Exception as e:
        st.error(f"❌ Unable to fetch configuration: {str(e)}")

    st.markdown("---")

    st.subheader("ℹ️ Next Steps")
    st.markdown("""
    1. **Set the position above** using the form
    2. **Share the app link with candidates**: Run `streamlit run HR.py` and direct them to the "Upload Resume" page
    3. **Review shortlisted resumes**: Use the navigation menu → Show Resumes
    """)

else:  # Candidate section
    st.header("Job Seeker Portal")
    st.markdown("""
    ### Available Job Openings
    View current job positions and apply for roles that match your skills.
    """)

    try:
        mydb = get_db_connection()
        cur = mydb.cursor()
        ensure_hr_table_schema(cur)
        cur.execute("SELECT Position, Experience, job_description FROM HR LIMIT 1")
        row = cur.fetchone()
        cur.close()
        mydb.close()
        
        if row:
            st.subheader(f"📋 {row[0].title()}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Position", value=row[0].title())
            with col2:
                st.metric(label="Min Experience Required", value=f"{row[1]} years")
            
            st.markdown("**📄 Job Description:**")
            st.info(row[2])
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Apply for this Position", use_container_width=True, type="primary"):
                    st.switch_page("pages/Upload_Resume.py")
            
            st.markdown("---")
            
            st.subheader("📊 Application Status")
            st.markdown("""
            After uploading your resume, you can:
            - Track your application status
            - View match scores and feedback
            - See missing skills recommendations
            """)
            
            if st.button("📋 View My Applications", use_container_width=True):
                st.switch_page("pages/Application_History.py")
                
        else:
            st.warning("⚠️ No job positions are currently available. Please check back later or contact HR.")
            st.info("💡 HR needs to configure job positions first before candidates can apply.")
            
    except Exception as e:
        st.error(f"❌ Unable to load job openings: {str(e)}")
