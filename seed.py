import argparse
from models import Student,Group,Teacher,session,create_engine

# create
def create_teacher(new_name):
    new_teacher = Teacher(name=new_name)
    session.add(new_teacher)
    session.commit()
def create_group(new_name):
    new_group = Group(name=new_name)
    session.add(new_group)
    session.commit()
def create_student(new_name):
    new_student = Student(name=new_name)
    session.add(new_student)
    session.commit() 

# list all teacher,student or group
def all_teacher():
    teachers_names = session.query(Teacher.name).all()
    for name in teachers_names:
        print(name)
def all_group():
    groups_names = session.query(Group.name).all()
    for name in groups_names:
        print(name)
def all_student():
    students_names = session.query(Student.name).all()
    for name in students_names:
        print(name)
# update
def update_teacher(id,name):
    teacher_to_update = session.query(Teacher).filter_by(id=id).first()
    teacher_to_update.name = name
    session.commit()
def update_student(id,name):
    student_to_update = session.query(Student).filter_by(id=id).first()
    student_to_update.name = name
    session.commit()
def update_group(id,name):
    group_to_update = session.query(Group).filter_by(id=id).first()
    group_to_update.name = name
    session.commit()
# delete
def remove_teacher(id):
    teacher_to_remove = session.query(Teacher).filter_by(id=id).first()
    session.delete(teacher_to_remove)
    session.commit()
def remove_student(id):
    student_to_remove = session.query(Student).filter_by(id=id).first()
    session.delete(student_to_remove)
    session.commit()
def remove_group(id):
    group_to_remove = session.query(Group).filter_by(id=id).first()
    session.delete(group_to_remove)
    session.commit()


def main():
    parser = argparse.ArgumentParser(description='CLI програма для CRUD операцій з базою даних')

    parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'],
                        help='Дія: create, list, update або remove')
    parser.add_argument('--model', '-m', choices=['Teacher', 'Student', 'Group'],
                        help='Модель: Teacher, Student або Group')
    parser.add_argument('--id', type=int, help='ID запису (для оновлення або видалення)')
    parser.add_argument('--name', help='Ім\'я запису (для створення або оновлення)')

    args = parser.parse_args()

    if args.action == 'create':
        if args.model == 'Teacher':
            create_teacher(args.name)
        elif args.model == 'Student':
            create_student(args.name)
        elif args.model == 'Group':
            create_group(args.name)
    elif args.action == 'list':
        if args.model == 'Teacher':
            all_teacher()
        elif args.model == 'Student':
            all_student()
        elif args.model == 'Group':
            all_group()
    elif args.action == 'update':
        if args.model == 'Teacher':
            update_teacher(args.id, args.name)
        elif args.model == 'Student':
            update_student(args.id, args.name)
        elif args.model == 'Group':
            update_group(args.id, args.name)
    elif args.action == 'remove':
        if args.model == 'Teacher':
            remove_teacher(args.id)
        elif args.model == 'Student':
            remove_student(args.id)
        elif args.model == 'Group':
            remove_group(args.id)
    else:
        print("Неправильно вказана дія або модель")


if __name__ == '__main__':
    engine = create_engine('sqlite:///some_db.db') 
    main()
