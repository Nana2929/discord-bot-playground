from datetime import datetime
from dataclasses import dataclass
import os
import aiosqlite
from typing import List

from exceptions import *

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"

@dataclass
class DB:
    lcc = "leetcode_daily_challenge"
    sub = "ldc_subscription"

async def check_in(user_id: int) -> List:
    """
    This function will return
    """
    now = datetime.now()
    fetch_sql = "SELECT * FROM {DB.lcc} WHERE user_id = ?"
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(fetch_sql, (user_id, )) as cursor:
            rows = await cursor.fetchall()

    today = now.date()
    data = []
    for row in rows:
        date = row[-1]
        if date.date() >= today:
            raise DupCheckIn
        data.append(date.date())
    data.append(today)
    data.sort()
    consecutive = 1
    for i in range(len(data)-1, 0, -1):
        if (data[i] - data[i-1]).days == 1:
            consecutive += 1
        else:
            break

    push_sql = f''' INSERT INTO {DB.lcc} (user_id, report_time) VALUES (?, ?) '''
    async with db.execute(push_sql, (user_id, now)):
        await db.commit()
    return consecutive, len(data)




# def check_in(conn, name):
#     if conn is None:
#         return 0, 0, "db_error"

#     now = datetime.now()

#     sql = f'''SELECT * FROM {DB.lcc} WHERE member_name = %s '''
#     cursor = conn.cursor()
#     cursor.execute(sql, (name, ))
#     rows = cursor.fetchall()

#     today = now.date()
#     data = []
#     for row in rows:
#         date = row[-1]
#         if date.date() >= today:
#             return 0, 0, "duplicate_error"
#         data.append(date.date())
#     data.append(today)
#     data.sort()
#     consecutive = 1
#     for i in range(len(data)-1, 0, -1):
#         if (data[i] - data[i-1]).days == 1:
#             consecutive += 1
#         else:
#             break

#     sql = f''' INSERT INTO {DB.lcc} (member_name, report_time) VALUES (%s, %s) '''
#     cur = conn.cursor()
#     cur.execute(sql, (name, now))
#     conn.commit()
#     return consecutive, len(data), "checked_in"

# def subscribe(conn, name, remind_time, condemn_time):
#     if conn is None:
#         return 'db_error'

#     remind_time = (int(remind_time) - 8) % 24
#     condemn_time = (int(condemn_time) - 8) % 24

#     sql = f''' INSERT INTO {DB.sub} VALUES (%s, %s, %s) ON CONFLICT (member_name) DO UPDATE SET remind_time=%s, condemn_time=%s'''
#     cur = conn.cursor()
#     cur.execute(sql, (name, remind_time, condemn_time, remind_time, condemn_time))
#     conn.commit()
#     return 'subscribed'

# def unsubscribe(conn, name):
#     if conn is None:
#         return 'db_error'

#     sql = f''' DELETE FROM {DB.sub} WHERE member_name = %s '''
#     cur = conn.cursor()
#     cur.execute(sql, (name,))
#     conn.commit()
#     return 'unsubscribed'

# def get_remind_list(conn, mode):
#     if conn is None:
#         return [], 'db_error'

#     now = datetime.now()
#     now_hour = now.hour

#     sql = f'''SELECT * FROM {DB.sub} WHERE {'remind_time' if mode=='remind' else 'condemn_time'} = %s'''
#     cursor = conn.cursor()
#     cursor.execute(sql, (now_hour, ))
#     rows = cursor.fetchall()

#     names = tuple(row[0] for row in rows)
#     name_set = set(names)

#     if name_set:
#         sql = f'''SELECT member_name, MAX(report_time) FROM {DB.lcc} WHERE member_name in ({",".join(['%s']*len(names))}) group by member_name '''
#         cursor = conn.cursor()
#         cursor.execute(sql, names)
#         rows = cursor.fetchall()

#         for row in rows:
#             date = row[-1]
#             if date.date() == now.date() or (now_hour == 0 and date.date == now.date() - 1):
#                 name_set.remove(row[0])

#     return list(name_set), 'get_remind_list'
