import pyodbc
import pymysql
#创建access数据库库连接
# DBfile = r"C:/Users/22248/Desktop/原始数据库/AdventureWorks2008.mdb"  # 数据库文件
DBfile = r"D:/kisen/kisen-project/SynologyDrive/诸多项目===/普洱/tye.mdb"  # 数据库文件
conn_A = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=88272008;charset=‘utf-8’;") # xingaolhw
cursor_A = conn_A.cursor()
#创建mysql数据库连接
conn_M = pymysql.connect(
    host='192.168.14.12',
    user='root',
    passwd='Kisen123456',#输入自己的mysql密码
    port=3306,
    db='accessdb',
    charset='utf8'
)
cursor_M = conn_M.cursor(pymysql.cursors.DictCursor)
#准备3个容器
tables = []
fields = []
field_str = []
#获取所有表名
for table_info in cursor_A.tables(tableType='TABLE'):
    tables.append(table_info.table_name)
#遍历所有表名
for table in tables:
    for row in cursor_A.columns(table):
        fields.append(row.column_name)
    # 判断下TABLE在MYSQL是否存在， 存在导入
    hasTable = cursor_M.execute(f"select * from information_schema.tables where table_name ='{table}'")
    if hasTable == 1:
        #进行sql语句拼接
        f = ','.join(fields)
        s = ','.join(['%s' for i in range(len(fields))])
        sql = f'insert into {table}({f}) values({s})'
        SQL = f"SELECT * from {table};"
        if table == 'SNKYGROne':
            sql = f'insert into {table}(`ZuHao`, `LingQI`, `PingZhong`, `OnekN`, `ShunXu`, `LenAv`, `WidAv`) values(%s,%s,%s,%s,%s,%s,%s)'
            SQL = f"SELECT `ZuHao`, `LingQI`, `PingZhong`, `OnekN`, `ShunXu`, `LenAv`, `WidAv` from {table};"
        print(sql)
        print(SQL)
        #获取到表的数据
        for row in cursor_A.execute(SQL):
            field_str.append(tuple(row))  # pyodbc.row -> tuple 否则sql提交失败
        count = cursor_M.executemany(sql, field_str)  # 传入多条数据
        print(f" table-'{table}' insert into mysql 数据量:" + str(count) + ", access数据量：" + str(len(field_str)))
        conn_M.commit()  # 提交更改

        fields.clear()
        field_str.clear()
    else:
        print(f" mysql do not exist table-'{table}'")

cursor_A.close()
conn_A.close()
cursor_M.close()  # 游标关闭
conn_M.close()