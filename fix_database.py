import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

ROOT = Path(__file__).resolve().parent
env_path = ROOT / '.env'
if env_path.exists():
    load_dotenv(env_path)

connection = mysql.connector.connect(
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'password'),
    host=os.getenv('DB_HOST', '127.0.0.1'),
    database=os.getenv('DB_NAME', 'resumes'),
    auth_plugin=os.getenv('DB_AUTH_PLUGIN', 'mysql_native_password'),
)
cur = connection.cursor()


def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s",
        (table_name,),
    )
    return cursor.fetchone()[0] > 0


def column_exists(cursor, table_name, column_name):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s",
        (table_name, column_name),
    )
    return cursor.fetchone()[0] > 0


try:
    # Ensure HR table exists and contains required columns
    if not table_exists(cur, 'HR'):
        cur.execute(
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
        connection.commit()
        print("✅ Created HR table")
    else:
        if not column_exists(cur, 'HR', 'Position'):
            if column_exists(cur, 'HR', 'POSITION'):
                cur.execute("ALTER TABLE HR CHANGE POSITION Position VARCHAR(255)")
                connection.commit()
                print("✅ Renamed POSITION to Position in HR")
            else:
                cur.execute("ALTER TABLE HR ADD COLUMN Position VARCHAR(255)")
                connection.commit()
                print("✅ Added Position column to HR")
        if not column_exists(cur, 'HR', 'Experience'):
            cur.execute("ALTER TABLE HR ADD COLUMN Experience INT DEFAULT 0")
            connection.commit()
            print("✅ Added 'Experience' column to HR")
        if not column_exists(cur, 'HR', 'job_description'):
            cur.execute("ALTER TABLE HR ADD COLUMN job_description LONGTEXT")
            connection.commit()
            print("✅ Added 'job_description' column to HR")

    # Ensure skills table exists
    if not table_exists(cur, 'skills'):
        cur.execute(
            """
            CREATE TABLE skills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                position VARCHAR(255) NOT NULL UNIQUE,
                skill TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
        print("✅ Created skills table")
        
        # Insert sample data
        cur.executemany(
            """
            INSERT IGNORE INTO skills (position, skill) VALUES (%s, %s)
            """,
            [
                ('python developer', 'python, django, flask, fastapi, requests, pandas, numpy, scikit-learn'),
                ('java developer', 'java, spring, spring boot, maven, gradle, junit, hibernate'),
                ('data science', 'python, r, sql, machine learning, deep learning, tensorflow, pytorch, statistics'),
                ('devops engineer', 'docker, kubernetes, jenkins, aws, gcp, azure, terraform, ci/cd'),
                ('web designing', 'html, css, javascript, react, vue, figma, ui/ux, responsive design')
            ]
        )
        connection.commit()
        print("✅ Inserted sample skills data")
    else:
        # Check if table has correct structure
        cur.execute("DESCRIBE skills")
        columns = [row[0] for row in cur.fetchall()]
        if 'position' not in columns or 'skill' not in columns:
            cur.execute("DROP TABLE skills")
            connection.commit()
            print("✅ Dropped malformed skills table")
            
            cur.execute(
                """
                CREATE TABLE skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    position VARCHAR(255) NOT NULL UNIQUE,
                    skill TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()
            print("✅ Recreated skills table")
            
            # Insert sample data
            cur.executemany(
                """
                INSERT IGNORE INTO skills (position, skill) VALUES (%s, %s)
                """,
                [
                    ('python developer', 'python, django, flask, fastapi, requests, pandas, numpy, scikit-learn'),
                    ('java developer', 'java, spring, spring boot, maven, gradle, junit, hibernate'),
                    ('data science', 'python, r, sql, machine learning, deep learning, tensorflow, pytorch, statistics'),
                    ('devops engineer', 'docker, kubernetes, jenkins, aws, gcp, azure, terraform, ci/cd'),
                    ('web designing', 'html, css, javascript, react, vue, figma, ui/ux, responsive design')
                ]
            )
            connection.commit()
            print("✅ Inserted sample skills data")

    # Ensure employees table exists and contains required columns
    if not table_exists(cur, 'employees'):
        cur.execute(
            """
            CREATE TABLE employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Email VARCHAR(255),
                Resume LONGTEXT,
                score FLOAT,
                location VARCHAR(255),
                category VARCHAR(255),
                match_percentage FLOAT,
                missing_skills TEXT,
                position_applied_for VARCHAR(255),
                mobile_number VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
        print("✅ Created employees table")
    else:
        if not column_exists(cur, 'employees', 'match_percentage'):
            cur.execute("ALTER TABLE employees ADD COLUMN match_percentage FLOAT")
            connection.commit()
            print("✅ Added 'match_percentage' column to employees")
        if not column_exists(cur, 'employees', 'missing_skills'):
            cur.execute("ALTER TABLE employees ADD COLUMN missing_skills TEXT")
            connection.commit()
            print("✅ Added 'missing_skills' column to employees")
        if not column_exists(cur, 'employees', 'position_applied_for'):
            cur.execute("ALTER TABLE employees ADD COLUMN position_applied_for VARCHAR(255)")
            connection.commit()
            print("✅ Added 'position_applied_for' column to employees")
        if not column_exists(cur, 'employees', 'mobile_number'):
            cur.execute("ALTER TABLE employees ADD COLUMN mobile_number VARCHAR(20)")
            connection.commit()
            print("✅ Added 'mobile_number' column to employees")
        cur.execute("SELECT DATA_TYPE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'employees' AND COLUMN_NAME = 'Resume'")
        resume_type = cur.fetchone()
        if resume_type and resume_type[0] in ('blob', 'mediumblob', 'longblob'):
            cur.execute("ALTER TABLE employees MODIFY COLUMN Resume LONGTEXT")
            connection.commit()
            print("✅ Converted 'Resume' column to LONGTEXT in employees")

    # Ensure applications_history table exists
    if not table_exists(cur, 'applications_history'):
        cur.execute(
            """
            CREATE TABLE applications_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                candidate_email VARCHAR(255) NOT NULL,
                candidate_name VARCHAR(255) NOT NULL,
                position_applied_for VARCHAR(255) NOT NULL,
                match_percentage FLOAT,
                application_status ENUM('Applied', 'Under Review', 'Shortlisted', 'Interview', 'Rejected') DEFAULT 'Applied',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
        print("✅ Created applications_history table")
    else:
        if not column_exists(cur, 'applications_history', 'match_percentage'):
            cur.execute("ALTER TABLE applications_history ADD COLUMN match_percentage FLOAT")
            connection.commit()
            print("✅ Added 'match_percentage' column to applications_history")
        if not column_exists(cur, 'applications_history', 'application_status'):
            cur.execute("ALTER TABLE applications_history ADD COLUMN application_status ENUM('Applied', 'Under Review', 'Shortlisted', 'Interview', 'Rejected') DEFAULT 'Applied'")
            connection.commit()
            print("✅ Added 'application_status' column to applications_history")

    print("✅ Database schema is now up to date.")
except mysql.connector.Error as e:
    print(f"❌ MySQL error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
finally:
    cur.close()
    connection.close()
