# coding: utf-8
# import os
# from xml.dom.minidom import parse
# import xml.dom.minidom
#
# from config import D_UP_LOADS
#
# # 使用minidom解析器打开 XML 文档
# file_name = os.path.join(D_UP_LOADS, '0245-web_rules.xml')
# DOMTree = xml.dom.minidom.parse(file_name)
# collection = DOMTree.documentElement
# rules = collection.getElementsByTagName("rule")
# for rule in rules:
#     rule_id = rule.getAttribute("id")
#     level = rule.getAttribute("level")
#     description = rule.getElementsByTagName('description')[0]
#     describe = description.childNodes[0].data
#
# from datetime import datetime, timedelta
# thirty_days_ago = datetime.now() - timedelta(days=30)
# print thirty_days_ago
from werkzeug.contrib.cache import MemcachedCache

mem_cache = MemcachedCache(['127.0.0.1:11211'])
print mem_cache.get('12')