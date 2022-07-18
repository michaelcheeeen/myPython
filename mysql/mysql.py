import pymysql
# 连接数据库
conn = pymysql.connect(
    host='192.168.14.12',
    user='root',
    passwd='Kisen123456',#输入自己的mysql密码
    port=3306,
    db='accessdb',
    charset='utf8'
)  # 数据库名称
# 创建数据库对象
# cursor = conn.cursor()
cursor = conn.cursor(pymysql.cursors.DictCursor)
# 写入SQL语句
# sql = 'insert into CheckTempValue(CtrlBox,Name,Value) values(%s,%s,%s)'
# param = [('EHC1000', 'CheckNum1', '2890.00'), ('EHC1000', 'CheckNum2', '49440.00'), ('EHC1000', 'CheckNum3', '99810.00')]
# cursor.executemany(sql, param)

sql = r"select * from information_schema.tables where table_name ='samples'"
hasTable = cursor.execute(sql)

if (hasTable == 1):
    print('exist')
else:
    print('no exist')
# 获取全部的查询内容
# restul = cursor.fetchall()
# print(restul)
conn.commit()
# 执行sql命令
# db.execute(sql)
# 获取一个查询
# restul = db.fetchone()


cursor.close()
conn.close()