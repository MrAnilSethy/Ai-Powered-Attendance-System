import streamlit as st
def footer_home():
    logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcddc1q1Gs_qunyVsxEK0-KctBGxZniChx5GPzsGHCcw&s=10"
    st.markdown(f"""
                <div style='margin-top:2rem;display:flex;gap:6px;justify-content:center;items-align:center';>
                    <p style='font-weight:bold;color:white'>Created with ❤️ by </p>
                    <img src='{logo_url}'style='max-height:25px;border-radius:5rem' />
                </div>
                """,unsafe_allow_html=True)
    
def footer_dashboard():
    logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcddc1q1Gs_qunyVsxEK0-KctBGxZniChx5GPzsGHCcw&s=10"
    st.markdown(f"""
                <div style='margin-top:2rem;display:flex;gap:6px;justify-content:center;items-align:center';>
                    <p style='font-weight:bold;color:black'>Created with ❤️ by </p>
                    <img src='{logo_url}'style='max-height:25px;border-radius:5rem' />
                </div>
                """,unsafe_allow_html=True)