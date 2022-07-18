import pypyodbc # 导入pypyodbc模块

DBfile = r"D:\\kisen\\kisen-project\\SynologyDrive\\诸多项目===\\普洱\\MeasDB.mdb"  # 数据库文件
conn = pypyodbc.win_connect_mdb(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;charset=‘utf-8’;")
curser = conn.cursor()
tableList = []
for table_info in curser.tables(tableType='TABLE'):
    tableList.append(table_info[2])
print(tableList)