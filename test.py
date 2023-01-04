import mariadb
import json
from flask import *
import jinja2

conn=mariadb.connect(
    user="root",
    password="12345",
    host="localhost",
    database="student_registration"
)

cur=conn.cursor()


app = Flask(__name__,template_folder='templates')



@app.route('/courses')
def get_all_course():
    query_courses = f"""select * from courses"""
    cur.execute(query_courses)
    data = tuple(cur)

    list_of_course = []

    for course_id, level_id, course_name, max_capacity, rate_per_hour, total_hours in data:
        courses = {
            "course_id": course_id,
            "level_id": level_id,
            "course_name": course_name,
            "max_capacity": max_capacity,
            "rate_per_hour": rate_per_hour,
            "total_hours": total_hours,
        }
        list_of_course.append(courses)

    #find level from database
    query_level = f"""select * from levels"""
    cur.execute(query_level)
    data = tuple(cur)

    list_of_level = []
    for level_id, level_name in data:
        levels = {
            "level_id": level_id,
            "level_name": level_name
        }
        list_of_level.append(levels)

    context={}
    context['title'] = "Courses"
    context['levels'] =list_of_level
    context['courses'] =list_of_course

    return render_template("courses.html",**context)


@app.route("/students")
def get_all_student():
    #find student from database
    query_student = f"""select * from students"""
    cur.execute(query_student)
    data = tuple(cur)

    list_of_student = []
    for student_id, student_name, contact_id, address_id, level_id, BOD in data:
        students = {
            "student_id": student_id,
            "student_name": student_name,
            "contact_id": contact_id,
            "address_id": address_id,
            "level_id": level_id,
            "BOD": BOD,
        }
        list_of_student.append(students)

    #find level from database
    query_level = f"""select * from levels"""
    cur.execute(query_level)
    data = tuple(cur)

    list_of_level = []
    for level_id, level_name in data:
        levels = {
            "level_id": level_id,
            "level_name": level_name
        }
        list_of_level.append(levels)

    #find contact from database
    query_contact = f"""select * from contacts"""
    cur.execute(query_contact)
    data = tuple(cur)

    list_of_contact = []
    for contact_id, mobile_number,email in data:
        contacts = {
            "contact_id": contact_id,
            "mobile_number": mobile_number,
            "email": email
        }
        list_of_contact.append(contacts)

    #find address from database
    query_address = f"""select * from addreses"""
    cur.execute(query_address)
    data = tuple(cur)

    list_of_address = []
    for address_id, country, city in data:
        address = {
            "address_id": address_id,
            "country": country,
            "city": city
        }
        list_of_address.append(address)

    context = {}
    context['title'] = "Students"
    context['students'] = list_of_student
    context['levels'] = list_of_level
    context['contacts'] = list_of_contact
    context['addreses'] = list_of_address
    return render_template("students.html",**context)


@app.route("/course-schedule")
def get_all_course_schedule():
    query_course_schedule = f"""select * from courses_schedule"""
    cur.execute(query_course_schedule)
    data = tuple(cur)

    list_of_course_schedule = []

    for course_schedule_id, course_id, day, duration, start_time in data:
        courses_schedule = {
            "course_schedule_id": course_schedule_id,
            "course_id": course_id,
            "day": day,
            "duration": duration,
            "start_time": f'{start_time}'
        }
        list_of_course_schedule.append(courses_schedule)


    #find course from database
    query_courses = f"""select * from courses"""
    cur.execute(query_courses)
    data = tuple(cur)

    list_of_course = []

    for course_id, level_id, course_name, max_capacity, rate_per_hour, total_hours in data:
        courses = {
            "course_id": course_id,
            "level_id": level_id,
            "course_name": course_name,
            "max_capacity": max_capacity,
            "rate_per_hour": rate_per_hour,
            "total_hours": total_hours,
        }
        list_of_course.append(courses)

    context = {}
    context['title'] = "Course Schedule"
    context['courses'] = list_of_course
    context['course_schedules'] = list_of_course_schedule
    return render_template("course_schedules.html",**context)




@app.route('/studentdetails/<int:id>',methods=['get'])
def student_details(id):
    context = {}
    # find student from database
    query_student = f"""select * from students"""
    cur.execute(query_student)
    data = tuple(cur)
    list_of_student = []

    for student_id, student_name, contact_id, address_id, level_id, BOD in data:
        if (id == student_id):
            student = {
                "student_id": student_id,
                "student_name": student_name,
                "contact_id": contact_id,
                "address_id": address_id,
                "level_id": level_id,
                "BOD": BOD,
            }
            list_of_student.append(student)
            context['status'] = True
            context['code'] = 200
            context['message'] = "completed successfully"
            break
        else:
            context['status'] = False
            context['code'] = 401
            context['message'] = "Not exist"

    context['data']=list_of_student

    return jsonify(context)



app.run(debug=True)
