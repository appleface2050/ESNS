# coding=utf-8
# Date: 15/1/30'
# Email: wangjian2254@icloud.com
import xlwt

__author__ = u'王健'

index = """
##你的need 客户端 api接口说明
**目录：**

------------------
"""
aindex = "* [%s.%s](#%s)"

hindex = ' <h3 id="%s">%s.%s</h3>'

mdfile = file('api.md')

indexlist = [index]

mdlist = []

num = 1
flag = 0

wb = xlwt.Workbook()
ws = wb.add_sheet(u'接口单元测试列表', cell_overwrite_ok=True)

for line in mdfile.readlines():
    print line
    if flag < 2 or line.find('**') == 0:
        if line.find('**') == 0:
            flag += 1
        if flag < 2:
            continue
    if line.find("<h3") >= 0 and line.find('</h3>') >= 0:
        title = line[line.find('.')+1:line.find('</')]
        indexlist.append(aindex % (num, title.replace(':',''), num))
        ws.write(num, 0, title.replace(':','').decode('utf-8'))
        mdlist.append(hindex % (num, num, title))
        num += 1
    else:
        mdlist.append(line.strip('\n'))
indexlist.append('<br/>')
apimdfile = file(u'你的Need 客户端 api接口说明.md', 'w')
apimdfile.write('\n'.join(indexlist + mdlist))
apimdfile.close()

try:
    wb.save('api.xls')
except Exception,e:
    print e

# 添加企业版接口
# by:王健 at:2015-06-18

index = """
##你的need 客户端 api接口说明-企业版
**目录：**

------------------
"""
aindex = "* [%s.%s](#%s)"

hindex = ' <h3 id="%s">%s.%s</h3>'

mdfile = file('api2.md')

indexlist = [index]

mdlist = []

num = 1
flag = 0

wb = xlwt.Workbook()
ws = wb.add_sheet(u'接口单元测试列表', cell_overwrite_ok=True)

for line in mdfile.readlines():
    print line
    if flag < 2 or line.find('**') == 0:
        if line.find('**') == 0:
            flag += 1
        if flag < 2:
            continue
    if line.find("<h3") >= 0 and line.find('</h3>') >= 0:
        title = line[line.find('.')+1:line.find('</')]
        indexlist.append(aindex % (num, title.replace(':',''), num))
        ws.write(num, 0, title.replace(':','').decode('utf-8'))
        mdlist.append(hindex % (num, num, title))
        num += 1
    else:
        mdlist.append(line.strip('\n'))
indexlist.append('<br/>')
apimdfile = file(u'你的Need 客户端 api接口说明-企业版.md', 'w')
apimdfile.write('\n'.join(indexlist + mdlist))
apimdfile.close()

try:
    wb.save('api2.xls')
except Exception,e:
    print e
