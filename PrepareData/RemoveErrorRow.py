import re

lines = []
lines1 = []
with open("house_data.txt", mode='r', encoding="utf-8") as fp:
    lines = fp.readlines()

# Xoa khoang trang du thua trong file txt.
flag = False
for it in lines:
    if(flag == False):
        lines1.append(it)
    if(flag == True):
        flag = False
        continue
    if(it[len(it)-2]=="²"):
        flag = True

lines2 = []
cnt = 0
for it in lines1:
    if(cnt > 0):
        cnt -= 1
        continue
    lines2.append(it)
    if(it[len(it)-2]=="²"):
        cnt = 2

with open("house_data_0space.txt", mode="w+", encoding="utf-8") as fp:
    output = []
    for it in lines2:
        if(it.isspace()):
            if(len(output)>2):
                for op in output:
                    fp.write(op)
                fp.write("\n")
            
            output = []
        else:
            output.append(it)

#Xoa du lieu co gia la "Thoa Thuan"
with open("house_data_0space.txt", mode='r', encoding="utf-8") as fp:
    lines = fp.readlines()

flag = False
with open("house_data_0space.txt", mode="w+", encoding="utf-8") as fp:
    output = []
    for it in lines:
        if(len(re.findall("Thỏa thuận", it)) > 0):
            flag = True
        if(flag == False):
            output.append(it)
        if(it.isspace()):
            if(flag == True):
                flag = False
                continue
            flag = False
            for op in output:
                fp.write(op)
            output = []

