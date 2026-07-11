import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path to import db_config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from db_config import get_db_connection

st.set_page_config(page_title="Application History", layout="wide")

st.title("📋 My Application History")
st.markdown("---")

# Add section for candidate login/identification
st.subheader("🔍 View Your Applications")
st.info("Enter your email address to see all the job positions you have applied for and track your application status.")

col1, col2 = st.columns([2, 1])
with col1:
    email = st.text_input(
        label='📧 Email Address',
        placeholder='your.email@example.com',
        help='Enter the email address you used to apply'
    )

with col2:
    show_applications = st.button('🔎 View Applications', use_container_width=True)

st.markdown("---")

if show_applications:
    email = email.strip()
    
    if not email:
        st.error("❌ Please enter your email address.")
    else:
        try:
            mydb = get_db_connection()
            cur = mydb.cursor()
            
            # Fetch application history for the candidate
            query = """SELECT candidate_name, position_applied_for, match_percentage, application_status, applied_at 
                      FROM applications_history 
                      WHERE candidate_email = %s 
                      ORDER BY applied_at DESC"""
            cur.execute(query, (email,))
            applications = cur.fetchall()
            cur.close()
            mydb.close()
            
            if not applications:
                st.warning("⚠️ No applications found for this email address.")
                st.info("💡 **Tip:** Make sure you enter the same email address you used when applying.")
            else:
                # Get candidate name from first application
                candidate_name = applications[0][0]
                
                st.success(f"✅ Found **{len(applications)}** application(s) for **{candidate_name}**")
                st.markdown("---")
                
                # Display applications in a formatted table
                st.subheader(f"📊 Application Summary - {candidate_name}")
                
                # Create dataframe for better visualization
                app_data = []
                for app in applications:
                    app_data.append({
                        "Position": app[1],
                        "Match Score": f"{app[2]:.1f}%",
                        "Status": app[3],
                        "Applied On": app[4].strftime("%Y-%m-%d %H:%M:%S") if app[4] else "N/A"
                    })
                
                df = pd.DataFrame(app_data)
                
                # Display as table
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                
                # Display detailed application cards
                st.subheader("📌 Application Details")
                
                for idx, app in enumerate(applications, 1):
                    with st.expander(f"Position {idx}: {app[1]} - Status: {app[3]}", expanded=(idx == 1)):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Match Score", f"{app[2]:.1f}%")
                        
                        with col2:
                            status_color = "🟢" if app[3] == "Shortlisted" else "🟡" if app[3] == "Under Review" else "🔴" if app[3] == "Rejected" else "🔵"
                            st.metric("Status", f"{status_color} {app[3]}")
                        
                        with col3:
                            st.metric("Position", app[1])
                        
                        with col4:
                            st.metric("Applied On", app[4].strftime("%b %d") if app[4] else "N/A")
                        
                        # Show match score interpretation
                        match_score = app[2]
                        if match_score >= 80:
                            st.success("✅ Excellent match! Your profile aligns well with this position.")
                        elif match_score >= 60:
                            st.info("ℹ️ Good match! You have most of the required skills.")
                        elif match_score >= 50:
                            st.warning("⚠️ Moderate match. Consider improving the missing skills identified during application.")
                        else:
                            st.error("❌ Low match. This position may require additional skills.")
                
                # Summary statistics
                st.markdown("---")
                st.subheader("📈 Your Application Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                total_applications = len(applications)
                avg_match = sum([app[2] for app in applications]) / total_applications if applications else 0
                
                with col1:
                    st.metric("Total Applications", total_applications)
                
                with col2:
                    st.metric("Average Match Score", f"{avg_match:.1f}%")
                
                with col3:
                    shortlisted = sum([1 for app in applications if app[3] == "Shortlisted"])
                    st.metric("Shortlisted", shortlisted)
                
                with col4:
                    highest_match = max([app[2] for app in applications]) if applications else 0
                    st.metric("Highest Match", f"{highest_match:.1f}%")
                
                st.markdown("---")
                st.info("""
                **📝 What do the statuses mean?**
                - 🟢 **Shortlisted**: Your resume matches the job requirements (50%+ match)
                - 🟡 **Under Review**: HR team is reviewing your application
                - 🔵 **Interview**: You've been selected for an interview
                - 🔴 **Rejected**: Your profile didn't meet the requirements for this position
                """)
        
        except Exception as e:
            st.error(f"❌ Error fetching applications: {str(e)}")
            st.info("💡 Please try again or contact HR support if the error persists.")

# Navigation footer
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back to Upload Resume", use_container_width=True):
        st.switch_page("pages/Upload_Resume.py")

with col2:
    if st.button("📄 Upload New Resume", use_container_width=True):
        st.switch_page("pages/Upload_Resume.py")
