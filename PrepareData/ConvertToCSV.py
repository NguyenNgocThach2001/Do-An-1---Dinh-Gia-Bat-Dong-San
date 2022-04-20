import re
import csv

from sklearn import datasets

tag = ["Giá", "Diện Tích", "Địa chỉ", "Mặt tiền", "Đường vào", "Hướng nhà", "Hướng ban công", "Số tầng", "Số phòng ngủ", "Số toilet", "Pháp lý"]
lines = []
with open("house_data_0space.txt", mode='r', encoding="utf-8") as fp:
    lines = fp.readlines()

output = []
pre_data = [{}]
for it in lines:
    if(it.isspace() == False):
        line = it.replace("\n", "")
        output.append(line)
    else:
        tmp = []
        price = output[0].split(' ')
        acreage = output[1].split(' ')
        cnt = 2
        tmp.append({"Giá" : price[0] + " tỷ"})
        tmp.append({"Diện Tích" : acreage[0] + " m2"})
        output.sort()
        while(cnt <= len(output)-1):
            element = output[cnt].split(':')
            if(len(element) == 1):
                cnt+=1
                continue
            element[0].strip("\n")
            element[1].strip("\n")
            tmp.append({element[0]: element[1]})
            cnt += 1
        pre_data.append(tmp)
        output = []

tag.sort()
csv_header = tag
dataset = []
for it in pre_data:
    tmp = []
    for tags in csv_header:
        flag = False
        for pair in it:
            if(tags == list(pair.keys())[0]):
                flag = True
                tmp.append(*pair.values())
                break
        if(flag == False):
            tmp.append("None")
    dataset.append(tmp)

with open('House_Dataset.csv', 'w+', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)
    for it in dataset:
        writer.writerow(it)
