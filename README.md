A Streamlit-based web application for managing client support queries with role-based access. Clients can raise queries and track their status, while support staff can 
view, manage and close queries stored in a MySQL database.
--------------------------------------------
--- Client ----
  Secure login with hashed passwords
  Submit new support queries
  View submitted queries and their status (Open / Closed)
---- Support ----
  View all client queries
  See detailed query information
  Close queries and automatically record resolution time
---- System ----
  Role-based authentication (Client / Support)
  MySQL database integration
  Query duration tracking
  Interactive UI built with Streamlit
--------------------------------------------
---- Tech Stack ----
Frontend: Streamlit
Backend: Python
Database: MySQL
Libraries: streamlit, mysql-connector-python, pandas, hashlib
--------------------------------------------


