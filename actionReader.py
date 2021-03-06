import re

class actionReader:
    def strQ2B(self,ustring):
        """全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            # print(inside_code)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
                inside_code -= 65248

            rstring += chr(inside_code)
        return rstring

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
                line = line.replace('帅', '将')
                line = line.replace('仕', '士')
                result = re.search(pattern, line)  # 以pattern的值 分割字符串
                if result != None and len(line.split()) == 3:
                    line = self.strQ2B(line)
                    arra = line.split()
                    actionList.append(arra[1])
                    actionList.append(arra[2])
        except UnicodeDecodeError:
            return []
        return actionList
if __name__ == '__main__':
    actionReader = actionReader()
    file = open('C://Users//Lucky//Desktop//test//1 (1).PGN')
    actionList = actionReader.getActionList(file)
    print(actionList)


