import streamlit as st 
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()  
    
    
 
        
#teacher dashboard    
def teacher_dashboard():
    teacher_data = st.session_state['teacher_data']
    st.header(f"""Welcome, {teacher_data['name']}""")
    

    
#login_teacher
def login_teacher(username,password):
    if not username or not password:
        return False
    teacher = teacher_login(username,password)
    if teacher:
        st.session_state['user_role'] = 'teacher'
        st.session_state['teacher_data'] = teacher
        st.session_state['is_logged_in'] = True
        return True


#teacher login screen       
def teacher_screen_login():
    col1,col2 = st.columns(2,gap="xxlarge")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
    st.markdown(
    "<h2 style='color:#31333F;text-align:center'>Login using password</h2>",
    unsafe_allow_html=True
    )
    st.space()
    st.space()
    teacher_username = st.text_input("enter username",placeholder="@anil")
    teacher_pass = st.text_input("Enter password",type="password",placeholder="enter your password")
    st.divider()
    btncol1,btncol2 = st.columns(2)
    with btncol1:
        if st.button("Login",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("Welcome back",icon="👋")
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid username & password")
    with btncol2:
        if st.button("Register instead",icon=":material/passkey:",width="stretch",type="primary"):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun() 
    footer_dashboard()


#register teacher
def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False,"All fields are required!"
    if check_teacher_exists(teacher_username):
        return False,"Username already exists!"
    if teacher_pass != teacher_pass_confirm:
        return False,"Password doesn't match"
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"Successfully Created! Login Now"
    except Exception as e:
        return False,"Unexcepted error"
            





#teacher register screen
def teacher_screen_register():
    col1,col2 = st.columns(2,gap="xxlarge")
    with col1:
        header_dashboard()
    with col2:
         if st.button("Go back to Home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
    st.markdown(
    "<h2 style='color:#31333F;text-align:center'>Register your teacher profile</h2>",
    unsafe_allow_html=True
    )
    
    teacher_username = st.text_input("Enter your username",placeholder="@anil")
    teacher_name = st.text_input("Enter your fullname",placeholder="Anil Sethy")
    teacher_pass = st.text_input("Enter your password",type="password",placeholder="enter your password")
    teacher_pass_confirm = st.text_input("Confirm your password",type="password",placeholder="enter confirm password")
    st.divider()
    btncol1,btncol2 = st.columns(2)
    with btncol1:
        if st.button("Register now",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            success,message = register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state['teacher_login_type'] = 'login'
                st.rerun()
            else:
                st.error(message)
           
    with btncol2:
        if st.button("Login instead",icon=":material/passkey:",width="stretch",type="primary"):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()
           
    footer_dashboard()
   
   