import streamlit as st
import mysql.connector
st.set_page_config(page_title="Show Resumes")
mydb = mysql.connector.connect(user='root', password='Sheshi@1234',
                                                host='127.0.0.1', database='resumes',
                                                auth_plugin='mysql_native_password')
cur = mydb.cursor()
query0 = """SELECT POSITION FROM HR"""
cur.execute(query0)
positin1 = cur.fetchall()


mydb.commit()
position1 = list(positin1[0])
category=position1[0].lower()
query1 = f"""SELECT Name,Email,location,score,Resume,category FROM employees WHERE category = '{category}' ORDER BY score DESC"""
cur.execute(query1)
resumes = cur.fetchall()

colms = st.columns((1, 2, 3, 1))
fields = ["Name", 'Email', 'Location', "Resume"]
for col, field_name in zip(colms, fields):
    # header
    col.write(field_name)
c=0
for row in resumes:
    col1, col2, col3, col4, col5 = st.columns((1, 2, 2,1, 1))
    col1.write(row[0])  #name
    col2.write(row[1])  # email
    col3.write(row[2])  # location
    # col4.write(row[3])   # score
    disable_status = "X"  # flexible type of button
    # button_type = "Show" if disable_status else "Seen"
    button_phold = col5.empty()  # create a placeholder
    # do_action = button_phold.button(button_type, key=c)
    do_action = button_phold.button("Show", key=c, type="primary")
    if do_action:
        button_phold.button("Hide", key=str(c)+'_', type="primary")
        st.text(row[4])
    c+=1