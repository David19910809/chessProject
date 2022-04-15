import re
f = open("C://test//test.PGN")
#读取一行数据
byt = 'flag'
while  byt != '':
    byt = f.readline()
    pattern = r'\d. +'  # 定义分隔符
    result = re.search(pattern, byt)  # 以pattern的值 分割字符串
    if result != None:
        print(byt.split())
    # print(byt)

