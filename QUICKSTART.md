# 🚀 Quick Start Guide - AI Resume Screening System

## Prerequisites

- Python 3.11+ installed
- MySQL running on your system
- Virtual environment activated (optional but recommended)

## 1️⃣ Initial Setup (One Time Only)

### Step 1: Install Dependencies

```bash
cd resume-screening
pip install -r requirements.txt
```

**If you get compilation errors on Windows:**

```bash
# Use conda instead
conda install scikit-learn nltk joblib mysql-connector-python streamlit python-dotenv
```

### Step 2: Configure Environment

```bash
copy .env.example .env
```

**Edit `.env` and update MySQL credentials if needed:**

```
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_NAME=resumes
```

### Step 3: Setup Database

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE resumes;"

# Initialize schema
mysql -u root -p resumes < init_database.sql
```

**Verify database is ready:**

```bash
mysql -u root -p resumes -e "SHOW TABLES;"
```

---

## 2️⃣ Running the System

### 🟦 For HR Team

**Configure Job Position & Description:**

```bash
streamlit run HR.py
```

- Select "👨‍💼 HR Manager" role
- Enter position name (e.g., "Python Developer")
- Paste detailed job description
- Click "Save Configuration"
- System is now ready for candidates

**View Shortlisted Candidates:**

- In the same app, navigate to "Show Resumes" in the sidebar
- See all candidates with 50%+ match score
- Sort by score, name, or date
- View missing skills for each candidate
- Click to see full resume text

---

### 🟩 For Candidates

**View Job Openings & Apply:**

```bash
streamlit run HR.py
```

- Select "👤 Job Candidate" role
- View the current job position and description
- Click "🚀 Apply for this Position" to upload your resume
- Fill in: Name, Email, Phone, Location
- Upload resume (PDF/DOCX/TXT)
- Get instant match score and missing skills feedback
- If match ≥ 50%, you're automatically shortlisted!

**Track Your Applications:**

- In the same app, navigate to "Application History" in the sidebar
- Enter your email to view all your applications
- See match scores, status, and application dates

---

```bash
streamlit run "pages/Application_History.py"
```

- Opens at `http://localhost:8504`
- Enter your email address
- See all positions you've applied for
- View match scores for each application
- Track application status (Shortlisted/Interview/Rejected)
- Compare your fit across different roles

---

## 3️⃣ Running All Services (Recommended)

Open **4 separate terminals** and run:

**Terminal 1:**

```bash
streamlit run HR.py
```

**Terminal 2:**

```bash
streamlit run Upload_Resume.py
```

**Terminal 3:**

```bash
streamlit run "pages/Show Resumes.py"
```

**Terminal 4:**

```bash
streamlit run "pages/Application_History.py"
```

---

## 📋 Complete Workflow Example

### Scenario: Hiring a Python Developer

**1. HR Sets Up Job (9:00 AM)**

- Run: `streamlit run HR.py`
- Select "👨‍💼 HR Manager" role
- Enter position: "Senior Python Developer"
- Enter job description with requirements
- Save configuration

**2. Candidate Applies (10:00 AM)**

- Run: `streamlit run HR.py`
- Select "👤 Job Candidate" role
- View the job description
- Click "Apply for this Position"
- Upload resume
- Get 78% match score
- See: "Missing: Docker, Kubernetes, MongoDB"

**3. HR Reviews Applications (11:00 AM)**

- In the same app, navigate to "Show Resumes" page
- See candidate with 78% match (shortlisted)
- Check their resume
- Note the missing skills

**4. Candidate Checks Status (10:30 AM)**

- In the same app, navigate to "Application History" page
- Enter email
- See "Senior Python Developer - 78% Match - Shortlisted"
- Check stats: "Average Match: 72%"

---

## 🔧 Troubleshooting

### ❌ "Port 8501 is already in use"

```bash
# Run on different port
streamlit run HR.py --server.port 8505
```

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit python-dotenv mysql-connector-python scikit-learn nltk joblib
```

### ❌ "Cannot connect to MySQL"

```bash
# Check MySQL is running
mysql -u root -p

# Verify credentials in .env
cat .env

# Test database
mysql -u root -p resumes -e "SELECT 1;"
```

### ❌ "Import error: cv.pickle not found"

- Make sure you're in the `resume-screening` directory
- Check that `cv.pickle` exists in the current folder
- Check that `RF.joblib` is extracted from `RF.joblib.zip`

---

## 📊 Files & What They Do

| File                         | Purpose                                                                                               | Run Command           |
| ---------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------- |
| HR.py                        | Main app - HR configures job postings, candidates upload resumes, view candidates, track applications | `streamlit run HR.py` |
| pages/Upload_Resume.py       | Candidates upload resumes                                                                             | Navigate in app       |
| pages/Show_Resumes.py        | HR views candidates                                                                                   | Navigate in app       |
| pages/Application_History.py | Candidates track applications                                                                         | Navigate in app       |
| model_training.ipynb         | View model training details                                                                           | Open in Jupyter       |
| db_config.py                 | Database configuration                                                                                | Auto-imported         |
| categories.json              | Job category mappings                                                                                 | Auto-loaded           |

---

## 🎯 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Resume Screening System                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   HR.py      │    │HR Dashboard  │    │Session Mgmt  │   │
│  │ Configure    │    │Show_Resumes  │    │Track Apps    │   │
│  │  Job Post    │    │  .py         │    │Application  │   │
│  │ Description  │    │              │    │_History.py  │   │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘   │
│         │                   │                   │            │
│  ┌──────┴───────────────────┴───────────────────┴──────┐    │
│  │        Upload_Resume.py - Candidate Portal          │    │
│  │  • View Job Description   • Upload Resume           │    │
│  │  • Get Match Score        • View Missing Skills     │    │
│  └──────────┬─────────────────────────────────────────┘    │
│             │                                               │
│  ┌──────────v─────────────────────────────────────────┐    │
│  │      ML Pipeline (TF-IDF + Semantic Similarity)     │    │
│  │  • Resume Processing    • Feature Extraction         │    │
│  │  • Job Description Analysis    • Matching Score      │    │
│  └──────────┬─────────────────────────────────────────┘    │
│             │                                               │
│  ┌──────────v─────────────────────────────────────────┐    │
│  │    MySQL Database (4 Tables)                        │    │
│  │  • HR               • skills                         │    │
│  │  • employees        • applications_history           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Tips & Best Practices

✅ **Keep 4 terminals open** for seamless workflow
✅ **Set detailed job descriptions** for better matching
✅ **Check candidate stats** before interviews
✅ **Update application status** so candidates stay informed
✅ **Review missing skills** to provide feedback to candidates

---

## 🆘 Need Help?

1. Check `README.md` for detailed documentation
2. Review error logs in terminal output
3. Verify all prerequisites are installed
4. Ensure database tables are created correctly
5. Check that model files (`RF.joblib`, `cv.pickle`) exist

---

**Last Updated:** April 2026
**Version:** 2.0 - Application Tracking
**Status:** ✅ Production Ready
