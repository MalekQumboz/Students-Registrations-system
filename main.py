import mariadb
import datetime
import calendar
from datetime import datetime ,timedelta
from random import random

conn=mariadb.connect(
    user="root",
    password="12345",
    host="localhost",
    database="student_registration"
)

cur=conn.cursor()


def registerStudent():
    print("To create the account:")
    name = input("Name:")
    BOD = input("birth of date ,As\'2021-01-12\':")
    country=input("Country:")
    city=input("City:")
    email=input("Email:")
    mobile_number = input("Mobile Number:")
    level = input("Level \" A-B-C\":")

    # Check entry level correctly
    if (level in ("A", "B", "C")):
        #insert contact
        query_contact = f"""insert into contacts (mobile_number,email) values('{mobile_number}','{email}');"""
        cur.execute(query_contact)
        contact_id = cur.lastrowid
        conn.commit()


        #insert address
        query_address = f"""insert into addreses (country,city) values('{country}','{city}');"""
        cur.execute(query_address)
        address_id = cur.lastrowid
        conn.commit()


        #select level ID
        query_level = f"""select level_id from levels where level_name= '{level}';"""
        cur.execute(query_level)
        data = tuple(cur)
        level_id = 0
        for i in data:
            level_id = i[0]
        #create student Id randomly
        student_id = int(random() * 100000)

        #insert student
        table_name = f"""students"""
        column_name = f"""student_id,student_name,BOD,contact_id,address_id,level_id"""
        valuse=f""" values("{student_id}","{name}","{BOD}",{contact_id},{address_id},{level_id}) """
        query_student = f"""insert into {table_name} ({column_name})  {valuse};"""
        cur.execute(query_student)
        conn.commit()


        print("Student Registered successfully.")
    else:
        print("level must be A,B or C, try again.. ")


def enrollCourse():
    print("To Enroll Course:")
    input_student_id = int(input("Student ID:"))

    #checking student id
    query_student_id = f"""select student_id,level_id from students where student_id= {input_student_id};"""
    cur.execute(query_student_id)
    data = tuple(cur)
    sudent_id=0
    level_student=0
    for i in data:
        sudent_id = i[0]
        level_student=i[1]

    key=0
    if(sudent_id!=0): # student exist or not in database
        key+=1
    else:
        print("The Student is not registered.")

    input_course_id = int(input("Course ID:"))

    # checking course id
    query_course_id = f"""select course_id,level_id from courses where course_id= {input_course_id};"""
    cur.execute(query_course_id)
    data = tuple(cur)
    course_id = 0
    level_course=0
    for i in data:
        course_id = i[0]
        level_course=i[1]

    if (course_id!=0): # course exist or not in database
        key+=1
    else:
        print("The Course dose not exist.")

    if(key==2):
        # checking level of the student is similar to the level of the course
        if(level_course==level_student):
            # checking student registered in the course or not
            query_enroll_history = f"""select course_id from enrollment_histories where student_id= {input_student_id};"""
            cur.execute(query_enroll_history)
            data = tuple(cur)
            course_id_list=()
            for i in data:
                course_id_list=i
            # checking student registered in the course or not
            if(input_course_id  not in course_id_list):
                # checking the course is full or not
                #find number of student in course
                query_student_count=f"""select count(student_id) from enrollment_histories where course_id={input_course_id};"""
                cur.execute(query_student_count)
                data = tuple(cur)
                student_no=0
                for i in data:
                    student_no = i[0]
                #find max capacity for course
                query_max_capcity=f"""select max_capacity from courses where course_id={input_course_id}"""
                cur.execute(query_max_capcity)
                data = tuple(cur)
                max_capacity=-1
                for i in data:
                    max_capacity = i[0]

                if(student_no<max_capacity):
                    # enroll course
                    enroll_date=datetime.datetime.now()

                    query_total=f""" select (total_hours*rate_per_hour) from courses where course_id={input_course_id} """
                    cur.execute(query_total)
                    data = tuple(cur)
                    total = 0
                    for i in data:
                        total = i[0]

                    table_name = f"""enrollment_histories"""
                    column_name = f"""student_id,course_id,enroll_date,total"""
                    valuse = f""" values({input_student_id},{input_course_id},'{enroll_date}',{total}) """
                    query_enrollment_history = f"""insert into {table_name} ({column_name})  {valuse};"""
                    cur.execute(query_enrollment_history)
                    conn.commit()
                    print("Enroll Course successfully.")
                else:
                    print("Sorry, Course capacity full.")
            else:
                print("The Student is already registered in the course.")
        else:
            print("The current level of the student is \n not compatible with the level of the course.")
    else:
        pass


def createNewCourse():
    print("To create Course:")
    course_id = input("Course ID:")
    course_name = input("Course Name:")
    level = input("Level \" A-B-C\":")
    max_capacity = int(input("Capacity:"))
    rate_per_hour = float(input("Hour Rate \"price\":"))
    total_hours=int(input("Total Hours:"))

    if (level in ("A", "B", "C")):

        # select level ID
        query_level = f"""select level_id from levels where level_name= '{level}';"""
        cur.execute(query_level)
        data = tuple(cur)
        level_id = 0
        for i in data:
            level_id = i[0]

        # insert course
        table_name = f"""courses"""
        column_name = f"""course_id,course_name,level_id,max_capacity,rate_per_hour,total_hours"""
        valuse = f""" values("{course_id}","{course_name}",{level_id},{max_capacity},{rate_per_hour},{total_hours}) """
        query_course = f"""insert into {table_name} ({column_name})  {valuse};"""
        cur.execute(query_course)
        conn.commit()
        print("Created course successfully.")

    else:
        print("level must be A,B or C, try again.. ")

def createCourseSchedule():
    print("To create Course Schedule:")

    day_input=input("Select Day:")

    #check day spelling correctly.
    correctly=False
    day_input=day_input.lower()
    for i in range (1,7):
        day=calendar.day_name[i]
        day=day.lower()
        if(day==day_input):
            correctly=True

    if(correctly==True): # check day spelling correctly.

        # checking course id exist or not in database
        input_course_id = int(input("Course ID:"))
        query_course_id = f"""select course_id from courses where course_id= '{input_course_id}';"""
        cur.execute(query_course_id)
        data = tuple(cur)
        course_id = 0
        for i in data:
            course_id = i[0]

        if (course_id != 0):  # course exist or not in database
            # checking course scheduled or not
            query_course_id = f"""select course_id from courses_schedule where course_id ={input_course_id}"""
            cur.execute(query_course_id)
            data = tuple(cur)
            course_id = 0
            for i in data:
                course_id = i[0]
            if(course_id == 0):   #checking course scheduled or not => if=0 mean not schedule
                # insert schedule details
                input_start_time = input("Start time, As\'16:00:00\':")
                input_duration = int(input("Duration:"))

                #change str type to time
                temp_start_time=datetime.strptime(input_start_time, '%H:%M:%S')
                input_end_time= temp_start_time + timedelta(hours=input_duration)
                end_time=input_end_time.time()
                input_start_time=datetime.strptime(input_start_time, '%H:%M:%S').time()

                # find level_id for course
                query_level_id = f"""select level_id from courses where course_id= '{input_course_id}';"""
                cur.execute(query_level_id)
                data = tuple(cur)
                level_id = 0
                for i in data:
                    level_id = i[0]

                # find course he has seam level
                query_course_id = f"""(select course_id from courses where level_id= {level_id})"""

                # find days and start time and end time for courses in the same level.
                query_course_schedule_id = f"""select count(course_schedule_id) from courses_schedule 
                                                where (course_id in ({query_course_id})) and day ='{day_input}' and start_time = '{input_start_time}'
                                                and '{end_time}'in (select date_add(start_time,interval duration hour ) from courses_schedule);"""
                cur.execute(query_course_schedule_id)
                data = tuple(cur)
                count=0
                for i in data:
                    count=i[0]

                if (count==0):
                    # insert schedule details
                    table_name = f"""courses_schedule"""
                    column_name = f"""course_id,day,duration,start_time"""
                    values = f""" values({input_course_id},'{day_input}','{input_duration}','{input_start_time}') """
                    query_course_schedule = f"""insert into {table_name} ({column_name})  {values};"""
                    cur.execute(query_course_schedule)
                    conn.commit()
                    print("Scheduled Course successfully.")
                else:
                    print("The appointment is already booked for anther course.")
            else:
                print("Sorry, the course has been scheduled before.")
        else:
            print("The Course dose not exist.")
    else:
        print("Check day spelling correctly , try again..")


def displayStudentSchedule():
    print("To Display Student Schedule:")
    input_student_id=int(input("Student ID:"))

    # checking student id
    query_student_id = f"""select count(student_id) from students where student_id= '{input_student_id}';"""
    cur.execute(query_student_id)
    data = tuple(cur)
    sudent_id = 0
    for i in data:
        sudent_id = i[0]

    if (sudent_id != 0):  # student exist or not in database
        # display course_id from enrollment_histories
        query_course_id = f"""select course_id from enrollment_histories where student_id={input_student_id};"""
        cur.execute(query_course_id)
        data = tuple(cur)
        course_id_tuple = (-1,-2,)
        for i in data:
            course_id_tuple += i
        #count_course_scheduled
        query_count_course_schedule = f"""select count(course_schedule_id) from courses_schedule where course_id in {course_id_tuple};"""
        cur.execute(query_count_course_schedule)
        data = tuple(cur)
        count=0
        for i in data:
            count= i[0]

        if(count !=0):
            # display student schedule
            query_display_course_id = f"""select course_id from enrollment_histories where student_id={input_student_id};"""
            cur.execute(query_display_course_id)
            data = tuple(cur)
            course_id_tuple = (-1,-2,)
            for i in data:
                course_id_tuple += i
            # display courses
            column = f"""course_id,day,duration,start_time"""
            query_display_course = f"""select {column} from courses_schedule where course_id in {course_id_tuple};"""
            cur.execute(query_display_course)
            data = tuple(cur)
            print("\nStudent Schedule:")
            for course_id, day, duration, start_time in data:
                print(f"""course ID: {course_id} \tDay: {day} \tStart time: {start_time} \tDuration: {duration} """)
        else:
            print("The student has not registered for courses yet.")
    else:
        print("The Student is not registered.")

loop=True
while (loop==True):
    print("""
    1-Register New Student.
    2-Enroll Course.
    3-Create New Course.
    4-Create New Schedule.
    5-Display Student Course schedule.
    6-Exit.""")
    try:
        input_1 = int(input("     Enter the service number:"))

        if input_1 == 1:        # Register new Student.
            registerStudent()

        elif input_1 == 2:      # Enroll Course.
            enrollCourse()

        elif input_1 == 3:      # Create New Course.
           createNewCourse()

        elif input_1 == 4:      # Create New Schedule.
            createCourseSchedule()

        elif input_1 == 5:      # Display Student Course schedule.
            displayStudentSchedule()

        elif input_1 == 6:      # To Exit.
            loop=False
            print("exit successfully.")

        else:
            print("Out of range...")

    except:
        print("Wrong entry, please try again..")