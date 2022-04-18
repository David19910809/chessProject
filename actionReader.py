import re

class actionReader:
    def getActionList(self,file):
        actionList = []
        #读取一行数据
        line = 'flag'
        try:
            while  line != '':
                line = file.readline()
                pattern = r'\d. +'  # 定义分隔符
                line = line.replace('一','1')
                line = line.replace('二', '2')
                line = line.replace('三', '3')
                line = line.replace('四', '4')
                line = line.replace('五', '5')
                line = line.replace('六', '6')
                line = line.replace('七', '7')
                line = line.replace('八', '8')
                line = line.replace('九', '9')
                line = line.replace('卒', '兵')
                line = line.replace('象', '相')
                result = re.search(pattern, line)  # 以pattern的值 分割字符串
                if result != None and len(line.split()) == 3:
                    arra = line.split()
                    actionList.append(arra[1])
                    actionList.append(arra[2])
        except UnicodeDecodeError:
            return []
        return actionList



