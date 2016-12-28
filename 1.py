from sqlalchemy import create_engine
import os
# if os.path.exists("some.db"):
#     os.remove("some.db")
#e = create_engine("sqlite:///some.db")
# e.execute("""
#     create table employee (
#         user_id integer primary key,
#         user_len integer,
#         user_lon integer,
#         user_step integer
#     )
# """)
# e.execute("""insert into employee(user_len,user_lon) values (22,106)""")
# e.execute("""insert into employee(user_len,user_lon) values (22,105)""")
#e.execute("""insert into employee(user_len,user_lon) values (22.02,104)""")

# result = e.execute(
#             "select user_lon, user_len from "
#             "employee where user_id=:emp_id",
#             emp_id=3)
# row = result.fetchone()
# if row == None:
#     e.execute("""insert into employee(user_len,user_lon) values (22.02,104)""")
#     print(1)
# else:
#  print(row["user_len"])
