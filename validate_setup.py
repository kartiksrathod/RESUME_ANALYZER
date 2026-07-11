import os
import sys
from pathlib import Path
from db_config import get_db_connection

def check_model_files():
    """Check if required model files exist."""
    errors = []
    
    cv_file = Path('cv.pickle')
    model_file = Path('RF.joblib')
    categories_file = Path('categories.json')
    
    if not cv_file.exists():
        errors.append(f"❌ Missing: {cv_file}")
    if not model_file.exists():
        errors.append(f"❌ Missing: {model_file}")
    if not categories_file.exists():
        errors.append(f"❌ Missing: {categories_file}")
    
    return errors

def check_database():
    """Check if database connection works."""
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE()")
        result = cursor.fetchone()
        mydb.close()
        return True, "✅ Database connection successful"
    except Exception as e:
        return False, f"❌ Database connection failed: {str(e)}"

def check_nltk_stopwords():
    """Check if NLTK stopwords are available."""
    try:
        from nltk.corpus import stopwords
        stopwords.words('english')
        return True, "✅ NLTK stopwords available"
    except Exception as e:
        return False, f"⚠️  NLTK stopwords not found. Run: python -m nltk.downloader stopwords"

def validate_environment():
    """Run all environment checks."""
    print("\n" + "="*60)
    print(" AI Resume Screening - Setup Validation")
    print("="*60 + "\n")
    
    # Check model files
    model_errors = check_model_files()
    if model_errors:
        print("Model Files:")
        for error in model_errors:
            print(f"  {error}")
    else:
        print("✅ All model files present")
    
    # Check database
    db_ok, db_msg = check_database()
    print(f"\nDatabase: {db_msg}")
    
    # Check NLTK
    nltk_ok, nltk_msg = check_nltk_stopwords()
    print(f"NLTK: {nltk_msg}")
    
    print("\n" + "="*60)
    
    if model_errors or not db_ok:
        print("⚠️  Setup incomplete. Please fix the issues above.")
        return False
    else:
        print("✅ All checks passed! Ready to run the app.")
        return True

if __name__ == '__main__':
    success = validate_environment()
    sys.exit(0 if success else 1)
