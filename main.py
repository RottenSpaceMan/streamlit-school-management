import streamlit as st

st.set_page_config(page_title="School Management System", layout="wide")

from supabase import create_client, Client

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

def fetch_all_data(table_name):
    return supabase.table(table_name).select("*").execute().data

def insert_data(table_name, data_dict):
    return supabase.table(table_name).insert(data_dict).execute()

def update_data(table_name, row_id, data_dict):
    return supabase.table(table_name).update(data_dict).eq('id', row_id).execute()

def delete_data(table_name, row_id):
    return supabase.table(table_name).delete().eq('id', row_id).execute()

def manage_students():
    st.header("Manage Students")
    st.subheader("Current Student Roster")
    students = fetch_all_data("students")
    if students:
        student_options = {s['id']: f"{s['first_name']} {s['last_name']} (Grade: {s['grade_level']})" for s in students}
        if students:
            formatted_students = [
                {
                    "ID": s["id"],
                    "Created At": s["created_at"].split("T")[0],  # Extract only the date part
                    "First Name": s["first_name"],
                    "Last Name": s["last_name"],
                    "Date of Birth": s["date_of_birth"],
                    "Grade Level": s["grade_level"]
                }
                for s in students
            ]
            st.dataframe(formatted_students)
    else:
        st.info("No students found.")
        student_options = {}
    
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add New Student")
        with st.form("add_student_form", clear_on_submit=True):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            date_of_birth = st.date_input("Date of Birth", min_value="1990-01-01")
            grade_level = st.number_input("Grade Level", min_value=1, max_value=12, step=1)
            submitted = st.form_submit_button("Add Student")

            if submitted:
                if first_name and last_name:
                    new_student = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": str(date_of_birth),
                        "grade_level": grade_level
                    }

                    insert_data("students", new_student)
                    st.success("Student added successfully!")
                    st.rerun()
                else:
                    st.error("First name and Last name are required.")
    with col2:
        st.subheader("Update or Delete Student")
        if student_options:
            selected_student_id = st.selectbox("Select Student", options=list(student_options.keys()), format_func=lambda x: student_options[x])
            selected_student_data = next((s for s in students if s['id'] == selected_student_id), None)

            if selected_student_data:
                with st.form("update_student_form"):
                    st.write(f"**Updating** {selected_student_data['first_name']} {selected_student_data['last_name']}")
                    updated_first_name = st.text_input("First Name", value=selected_student_data['first_name'])
                    updated_last_name = st.text_input("Last Name", value=selected_student_data['last_name'])
                    updated_date_of_birth = st.date_input("Date of Birth", value=selected_student_data['date_of_birth'])
                    updated_grade_level = st.number_input("Grade Level", min_value=1, max_value=12, step=1, value=selected_student_data['grade_level'])
                    update_button = st.form_submit_button("Update Student")
                    if update_button:
                        update_payload = {
                            "first_name": updated_first_name,
                            "last_name": updated_last_name,
                            "date_of_birth": str(updated_date_of_birth),
                            "grade_level": updated_grade_level
                        }
                        update_data("students", selected_student_id, update_payload)
                        st.success("Student updated successfully!")
                        st.rerun()
                if st.button("Delete Student", key=f"delete_{selected_student_id}"):
                    delete_data("students", selected_student_id)
                    st.warning("Student deleted successfully!")
                    st.rerun()
        else:
            st.info("Add a student to update or delete.")

def manage_teachers():
    st.header("Manage Teachers")
    st.subheader("Current Teacher Roster")
    teachers = fetch_all_data("teachers")
    if teachers:
        teacher_options = {s['id']: f"{s['first_name']} {s['last_name']} (Subject: {s['subject_specialty']})" for s in teachers}
        if teachers:
            formatted_teachers = [
            {
                "ID": t["id"],
                "Created At": t["created_at"].split("T")[0],  # Extract only the date part
                "First Name": t["first_name"],
                "Last Name": t["last_name"],
                "Subject Specialty": t["subject_specialty"]
            }
            for t in teachers
            ]
            st.dataframe(formatted_teachers)
    else:
        st.info("No teachers found.")
        teacher_options = {}
    
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add New Teacher")
        with st.form("add_teacher_form", clear_on_submit=True):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            subject_specialty = st.text_input("Subject Specialty")
            submitted = st.form_submit_button("Add Teacher")

            if submitted:
                if first_name and last_name:
                    new_teacher = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "subject_specialty": subject_specialty
                    }

                    insert_data("teachers", new_teacher)
                    st.success("Teacher added successfully!")
                    st.rerun()
                else:
                    st.error("First name and Last name are required.")
    with col2:
        st.subheader("Update or Delete Teacher")
        if teacher_options:
            selected_teacher_id = st.selectbox("Select Teacher", options=list(teacher_options.keys()), format_func=lambda x: teacher_options[x])
            selected_teacher_data = next((t for t in teachers if t['id'] == selected_teacher_id), None)

            if selected_teacher_data:
                with st.form("update_teacher_form"):
                    st.write(f"**Updating** {selected_teacher_data['first_name']} {selected_teacher_data['last_name']}")
                    updated_first_name = st.text_input("First Name", value=selected_teacher_data['first_name'])
                    updated_last_name = st.text_input("Last Name", value=selected_teacher_data['last_name'])
                    updated_subject_speciality = st.text_input("Subject Specialty", value=selected_teacher_data['subject_specialty'])
                    update_button = st.form_submit_button("Update Teacher")
                    if update_button:
                        update_payload = {
                            "first_name": updated_first_name,
                            "last_name": updated_last_name,
                            "subject_specialty": updated_subject_speciality
                        }
                        update_data("teachers", selected_teacher_id, update_payload)
                        st.success("Teacher updated successfully!")
                        st.rerun()
                if st.button("Delete Teacher", key=f"delete_{selected_teacher_id}"):
                    delete_data("teachers", selected_teacher_id)
                    st.warning("Teacher deleted successfully!")
                    st.rerun()
        else:
            st.info("Add a teacher to update or delete.")


st.title("School Management System")
st.write("Manage students and teachers in your school.")

page = st.sidebar.radio("Select Page", ("Manage Students", "Manage Teachers"))

if page == "Manage Students":
    manage_students()
if page == "Manage Teachers":
    manage_teachers()