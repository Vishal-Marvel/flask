import os
# sql = 'mysql://python:python_sql@localhost/users'
# sql = 'sqlite:///users.db'
sql = os.environ.get('DATABASE_URL')
# import os


# sql = os.getenv("DATABASE_URL")  # or other relevant config var
# if sql.startswith("postgres://"):
#     sql = sql.replace("postgres://", "postgresql://", 1)
    
# sql = 'postgresql://postgres:heuwvybzcpaylc:436dabaec96ed3f7688aac3b516195df24abf2436fb73923c95a8f21bbe6e774@ec2-34-205-209-14.compute-1.amazonaws.com:5432/d2nsrdqrqkcik7'
# sql = 'mysql://uboczaqyyznehlwt:gkDtUL1SFF5wnU9Du0MW@bmrujrdixbkkvxb3jjzx-mysql.services.clever-cloud.com/bmrujrdixbkkvxb3jjzx'

key = "my super secret key that no one is supposed to know"

u_name = 'autostock2021@gmail.com'
passw = 'cbkmcxxhswkwfxpd'

# https://www.youtube.com/watch?v=NYWEf9bZhHQ
# https://ckraczkowsky.medium.com/building-a-secure-admin-interface-with-flask-admin-and-flask-security-13ae81faa05
# https://www.youtube.com/watch?v=ysdShEL1HMM
# https://youtu.be/3rr3pGX7OsY?t=896