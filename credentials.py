import os
sql = 'sqlite:///users.db'

if sql.startswith("postgres://"):
    sql = sql.replace("postgres://", "postgresql://", 1)

key = "my super secret key that no one is supposed to know"

u_name = 'autostock2021@gmail.com'
passw = 'cbkmcxxhswkwfxpd'

# https://www.youtube.com/watch?v=NYWEf9bZhHQ
# https://ckraczkowsky.medium.com/building-a-secure-admin-interface-with-flask-admin-and-flask-security-13ae81faa05
# https://www.youtube.com/watch?v=ysdShEL1HMM
# https://youtu.be/3rr3pGX7OsY?t=896