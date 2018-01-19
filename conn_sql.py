#-*-coding:utf8-*-
from utility import *

ms = MYSQL(host="localhost", user="root", pwd="960513", db="prosper")
log = ms.ExecQuery("select * from listings" )
print type(log)
print log