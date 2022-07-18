import pyodbc
import pymysql
import configparser

# config
cf = configparser.ConfigParser()
cf.read("config.ini", encoding="utf-8")
sections = cf.sections()

#创建mysql数据库连接
conn_Mysql = pymysql.connect(
    host=cf.get("mysql", "host"),
    user=cf.get("mysql", "user"),
    passwd=cf.get("mysql", "passwd"),
    port=int(cf.get("mysql", "port")),
    db=cf.get("mysql", "db"),
    charset=cf.get("mysql", "charset")
)
cursor_Mysql = conn_Mysql.cursor(pymysql.cursors.DictCursor)

#抗压
measdb = cf.get("access", "measdb")
measdb_pwd = cf.get("access", "measdb_pwd")
conn_measdb = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+measdb+";Uid=;Pwd="+measdb_pwd+";charset=‘utf-8’;")
cursor_measdb = conn_measdb.cursor()

SQL = f"SELECT `ZuHao`, `LingQI`, `PingZhong`, `OnekN`, `ShunXu`, `LenAv`, `WidAv` from SNKYGROne;"
field_str = []
for row in cursor_measdb.execute(SQL):
    field_str.append(tuple(row))  # pyodbc.row -> tuple 否则sql提交失败
sql = f'insert into SNKYGROne (`ZuHao`, `LingQI`, `PingZhong`, `OnekN`, `ShunXu`, `LenAv`, `WidAv`) values(%s,%s,%s,%s,%s,%s,%s)'
cursor_Mysql.execute("TRUNCATE SNKYGROne;")
count = cursor_Mysql.executemany(sql, field_str)  # 传入多条数据
print(f" table-'SNKYGROne' insert into mysql 数据量:" + str(count) + ", access数据量：" + str(len(field_str)))

conn_Mysql.commit()  # 提交更改
cursor_measdb.close()
conn_measdb.close()

#抗折
# conn_tye = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + path+'tye.mdb' + ";Uid=;Pwd=88272008;charset=‘utf-8’;") # xingaolhw
# cursor_tye = conn_tye.cursor()
# SQL = f"SELECT `ZuHao`, `LingQI`, `PingZhong`, `OnekN`, `ShunXu`, `LenAv`, `WidAv` from SNKYGROne;"
# #获取到表的数据
# field_str = []
# for row in cursor_tye.execute(SQL):
#     field_str.append(tuple(row))  # pyodbc.row -> tuple 否则sql提交失败
# sql = f'insert into SNKYGROne (`ZuHao`, `LingQI`, `PingZhong`, `OnekN`, `ShunXu`, `LenAv`, `WidAv`) values(%s,%s,%s,%s,%s,%s,%s)'
# cursor_Mysql.execute("TRUNCATE SNKYGROne;")
# count = cursor_Mysql.executemany(sql, field_str)  # 传入多条数据
# print(f" table-'SNKYGROne' insert into mysql 数据量:" + str(count) + ", access数据量：" + str(len(field_str)))
# conn_Mysql.commit()  # 提交更改
# cursor_tye.close()
# conn_tye.close()

#碳硫分析仪
csdatadb = cf.get("access", "csdatadb")
csdatadb_pwd = cf.get("access", "csdatadb_pwd")
conn_cs_data = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+csdatadb+";Uid=;Pwd="+csdatadb_pwd+";charset=‘utf-8’;")
cursor_cs_data = conn_cs_data.cursor()

SQL = f"SELECT `ID`, `SampleNo`, `SampleName`, `Description`, `AnalyseAmounts`, `LastAnalyseTime`, `SampleGg`, `SampleCz` from samples;"
#获取到表的数据
field_str = []
for row in cursor_cs_data.execute(SQL):
    field_str.append(tuple(row))  # pyodbc.row -> tuple 否则sql提交失败
sql = f'insert into samples (`ID`, `SampleNo`, `SampleName`, `Description`, `AnalyseAmounts`, `LastAnalyseTime`, `SampleGg`, `SampleCz`) values(%s,%s,%s,%s,%s,%s,%s,%s)'
# 清表
cursor_Mysql.execute("TRUNCATE samples;")
count = cursor_Mysql.executemany(sql, field_str)  # 传入多条数据
print(f" table-'samples' insert into mysql 数据量:" + str(count) + ", access数据量：" + str(len(field_str)))

SQL1 = f"SELECT `ID`, `SampleID`, `UserID`, `AnalyseTime`, `AnalyseWeight`, `Data_C`, `Jzxs_C`, `Kbz_C`, `Bybzz_C`, `Jzdp_C`, `TopTime_C`, `TopVal_C`, `SumVal_C`, `Area_C`, `CostTime_C`, `Data_S`, `Jzxs_S`, `Kbz_S`, `Bybzz_S`, `Jzdp_S`, `TopTime_S`, `TopVal_S`, `SumVal_S`, `CostTime_S`, `Area_S`, `Amount`, `Channel_C`, `Channel_S`, `Bz` from AnalyseData;"
field_str1 = []
for row in cursor_cs_data.execute(SQL1):
    field_str1.append(tuple(row))  # pyodbc.row -> tuple 否则sql提交失败
sql1 = f'insert into analysedata (`ID`, `SampleID`, `UserID`, `AnalyseTime`, `AnalyseWeight`, `Data_C`, `Jzxs_C`, `Kbz_C`, `Bybzz_C`, `Jzdp_C`, `TopTime_C`, `TopVal_C`, `SumVal_C`, `Area_C`, `CostTime_C`, `Data_S`, `Jzxs_S`, `Kbz_S`, `Bybzz_S`, `Jzdp_S`, `TopTime_S`, `TopVal_S`, `SumVal_S`, `CostTime_S`, `Area_S`, `Amount`, `Channel_C`, `Channel_S`, `Bz`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s)'
cursor_Mysql.execute("TRUNCATE AnalyseData;")
count1 = cursor_Mysql.executemany(sql1, field_str1)  # 传入多条数据
print(f" table-'AnalyseData' insert into mysql 数据量:" + str(count1) + ", access数据量：" + str(len(field_str1)))

conn_Mysql.commit()  # 提交更改
cursor_cs_data.close()
conn_cs_data.close()



cursor_Mysql.close()  # 游标关闭
conn_Mysql.close()