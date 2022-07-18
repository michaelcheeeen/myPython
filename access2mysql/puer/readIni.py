# -*- coding: utf-8 -*-
# 导入依赖
import configparser

# 创建配置类对象
cf = configparser.ConfigParser()

# 读取配置文件
cf.read("config.ini", encoding="utf-8")

# 获取文件中的所有配置
sections = cf.sections()
print(sections)

# 获取某个section名为config所对应的键
options = cf.options("mysql")
print(options)

#  获取config配置中的id值
id = cf.get("mysql", "charset")
print(id)