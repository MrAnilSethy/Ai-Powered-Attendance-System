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

# register teacher
def create_teacher(username,password,name):
    data = {"username":username,"password":hash_pass(password),"name":name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data
    
# login teacher   
def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
        else:
            return None
        
# all studnets
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

# create student
def create_student(new_name,face_embedding=None,voice_embedding=None):
    data = {'name':new_name,'face_embedding':face_embedding,'voice_embedding':voice_embedding}
    
    response = supabase.table("students").insert(data).execute()
    return response.data
    
# create subject
def create_subject(subject_code,name,section,teacher_id):
    data = {'subject_code':subject_code,'name':name,'section':section,'teacher_id':teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data
    
    
    
    
# get teacher subjects
def get_teacher_subjects(teacher_id):
    response = (
        supabase.table("subjects")
        .select("*,subject_students(count),attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for sub in subjects:

        sub["total_students"] = (
            sub["subject_students"][0]["count"]
            if sub.get("subject_students")
            else 0
        )

        attendance = sub.get("attendance_logs", [])

        unique_sessions = len(
            set(log["timestamp"] for log in attendance)
        )

        sub["total_classes"] = unique_sessions

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects
    
# Enroll Students
def enroll_student_to_subject(student_id,subject_id):
    data = {'student_id':student_id,'subject_id':subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data


# Un-enroll student
def unenroll_student_to_subject(student_id,subject_id):
    response = supabase.table("subject_students").delete().eq("student_id",student_id).eq("subject_id",subject_id).execute()
    return response.data
    

# get student subject
def get_student_subject(student_id):
    response = supabase.table("subject_students").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data

#get student attendance
def get_student_attendance(student_id):
    response = supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data


# craete attendance
def create_attendance(logs):
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data    
    
    
# attendance for teacher
def get_attendance_for_teacher(teacher_id):
    response = supabase.table("attendance_logs").select("*,subjects!inner(*)").eq("subjects.teacher_id",teacher_id).execute()
    return response.data