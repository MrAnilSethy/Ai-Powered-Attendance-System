import streamlit as st 
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
    match st.session_state['login_type']:
        case 'teacher':
            st.session_state['login_type'] = 'teacher'
            teacher_screen()
        case 'student':
            st.session_state['login_type'] = 'student'
            student_screen()
        case None:
            st.session_state['login_type'] = None
            home_screen()
            
main()