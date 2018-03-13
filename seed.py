cofrom app import db, Student

db.create_all()

s1 = Student(first_name='Elie', last_name='Schoppik')
s2 = Student(first_name='Matt', last_name='Lane')
s3 = Student(first_name='Michael', last_name='Hueter')
s4 = Student(first_name='Joel', last_name='Burton')

db.session.add(s1)
db.session.add(s2)
db.session.add(s3)
db.session.add(s4)
db.session.commit()