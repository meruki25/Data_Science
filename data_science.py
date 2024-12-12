import streamlit as st

pg = st.navigation([st.Page("datascience.py"), st.Page("streamlit_app.py")])
pg.run()
