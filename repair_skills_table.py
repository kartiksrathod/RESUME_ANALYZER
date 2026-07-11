import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='Sheshi@1234',
    host='127.0.0.1',
    database='resumes',
    auth_plugin='mysql_native_password',
)
cnx.autocommit = True
cur = cnx.cursor()
cur.execute('SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED')
cur.execute('DROP TABLE IF EXISTS skills')
cur.execute('CREATE TABLE skills (id INT AUTO_INCREMENT PRIMARY KEY, position VARCHAR(255) NOT NULL UNIQUE, skill TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
cur.executemany(
    'INSERT INTO skills (position, skill) VALUES (%s, %s)',
    [
        ('python developer', 'python, django, flask, fastapi, requests, pandas, numpy, scikit-learn'),
        ('java developer', 'java, spring, spring boot, maven, gradle, junit, hibernate'),
        ('data science', 'python, r, sql, machine learning, deep learning, tensorflow, pytorch, statistics'),
        ('devops engineer', 'docker, kubernetes, jenkins, aws, gcp, azure, terraform, ci/cd'),
        ('web designing', 'html, css, javascript, react, vue, figma, ui/ux, responsive design')
    ]
)
cur.close()
cnx.close()
print('skills table recreated successfully')
