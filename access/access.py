import pyodbc
#创建access数据库库连接
# DBfile = r"C:/Users/22248/Desktop/原始数据库/AdventureWorks2008.mdb"  # 数据库文件
DBfile = r"D:\kisen\kisen-project\SynologyDrive\诸多项目===\普洱\MeasDB.mdb"  # 数据库文件
### pyodbc.Error: ('HY000', '[HY000] [Microsoft][ODBC Microsoft Access Driver]常见错误 无法打开注册表项“Temporary (volatile) Ace DSN for process 0x36e8 Thread 0x1e58 DBC 0xf23200b8
### 密码不对
conn_A = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=xingaolhw;charset=‘utf-8’;") # xingaolhw
cursor_A = conn_A.cursor()
#准备3个容器
tables = []
fields = []
field_str = []
#获取ACCESS所有表名
for table_info in cursor_A.tables(tableType='TABLE'):
    tables.append(table_info.table_name)
#遍历所有表名
for table in tables:
    for row in cursor_A.columns(table):
        fields.append(row.column_name)
    #进行sql语句拼接
    f = ','.join(fields)
    s = ','.join(['%s' for i in range(len(fields))])
    sql = f'insert into {table}({f}) values({s})'
    SQL = f"SELECT * from {table};"
    print(sql)
    print(SQL)
    #获取到表的数据
    for row in cursor_A.execute(SQL):
        field_str.append(row)


    fields.clear()
    field_str.clear()
cursor_A.close()
conn_A.close()
