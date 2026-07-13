from src.database.config import supabase
import bcrypt

def check_pass(pwd,hased):
    return bcrypt.checkpw(pwd.encode(),hased.encode())
    



def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()



#check teacher username already taken or not
def check_teacher_exists(username):
    #check username return false if username already taken
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0


def create_teacher(username,password,name):
    data = {"username":username,"password":hash_pass(password),"name":name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data
    
    
def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
        else:
            return None
        
#all studnets
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data