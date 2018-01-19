#-*-coding:utf8-*-
import numpy as np
import datetime
import time
import math
import pandas as pd
import pymysql
from functools import wraps

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.__name__, str(t1-t0))
               )
        return result
    return function_timer

class MYSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")

        self.conn = pymysql.connect(self.host, self.user, self.pwd, self.db)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    @fn_timer
    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        try:
            cur.execute(sql)
            resList = cur.fetchall()
        # 查询完毕后必须关闭连接
        except:
            print("Error: unable to fecth data")
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 提交修改
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()

        self.conn.close()

