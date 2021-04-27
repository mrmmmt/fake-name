# -*- coding: utf-8 -*-
import sqlite3
import os


def add_info2db(lastname_dict, firstnameLst):
    if not os.path.exists('./fake.db'):
        flag = 0
    else:
        flag = 1

    conn = sqlite3.connect('./fake.db')  # 链接数据库，若数据库不存在则创建
    cursor = conn.cursor()

    if not flag:
        print('数据库不存在，开始创建数据库...')

        # 创建姓氏表 lastnames
        sql = '''
            CREATE TABLE lastnames (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lastname varchar(8) NOT NULL,
                weight int NOT NULL,
                UNIQUE(lastname)
            )
        '''
        cursor.execute(sql)

        # 创建名字表 firstnames
        sql = '''
            CREATE TABLE firstnames (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname varchar(8) NOT NULL,
                UNIQUE(firstname)
            )
        '''
        cursor.execute(sql)

        print('数据库创建完成')


    # 插入数据

    for lastname in lastname_dict.keys():
        try:
            sql = 'INSERT INTO lastnames ("lastname", "weight") VALUES ("{0}", {1})'.format(lastname, lastname_dict[lastname])
            cursor.execute(sql)
            print('insert lastname', lastname, 'success')
        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: lastnames.lastname':
                sql = 'UPDATE lastnames SET weight = {0} WHERE lastname = "{1}"'.format(lastname_dict[lastname], lastname)
                cursor.execute(sql)
                print('update lastname: {0}  weight: {1}'.format(lastname, lastname_dict[lastname]))
            else:
                print(e, lastname)

    for i in range(len(firstnameLst)):
        try:
            sql = 'INSERT INTO firstnames ("firstname") VALUES ("{0}")'.format(firstnameLst[i].strip())
            cursor.execute(sql)
            print('insert firstname', firstnameLst[i].strip(), 'success')
        except Exception as e:
            if str(e) != 'UNIQUE constraint failed: firstnames.firstname':
                print(e, firstnameLst[i].strip())

    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    lastname_dict = dict() 
    firstnameLst = []
    add_info2db(lastname_dict, firstnameLst)