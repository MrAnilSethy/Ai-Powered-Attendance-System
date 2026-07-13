import streamlit as st 
#header for homescreen
def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
                <div style='display:flex;flex-direction:column;align-items:center;margin-top:10px;'>
                <img src='{logo_url}' style='height:100px' />
                <h1 style='text-align:center;color:#E0E3FF;'>SNAP<br/>CLASS</h1>
                </div>
                """,unsafe_allow_html=True)
    
    
#header for dashboard  
def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;'>
                <img src='{logo_url}' style='height:85px' />
                <h2 style='text-align:center;color:#5865F2;'>SNAP<br/>CLASS</h2>
                </div>
                """,unsafe_allow_html=True)