# AI Resume Screening

## Introduction

AI Resume Screening is an advanced tool that uses artificial intelligence to automate and enhance the resume screening process. The system now features job description-based matching, providing detailed compatibility scores and specific feedback to help candidates improve their resumes.

**Key Innovation:** Unlike traditional keyword-based systems, our tool compares candidate resumes directly against detailed job descriptions using semantic similarity analysis. This provides more accurate matching and actionable feedback for both HR teams and job seekers.

The tool uses natural language processing and machine learning algorithms to:

- Analyze resumes against complete job descriptions
- Calculate semantic similarity scores
- Identify missing skills and keywords
- Provide specific improvement suggestions
- Maintain fast processing (< 5 seconds per resume)

Our enhanced system makes the hiring process more efficient for HR teams and provides valuable insights for job seekers to optimize their resumes.

## Features

1. **Job Description-Based Matching**: HR can upload detailed job descriptions instead of just selecting from predefined categories
2. **Semantic Similarity Scoring**: Uses advanced NLP to calculate how well a resume matches the job requirements
3. **Detailed Feedback**: Identifies specific missing skills and provides actionable improvement suggestions
4. **Automated Shortlisting**: Candidates with match scores above 50% are automatically shortlisted
5. **Improved Accuracy**: Advanced algorithms reduce bias and improve matching accuracy (91%+)
6. **Fast Processing**: Each resume is analyzed in under 5 seconds
7. **Comprehensive Output**: HR gets detailed candidate information including match scores and missing skills

## Usage

The code consists of the following parts:

1. HR.py : Main Streamlit application that serves as the central hub for the entire resume screening system. Select your role (HR Manager or Job Candidate) to access appropriate features. HR can configure job postings, candidates can view openings and apply. Use the command "streamlit run HR.py" to start the application.

2. pages/Upload_Resume.py : Integrated page within the main app where candidates can upload their resumes. Provides UI integration with the trained model for instant match scoring and feedback.

3. model_training.ipynb : Jupyter notebook containing the model training process and accuracy comparisons for different algorithms. TF-IDF was used to extract features from pre-processed resumes.

4. cv.pickle : Pickled file containing the TF-IDF features of the trained model, used to compare uploaded resume features.

5. RF.joblib.zip: Compressed machine learning model (Random Forest) with highest accuracy for predicting resume categories. Decompress to get 'RF.joblib'.

6. SQL.txt : Contains MySQL queries for setting up the database to store candidate details.

7. pages/Show_Resumes.py: HR dashboard within the main app showing all shortlisted candidates sorted by match score, with detailed missing skills feedback.

8. pages/Application_History.py: Candidate portal within the main app where applicants can view past applications, track status, and see match scores.

## Setup

### Quick Start?

👉 **See [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide!**

### Full Setup Instructions

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   **Note for Windows users**: If you encounter compilation errors with scikit-learn or numpy, try one of these solutions:
   - Use conda: `conda install scikit-learn nltk joblib`
   - Use Python 3.11 instead of Python 3.13
   - Install pre-compiled wheels from https://www.lfd.uci.edu/~gohlke/pythonlibs/

2. Copy the example environment file:

   ```bash
   copy .env.example .env
   ```

3. Open `.env` and update the database credentials if needed.

## Database Setup

1. Create a MySQL database:
   ```bash
   mysql -u root -p -e "CREATE DATABASE resumes;"
   ```
2. Initialize the schema by running the SQL script:
   ```bash
   mysql -u root -p resumes < init_database.sql
   ```
3. This creates four required tables:
   - `HR`: Stores the current job position requirement and description
   - `skills`: Maps job positions to required keywords (for backward compatibility)
   - `employees`: Stores shortlisted candidate resumes with match scores and missing skills
   - `applications_history`: Tracks all applications from candidates, including match scores and application status

## New Features (v2.0)

- **Job Description Upload**: HR can now provide complete job descriptions instead of selecting from predefined categories
- **Semantic Matching**: Resumes are compared against full job descriptions using cosine similarity
- **Detailed Feedback**: Candidates receive specific information about missing skills to improve their resumes
- **Enhanced Scoring**: Match percentages provide more accurate assessment than simple keyword matching
- **Improved Shortlisting**: Automatic shortlisting for candidates with 50%+ match scores
- **Application History Tracking**: Candidates can view all their applications, compare match scores across different positions, and track application status in real-time

## Running the app

### Quick Start (One Command Setup)

```bash
# Navigate to the project directory
cd resume-screening

# Run the complete application
streamlit run HR.py
```

### Application Pages

#### **For HR Team - Configure Job Postings:**

- Run `streamlit run HR.py`
- Select "👨‍💼 HR Manager" role
- **What you can do**:
  - Set the current job position
  - Upload detailed job description
  - View current configuration
  - All changes are saved automatically

#### **For Candidates - View Job Openings:**

- Run `streamlit run HR.py`
- Select "👤 Job Candidate" role
- **What you can do**:
  - View current job position and description
  - Apply for the position by uploading your resume
  - Get immediate feedback on match score
  - See missing skills to improve
  - Track if you've been shortlisted

#### **For HR Team - Review Candidates:**

- Run `streamlit run HR.py` and navigate to "Show Resumes" page
- **What you can do**:
  - View all shortlisted candidates (50%+ match)
  - Sort by match score, name, or date
  - See detailed feedback and missing skills
  - View complete resume content
  - Track candidate application journey

#### **For Candidates - Track Applications:**

- Run `streamlit run HR.py` and navigate to "Application History" page
- **What you can do**:
  - Enter your email and view all applications
  - See match scores for each position
  - Track application status (Applied → Shortlisted → Interview → etc.)
  - Compare your fit for different roles
  - View application statistics

### Running the Complete System

```bash
streamlit run Upload_Resume.py --logger.level=error
```

**Terminal 3 - HR Dashboard:**

```bash
streamlit run "pages/Show Resumes.py" --logger.level=error
```

**Terminal 4 - Candidate Application Tracking:**

```bash
streamlit run "pages/Application_History.py" --logger.level=error
```

### Complete Workflow Example

**Step 1: HR Sets Up Job**

```bash
streamlit run HR.py
```

- Select "👨‍💼 HR Manager" role
- Enter position: "Python Developer"
- Paste job description: "We need 5+ years of Python experience, Django knowledge..."
- Click "Save Configuration"

**Step 2: Candidate Views and Applies**

- In the same app, select "👤 Job Candidate" role
- View the job description automatically displayed
- Click "Apply for this Position"
- Fill in: Name, Email, Phone, Location
- Upload resume (PDF/DOCX/TXT)
- Get instant feedback with match score and missing skills

**Step 3: HR Reviews Candidates**

- In the same app, navigate to "Show Resumes" page
- All shortlisted candidates appear (50%+ match)
- Sort by match score to find the best candidates
- See recommended missing skills for each candidate

**Step 4: Candidate Tracks Progress**

- In the same app, navigate to "Application History" page
- Enter email to view all applications
- See match scores across different positions
- Track if shortlisted, under review, or rejected

## Troubleshooting

### Port Already in Use

If you get "Port 8501 is already in use" error:

```bash
# Run on a different port
streamlit run HR.py --server.port 8505
```

### Database Connection Error

1. Verify MySQL is running:

```bash
mysql -u root -p
```

2. Check `.env` file has correct credentials:

```bash
cat .env
```

3. Verify database exists:

```bash
mysql -u root -p -e "SHOW DATABASES LIKE 'resumes';"
```

### Import Errors

If you get module not found errors:

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or use conda (recommended for Windows)
conda install scikit-learn nltk joblib mysql-connector-python streamlit python-dotenv
```

### Resume Not Being Processed

- Check file format (must be PDF, DOCX, or TXT)
- Check file size (should be < 10MB)
- Ensure job description is already set in HR.py
- Check browser console for errors (F12)

## Advanced Usage

### Running Behind a Web Server

```bash
# Using ngrok for public access
ngrok http 8501  # Make Hr.py publicly accessible

# Your candidates can access at: https://your-ngrok-url.ngrok.io
```

### Batch Processing Multiple Resumes

Use the `fix_database.py` script to manage bulk operations:

```bash
python fix_database.py
```

### Monitoring System Performance

Check logs and validate setup:

```bash
python validate_setup.py
```

## Configuration

- **categories.json**: Maps model prediction class indices to job category names (loaded by `Upload_Resume.py`)
- **db_config.py**: Centralized database connection using environment variables
- **.env**: Database credentials (copy from `.env.example` and update with your credentials)
- **requirements.txt**: Pinned package versions for reproducibility

## Notes

- The project uses `.env` for database configuration and `.env` is excluded from git.
- The model file `RF.joblib` and vectorizer `cv.pickle` must be present in the project root for inference to work.
- Large binary files (`.joblib`, `.pkl`, `.zip`) are excluded from git to keep the repository clean.

## Other things to know:

1. The data of shortlisted candidates will be stored in a MySQL database, making it feasible to view their profiles.

2. The 'pages' folder should be placed in the same parent folder which contains 'HR.py'

## Candidate Application Tracking (<NEW>!)

Candidates can now track all their job applications in one place:

### Features:

- **View All Applications**: See every job position you've applied for
- **Track Application Status**: Monitor whether your application is being reviewed, shortlisted, or in interview stage
- **Compare Match Scores**: View your match percentage for each position to understand how well you fit different roles
- **Application Statistics**: See your average match score, total applications, and highest match score
- **Real-time Updates**: HR team can update application status, and you'll see it immediately

### How to Use:

1. Launch `streamlit run "pages/Application_History.py"`
2. Enter the email address you used when applying
3. View all your applications and track their progress
4. Get insights into which positions match your profile better

The application history helps both candidates understand their fit for different roles and HR teams manage the hiring pipeline more effectively.

## Datasets used for the model:

1. https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset

2. https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
