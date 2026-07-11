import streamlit as st

st.set_page_config(page_title="Resume Screening", layout="wide")

st.title("📄 Resume Screening System")
st.markdown("---")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Home", "Upload Resume", "Show Resumes", "Application History"])

if page == "Home":
    st.header("Welcome to Resume Screening System")
    st.write("""
    This application helps with:
    - 📤 Uploading and screening resumes
    - 📋 Viewing submitted resumes
    - 📊 Tracking your application history
    """)
elif page == "Upload Resume":
    st.markdown(":arrow_left: Use the sidebar to navigate to Upload Resume page")
elif page == "Show Resumes":
    st.markdown(":arrow_left: Use the sidebar to navigate to Show Resumes page")
elif page == "Application History":
    st.markdown(":arrow_left: Use the sidebar to navigate to Application History page")
