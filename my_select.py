from sqlalchemy import func,desc
from models import Student, Group, Teacher, Subject, Grade
from models import Session



# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():

    session = Session()
    results = (
        session.query(Student.name, func.round(func.avg(Grade.grade), 2)
        .label('avg_grade'))
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .limit(5)
        .all()
    )
    return results

    
# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    session = Session()
    results = (
        session.query(Student)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    session.close()
    return f"{results}"

# Знайти середній бал у групах з певного предмета.
def select_3(subject_name):
    session = Session()
    results = (
        session.query(Group.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )
    session.close()
    return results

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    session = Session()
    results = (
        session.query(func.avg(Grade.grade).label('avg_grade'))
       .join(Student, Grade.student_id == Student.id)
       .join(Group, Student.group_id == Group.id)
       .first()
    )
    session.close()
    return results


# # Знайти які курси читає певний викладач.
def select_5(name_teacher):
    session = Session()
    results = (
        session.query(Subject)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.name.contains(name_teacher))
        .all()
    )
    session.close()
    subject_names = [str(subject) for subject in results]
    return subject_names

    
# Знайти список студентів у певній групі.
def select_6(group_name):
    session = Session()
    results = (
        session.query(Student)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .all()
    )
    students_name = [str(Student) for Student in results]
    return students_name

# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_name, subject_name):
    session = Session()
    results = (
        session.query(Grade)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .all()
    )
    session.close()
    results = [str(Grade) for Grade in results]
    return f"{results}"

# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_name):
    session = Session()
    result = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Teacher.id == Subject.teacher_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    session.close()
    return result
# Знайти список курсів, які відвідує певний студент.
def select_9(name_student):
    session = Session()
    result = (
        session.query(Subject)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.name == name_student)
        .all()
    )
    session.close()
    subject_names = [str(subject) for subject in result]
    return f"{subject_names}"
# Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    session = Session()
    result = (
        session.query(Subject)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.name == student_name)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    session.close()
    subject_names = [str(subject) for subject in result]
    return f"{subject_names}"
# Середній бал, який певний викладач ставить певному студентові.
def select_11(teacher_name, student_name):
    session = Session()
    result = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Teacher.name == teacher_name)
        .filter(Student.name == student_name)
        .scalar()
    )
    session.close()
    return result
# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(group_name, subject_name):
    session = Session()
    subquery = (
        session.query(func.max(Grade.date).label("max_date"))
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .subquery()
    )

    result = (
        session.query(Grade)
        .join(subquery, Grade.date == subquery.c.max_date)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .all()
    )
    results = [str(Grade) for Grade in result]
    return f"{results}"

if __name__ == "__main__":
    # result1 = select_1()
    # result2 = select_2("Mathematics")
    # result3 = select_3("Physics")
    # result4 = select_4()
    # result5 = select_5('Amanda Cochran')
    # result6 = select_6("A")
    # result7 = select_7("A","Mathematics")
    # result8 = select_8("Sheri Day")
    # result9 = select_9('Charles Bentley')
    # result10 = select_10('Nicholas Kim','James Price')
    # result11 = select_11('Jacqueline Garcia','Thomas Reeves')
    result12 = select_12("B","History")
    # print(result1)
    # print(result2)
    # print(result3)
    # print(result4)
    # print(result5)
    # print(result6)
    # print(result7)
    # print(result8)
    # print(result9)
    # print(result10)
    # print(result11)
    print(result12)


