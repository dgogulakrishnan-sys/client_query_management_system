import streamlit as st
import mysql.connector
import hashlib
import pandas as pd
import math

# ---------- MySQL Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Durai@8695",
        database="client_query_management"
    )

# ---------- Password Utils ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    if hash_password(password) == hashed:
        return True
    else:
        return False

# ---------- Authentication ----------
def authenticate_user(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT hashed_password FROM users WHERE username = %s and role=%s"
    cursor.execute(query, (username,role))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and verify_password(password, user["hashed_password"]):
        return True
    return False

def create_query(username, mobile_number,query_title, query_description):
    conn = get_db_connection()
    cursor = conn.cursor()
    query="INSERT into queries (mobile_number,query_heading,query_description,username) values (%s,%s,%s,%s);"
    cursor.execute(query, (mobile_number,query_title,query_description,username))
    conn.commit()
    cursor.close()
    conn.close()

def get_query(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    query= "select query_id,query_heading,status from queries where username = %s;"
    cursor.execute(query, (username,))
    queries = cursor.fetchall()
    dicts = [{"ID": t[0], "Heading": t[1], "Status": t[2]} for t in queries]
    cursor.close()
    conn.close()
    return dicts

def support_query():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "select query_id, username, mobile_number, query_heading, query_description, status, query_created_time, query_closed_time, TIMEDIFF(query_closed_time, query_created_time) as Duration from queries order by status desc;"
    cursor.execute(query, )
    queries = cursor.fetchall()
    dicts = [{"ID": t[0], "User":t[1], "Mobile":t[2], "Query Title":t[3],"Query Description":t[4], "Status":t[5], "Created Time":t[6], "Closed Time":t[7], "Duration":t[8]} for t in queries]
    cursor.close()
    conn.close()
    print(dicts)
    return dicts


def update_query(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    id = int(id)
    query = "update queries set status = 'Closed', query_closed_time = NOW() where query_id = %s"
    cursor.execute(query, (id,))   
    conn.commit()
    cursor.close()
    conn.close()

# ---------- UI ----------
st.set_page_config(page_title="Login")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if not st.session_state.get("authenticated"):
    st.title("CLIENT QUERY MANAGEMENT SYSTEM")
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role=st.selectbox('Role',['Client','Support'])

    if st.button("Login"):
        if authenticate_user(username, password,role):
            st.success("Login successful!")
            
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.rerun()
        else:
            st.error("Invalid username or password")

# ---------- Protected Page ----------

def clear_text():
    create_query(st.session_state.get("username"), st.session_state.mobile_no,st.session_state.query_title, st.session_state.query_description)
    st.success("Query Submitted!")
    st.session_state.mobile_no = "" 
    st.session_state.query_title = ""
    st.session_state.query_description = ""

def view_table():
    username=st.session_state.get("username")
    view=get_query(username)
    df=pd.DataFrame(view)
    st.dataframe(df)
 
if st.session_state.get("authenticated"):

    col_left, col_mid, col_right = st.columns([4,1,1])

    with col_right:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
    
    st.subheader(f"Welcome, {st.session_state['username']} 👋")
    if st.session_state.get("role")=="Client":
        username=st.session_state.get("username")
        mobile_no=st.text_input("mobile_number",key="mobile_no")
        query_title=st.text_input("query_title",key="query_title")
        query_description=st.text_input("query_description",key="query_description")
        st.button("Submit", on_click=clear_text)
        view_table()
    
    elif st.session_state.get("role")=="Support":
        view=support_query()
        df=pd.DataFrame(view)
        event = st.dataframe(df, use_container_width=True, on_select="rerun")
        if event.selection.rows:
            selected_row = df.iloc[event.selection.rows[0]]

            @st.dialog("Query Details")
            def query_modal():
                id = 0
                for col, val in selected_row.items():
                    if col == "ID":
                        id = val
                    st.write(f"**{col}:** {val}")

                st.divider()

                if selected_row["Status"] == "Closed":
                    st.info("Ticket already closed")
                else:
                    if st.button("Close Ticket", type="primary"):
                        update_query(id)
                        st.success("Ticket closed successfully")
                        st.rerun()

            query_modal()
        
        
        


