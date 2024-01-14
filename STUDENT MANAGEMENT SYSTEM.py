import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Function Definitions

def print_welcome_note():
    print("""
    ================================================================================
               WELCOME TO BUNNY'S STUDENT MANAGEMENT SYSTEM
    ================================================================================
    """)

def create_database_connection(password):
    return mysql.connector.connect(host="localhost", user="root", passwd=password, database="stud_manage")

def check_courses(cursor, db):
    cursor.execute("SELECT * FROM COURSES")
    data = cursor.fetchall()
 
    if len(data) == 0:
        courses_table(cursor, db)
    else:
        pass
    
def courses_table(cursor, db):
    cursor.execute("INSERT INTO COURSES VALUES (201,\"Python and C\")")
    cursor.execute("INSERT INTO COURSES VALUES (208,\"Data Structures and Algorithm \")")
    cursor.execute("INSERT INTO COURSES VALUES (215,\"Security and Cyber Laws\")")
    cursor.execute("INSERT INTO COURSES VALUES (211,\"Discrete Mathematics\")")
    cursor.execute("INSERT INTO COURSES VALUES (212,\"Software Engineering\")")
    cursor.execute("INSERT INTO COURSES VALUES (213,\"Professional Skills and Ethics\")")
    cursor.execute("INSERT INTO COURSES VALUES (214,\"Design and Analysis of Algorithm\")")
    db.commit()

def create_tables(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS courses (course_id INT PRIMARY KEY, course_name VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS grades (student_id INT, course_id INT, grade INT)")

def add_student(cursor, student_data):
    cursor.execute("SELECT NAME, AGE FROM STUDENTS")
    data = cursor.fetchall()
    flag = 0
    for name, age in data:
        if name == student_data[0] and age == student_data[1]:
            flag = 1
            print("\nSTUDENT ALREADY EXIST.")
    if flag == 0:
        cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", student_data)
        print("\nSTUDENT ADDED SUCCESSFULLY.")

def update_student(cursor, student_id, updated_data):
    cursor.execute("SELECT ID FROM STUDENTS")
    data = cursor.fetchall()

    flag = 0
    for s_id in data:
        if str(s_id[0]) == student_id:
            flag = 1
            cursor.execute("UPDATE students SET name=%s, age=%s WHERE id=%s", (updated_data['name'], updated_data['age'], student_id))
            print("\nUPDATED SUCCESSFULLY.")
    if flag == 0:
        print("\nINVALID STUDENT ID.")

def delete_student(cursor, student_id):
    cursor.execute("SELECT ID FROM STUDENTS")
    data = cursor.fetchall()
    flag = 0
    for s_id in data:
        if str(s_id[0]) == student_id:
            flag = 1
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            print("\nDELETED SUCCESSFULLY.")
    if flag == 0:
        print("\nINVALID STUDENT ID.")

def get_student_data(cursor, student_id):
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    data = cursor.fetchall()
    cols = ["ID", "NAME", "AGE"]
    df = pd.DataFrame(data, columns = cols)
    print("\n")
    print(df)

def list_all_students(cursor):
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cols = ["ID", "NAME", "AGE"]
    df = pd.DataFrame(data, columns = cols)
    print("\n")
    print(df)
    
    return cursor.fetchall()

def assign_grade(cursor, student_id, course_id, grade):
    cursor.execute("SELECT STUDENT_ID, COURSE_ID FROM GRADES")
    data = cursor.fetchall()
    flag = 0
    for s_id, c_id in data:
        if str(s_id) == student_id and str(c_id) == course_id:
            flag = 1
            print("\nGRADES ALREADY ASSIGNED.")
            break
    if flag == 0:
        cursor.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s)", (student_id, course_id, grade))
        print("\nGRADES ASSIGNED SUCCESSFULLY.")

def update_grade(cursor, student_id, course_id, grade):
    cursor.execute("SELECT STUDENT_ID, COURSE_ID FROM GRADES")
    data = cursor.fetchall()
    flag = 0
    for s_id, c_id in data:
        if str(s_id) == student_id and str(c_id) == course_id:
            flag = 1
            cursor.execute("UPDATE grades SET grade=%s WHERE student_id=%s AND course_id=%s", (grade, student_id, course_id))
            print("\nUPDATED SUCCESSFULLY.")
    if flag == 0:
        print("\nINVALID STUDENT OR COURSE ID.")

def generate_report(cursor):
    s_id = int(input("ENTER STUDENT ID:"))
    cursor.execute("SELECT ID, NAME FROM STUDENTS")
    stu_ids = cursor.fetchall()
    flag = 0
    for stu_id in stu_ids:
        if stu_id[0] == s_id:
            flag = 1
            cursor.execute(f"SELECT C.COURSE_NAME, G.GRADE from COURSES C, GRADES G WHERE C.COURSE_ID = G.COURSE_ID AND G.STUDENT_ID = '{s_id}'")
            data = cursor.fetchall()

            if len(data) == 0:
                print("\nSORRY... NO DATA.")
            else:
                df = pd.DataFrame(data, columns=['Course', 'Grade'])
                print("\n\t\t" + stu_id[1].upper() + "\'s REPORT")
                print(df)
                df.plot(kind='bar', x='Course', y='Grade')
                plt.title(stu_id[1].upper())
                plt.ylabel("GRADES")
                plt.xlabel("COURSES")
                plt.xticks(rotation=9, fontsize = 8)
                plt.show()
           
    if flag == 0:
        print("\nINVALID STUDENT ID.")
        

def print_main_menu():
    print("\nMain Menu")
    print("1. Manage Students")
    print("2. Manage Grades")
    print("3. Generate Reports")
    print("4. Exit")

def manage_students(cursor):
    while True:
        print("\n--- Manage Students ---")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. View Student Details")
        print("5. List All Students")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == '1':
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            add_student(cursor, (name, age))
        elif choice == '2':
            student_id = input("Enter student ID to update: ")
            name = input("Enter new name: ")
            age = input("Enter new age: ")
            update_student(cursor, student_id, {'name': name, 'age': age})
        elif choice == '3':
            student_id = input("Enter student ID to delete: ")
            delete_student(cursor, student_id)
        elif choice == '4':
            student_id = input("Enter student ID: ")
            print("\nStudent Details:")
            get_student_data(cursor, student_id)
            
        elif choice == '5':
            students = list_all_students(cursor)
            for student in students:
                print(student)
        elif choice == '6':
            break


def manage_grades(cursor):
    while True:
        print("\n--- Manage Grades ---")
        print("1. Assign Grade")
        print("2. Update Grade")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")
        cursor.execute("SELECT * FROM COURSES")
        data = cursor.fetchall()
        cols = ["COURSE ID", "COURSES"]
        df = pd.DataFrame(data, columns = cols)
        print("\n")
        print(df)
        if choice == '1':
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID: ")
            grade = input("Enter grade (OUT OF 10): ")
            assign_grade(cursor, student_id, course_id, grade)
        elif choice == '2':
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID: ")
            grade = input("Enter new grade: ")
            update_grade(cursor, student_id, course_id, grade)
            print(f"Grade: {grade}")
        elif choice == '3':
            break

def main():
    db_connection = create_database_connection("root")  # Replace with your actual password
    cursor = db_connection.cursor(buffered = True)

    create_tables(cursor)
    check_courses(cursor, db_connection)

    while True:
        print_main_menu()
        choice = input("\nEnter your choice: ")

        if choice == '1':
            manage_students(cursor)
        elif choice == '2':
            manage_grades(cursor)
        elif choice == '3':
            generate_report(cursor)
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

        db_connection.commit()

    db_connection.close()

if __name__ == "__main__":
    main()
