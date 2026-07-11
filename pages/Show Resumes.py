import streamlit as st
from db_config import get_db_connection

st.set_page_config(page_title="Show Resumes")

mydb = get_db_connection()
cur = mydb.cursor()
query0 = """SELECT POSITION FROM HR"""
cur.execute(query0)
row = cur.fetchone()

if not row or not row[0]:
    st.warning("No HR position is set. Please add a position via HR.py first.")
    st.stop()

category = row[0].lower()
cur.execute("SHOW COLUMNS FROM employees")
employee_columns = {column[0].lower() for column in cur.fetchall()}

if 'match_percentage' in employee_columns:
    match_column = 'match_percentage'
elif 'score' in employee_columns:
    match_column = 'score'
else:
    st.error("No match score column found in the employees table. Please run fix_database.py to update the schema.")
    st.stop()

missing_skills_expression = 'missing_skills' if 'missing_skills' in employee_columns else "'' AS missing_skills"

query1 = f"SELECT Name,Email,location,{match_column} AS match_percentage,Resume,category,{missing_skills_expression} FROM employees ORDER BY {match_column} DESC"
cur.execute(query1)
resumes = cur.fetchall()

st.title("Shortlisted Resumes")
st.subheader("All Candidates (Sorted by Match Score)")

if not resumes:
    st.info("No resumes found yet.")
    st.stop()

for idx, (name, email, location, match_percentage, resume_text, category_name, missing_skills) in enumerate(resumes):
    if isinstance(resume_text, (bytes, bytearray)):
        resume_text = resume_text.decode('utf-8', errors='ignore')
    if category_name is None:
        category_name = 'Uncategorized'
    if missing_skills is None:
        missing_skills = 'None identified'

    with st.expander(f"{name} — {email} — Match: {match_percentage:.1f}% — {category_name}", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Location:**", location)
            st.write("**Match Score:**", f"{match_percentage:.1f}%")
        with col2:
            st.write("**Category:**", category_name)
            if missing_skills and missing_skills != 'None identified':
                st.write("**Missing Skills:**", missing_skills)
            else:
                st.write("**Missing Skills:** None identified")
        
        st.markdown("**Resume:**")
        st.write(resume_text)
