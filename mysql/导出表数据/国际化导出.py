# coding:utf8
import sys
import xlwt
#import MySQLdb
import pymysql as MySQLdb
import datetime

host = '192.168.1.211'
user = 'root'
pwd = 'Kisen123456'
db = 'mms_master'
sql = 'SELECT i18n_key, SUBSTRING_INDEX(GROUP_CONCAT(i18n_value order by locale SEPARATOR \'$$\'), \'$$\',1) as \'中文\', SUBSTRING_INDEX(GROUP_CONCAT(i18n_value order by locale SEPARATOR \'$$\'), \'$$\', -1) as \'英文\', null as \'韩文\' FROM sys_i18n GROUP BY i18n_key'
sheet_name = 'building'
out_path = 'i18n.xls'


conn = MySQLdb.connect(host,user,pwd,db,charset='utf8')
cursor = conn.cursor()
count = cursor.execute(sql)
print(count)

cursor.scroll(0,mode='absolute')
results = cursor.fetchall()
fields = cursor.description
workbook = xlwt.Workbook()
sheet = workbook.add_sheet(sheet_name,cell_overwrite_ok=True)

for field in range(0,len(fields)):
    sheet.write(0,field,fields[field][0])

row = 1
col = 0
for row in range(1,len(results)+1):
    for col in range(0,len(fields)):
        sheet.write(row,col,u'%s'%results[row-1][col])

workbook.save(out_path)