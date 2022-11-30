from sys import stdout
import time, gol

class dkConfigObject():
    global saveHc
    global waitSec
    
    global stdout
    global log

    inputFile = ''
    outputFile = ''

class submitStatusObject():
    global fails
    global success

class dkUtil():

    def SaveInput(loginDict, tp):
        fileName = input("请输入文件名: ")
        try:
               saveFile = open(fileName, 'w')
        except IOError:
               print("错误: 文件建立或访问失败")
        else:
               for i in loginDict:
                   saveFile.write(i + ' ')
                   for j in tp[1:]:
                       saveFile.write(loginDict[i][j] + ' ')
                   saveFile.write('\n')

               saveFile.close()
               print("保存成功")

    def t():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': '

    def ts():
        return str(round(time.time() * 1000))

    def printf(str): # 根据 stdout 变量的情况选择是输出到 stdout 还是输出到指定的文件
        if gol.get_value('dkConfig').stdout: print(dkUtil.t() + str)
        else: gol.get_value('dkConfig').log.write(dkUtil.t() + str + '\n')

    pass




