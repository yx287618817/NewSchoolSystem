
# -*- coding: utf-8 -*-
# @Time    : 2019-05-22 08:45
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : SQL即查即用.py
# @Software: PyCharm
import pymysql
from .mysql_config import LOCALHOST, USER, PASSWORD, DATABASE


class MySqlControl(object):
    def __init__(self):
        self.localhost = LOCALHOST
        self.user = USER
        self.pwd = PASSWORD
        self.database = DATABASE
        self.conn = pymysql.connect(self.localhost, self.user, self.pwd, self.database)
        self.cursor = self.conn.cursor()

    def execute_sql_query(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        a = self.cursor.description
        self.close_db()
        return result, a

    def execute_sql_transaction(self, *args):
        try:
            for sql in args:
                self.cursor.execute(sql)
        except Exception as e:
            print(e)
            print('操作失败,回滚事务')
            self.conn.rollback()
        else:
            self.conn.commit()
            print('数据库执行成功')
        finally:
            self.close_db()

    def close_db(self):
        self.cursor.close()
        self.conn.close()




if __name__ == '__main__':
    db = MySqlControl()

    sql = '''
    SELECT usernameas 用户名 FROM Main_registerfirst
    '''

    data, a = db.execute_sql_query(sql)

    print(data, a)