import sys
sys.path.insert(0, r'c:\Users\KARTIK S RATHOD\OneDrive\Desktop\Resume_ML\venv\Lib\site-packages')

import mysql.connector

# Connect to MySQL
mydb = mysql.connector.connect(
    user='root',
    password='Sheshi@1234',
    host='127.0.0.1',
    database='resumes',
    auth_plugin='mysql_native_password'
)

cur = mydb.cursor()

try:
    # Add category column if it doesn't exist
    alter_query = "ALTER TABLE employees ADD COLUMN category VARCHAR(50)"
    cur.execute(alter_query)
    mydb.commit()
    print("✅ Successfully added 'category' column to employees table")
except mysql.connector.errors.ProgrammingError as e:
    if "Duplicate column" in str(e):
        print("✅ Column 'category' already exists")
    else:
        print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    cur.close()
    mydb.close()
