from faker import Faker
import random
import sqlite3

conn = sqlite3.connect('some_db.db')
cursor = conn.cursor()

fake = Faker()
subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Literature', 'Geography']
groups = ['A', 'B', 'C']

for group in groups:
    cursor.execute("INSERT INTO groups (name) VALUES (?)", (group,))
conn.commit()

for i in range(7):
    cursor.execute("INSERT INTO teachers (name) VALUES (?)", (fake.name(),))
conn.commit()

for subject in subjects:
    teacher_id = random.randint(1, 7)
    cursor.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", (subject, teacher_id))
conn.commit()

for i in range(50):
    name = fake.name()
    group_id = random.randint(1, 3)
    cursor.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (name, group_id))
conn.commit()

for student_id in range(1, 51):
    for subject_id in range(1, 8):
        grade = random.randint(1, 12)  
        date = fake.date_this_year().isoformat()
        cursor.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)",
                       (student_id, subject_id, grade, date))
conn.commit()

conn.close()
