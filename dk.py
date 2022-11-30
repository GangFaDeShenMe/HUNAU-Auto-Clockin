#!/usr/bin/python3

from dkGen import *
from dkUtil import *
import sys, getopt, requests, time, random, string, gol

def main(argv):
   gol._init()
   global dkConfig 
   dkConfig = dkConfigObject

   dkConfig.waitSec = 1
   dkConfig.saveHc = False
   dkConfig.submitMaxRetries = 5
   dkConfig.near = False

   gol.set_value('dkConfig', dkConfig)

   try:
      opts, args = getopt.getopt(argv,"hi:o:w:r:s:",["ifile=","ofile=","wait=","retries=","save="])
   except getopt.GetoptError:
      print('-h (显示用法)')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('用法: -i [登录信息文件，不指定时从 stdin 取得登录信息]')
         print('      -o [输出的 log 文件，不指定时向 stdout 输出]')
         print('      -w [每次访问服务器时的间隔时间，默认为 1]')
         print('      -r [打卡失败时的重试次数，默认为 5]')
         print('      -s [输入 Y 保存，输入其他取消。保存生成的健康码，默认为不保存]')
         print('      -h (显示用法)')
         print('湘农打卡小助手 V2.0 -GangFaDeShenMe')
         sys.exit(0)
      elif opt in ("-i", "--ifile"):
         dkConfig.inputFile = arg
      elif opt in ("-o", "--ofile"):
         dkConfig.outputFile = arg
      elif opt in ("-w", "--wait"):
          dkConfig.waitSec = int(arg)
      elif opt in ("-r", "--retries"):
         dkConfig.submitMaxRetries = int(arg)
      elif opt in ("-s", "--save"):
          if arg == 'y' or arg == 'Y':
            dkConfig.saveHc = True
          else:
            dkConfig.saveHc = False
      elif opt in ("-s", "--save"):
          if arg == 'y' or arg == 'Y':
            dkConfig.near = True
          else:
            dkConfig.near = False
   
   # 在此手动指定输出文件
   # dkConfig.outputFile = "output.txt"
   gol.set_value('dkConfig', dkConfig)
   
   if dkConfig.outputFile == '':
      dkConfig.stdout = True
      dkUtil.printf("没有指定输出的 log 文件，默认输出到 stdout 。")
   else:
      dkConfig.log = open(dkConfig.outputFile, 'a')
      dkConfig.stdout = False
      
   dkUtil.printf('湘农打卡小助手 V2.0 -GangFaDeShenMe')

   # 在此手动指定输入文件
   # dkConfig.inputFile = 'input.txt'

   ##########################
   # 输入文件格式示例 :
   '''
   #
   #用空白字符分隔学号和密码等信息。顺序不能颠倒，内容都是必填的，否则会出错。
   #使用 '#' 来写注释，只当在行首时才有效，否则会出错。
   #省市必须写明省字和市字。默认省市地址只支持填写 "湖南省长沙市"。
   #
   #示例
   #
   #学号 密码 省市地址 详细地址 联系电话 是否在校(Y/N) 姓名 身份证前后四位
   123 456 湖南省长沙市 湖南农业大学芷兰学生公寓12栋314 12365473214 y 徐俊平 11013019
   789 654 湖南省长沙市 湖南农业大学金岸学生公寓7栋108  16665473214 n 李四 43016666
   789 654 湖南省长沙市 湖南农业大学丰泽学生公寓4栋204  16665473214 y 王五 43029999
   '''
   ##########################

   dkUtil.printf("每次访问服务器时的间隔时间为 " + str(dkConfig.waitSec) + " 秒。")

   if dkConfig.saveHc:
       dkUtil.printf("保存生成的健康码。")
   else:
       dkUtil.printf("不保存生成的健康码。")

   dkUtil.printf("打卡失败时的重试次数为 " + str(dkConfig.submitMaxRetries) + " 次。")

   loginDict = {}

   if dkConfig.inputFile != '':
       dkUtil.printf("输入文件：" + dkConfig.inputFile)
       try:
           i = open(dkConfig.inputFile, "r")
       except IOError:
           dkUtil.printf("错误: 没有找到文件或读取文件失败")
           exit(1)

       else:
           for line in i:
               if line[0] != '#' and line[0] != '\n' and line[0] != ' ' and line[0] != '\t':
                  ID, pwd, sAddr, sDetailedAddr, sPhoneNo, sPresentStatus, sName, sIdNum = line.rstrip().split(' ')
                  loginDict[ID] = {"密码" : pwd, "省市地址" : sAddr, "详细地址" : sDetailedAddr, "联系电话" : sPhoneNo, "是否在校(Y/N)" : sPresentStatus, "姓名" : sName, "身份证前后四位" : sIdNum}
                  if sPresentStatus == 'y' or sPresentStatus == 'Y':
                      loginDict[ID]["是否在校"] = "在校"
                  else: loginDict[ID]["是否在校"] = "不在校"

           dkUtil.printf("读取输入文件成功")
           i.close()
   else :
       print("没有指定输入文件，从 stdin 读取登录信息。任何时候输入 x 结束输入。")
       
       global tp
       tp = ("学号: ", "密码", "省市地址", "详细地址", "联系电话", "是否在校(Y/N)", "姓名", "身份证前后四位")
       print("注意: 省市地址必须写成xx省xx市的格式。")

       while True:
           sID = input("输入学号: ")
           if sID == 'x' or sID == 'X': break

           loginDict[sID] = {}
           buf = ''
           for i in tp[1:]:
               buf = input("输入" + i + ": ")

               if i == "是否在校(Y/N)":
                   while True:
                       if buf == 'Y' or buf == 'y' or buf == 'N' or buf == 'n' or buf == 'X' or buf == 'x':
                           if buf == 'Y' or buf == 'y':
                               loginDict[sID]["是否在校"] = "在校"
                           elif buf == 'N' or buf == 'n':
                               loginDict[sID]["是否在校"] = "不在校"
                           break

                       else:
                           buf = input("输入错误。重新输入：")

               if buf == 'X' or buf == 'x':
                   del loginDict[sID]
                   break
               loginDict[sID][i] = buf
           if buf == 'X' or buf == 'x': break
       
       isSave = input("是否保存当前输入至脚本目录下的文件？输入 Y 确认，输入其他取消")
       if isSave == 'Y' or isSave == 'y':
           dkUtil.SaveInput(loginDict, tp)
       else: print("保存已取消")
       if dkConfig.stdout == False : print("重导向输出至文件")

   for sID in loginDict:
       global submitStatus
       submitStatus = submitStatusObject
       submitStatus.fails = 0
       submitStatus.success = False

       while True:
           if submitStatus.success:
               break

           if submitStatus.fails >= dkConfig.submitMaxRetries:
               dkUtil.printf("学号 " + sID + " 已达到最大重试次数: " + str(dkConfig.submitMaxRetries) + " 次。该学号打卡已取消。")
               break

           time.sleep(dkConfig.waitSec)
           submit(sID, loginDict[sID], dkConfig)

   if dkConfig.stdout == False:
      dkConfig.log.close()
   else: input("按任意键继续。")   

def submit(sID, sIdDict, dkConfig):
    # url = "http://10.7.1.246/" # 校内网访问入口
    url = "http://xgxt.hunau.edu.cn/" # 湖南农业大学学工平台

    wechatUa = dkGen.WechatUa(sID)
    header = dkGen.HttpHeader("loginGet", "", wechatUa)

    loginGet = requests.get(url + "index", headers = header) # 访问学工平台登录页
    cookie = loginGet.cookies # 取得 Cookie （会话 ID）

    if loginGet.ok:
       dkUtil.printf("学号 " + sID + " 获取登录页面成功")
       time.sleep(dkConfig.waitSec)
       
       header = dkGen.HttpHeader("loginPost", url + "index", wechatUa)
       loginPost = requests.post(url + "website/login", data = (('uname', sID), ('pd_mm', dkGen.HunauEncrypt(sIdDict["密码"]))), cookies = cookie, headers = header)
       # 提交登录请求

       if loginPost.ok:
          loginRes = loginPost.json()
        
          if 'error' in loginRes:
             dkUtil.printf("学号 " + sID + " 登录出错，服务器传回信息： " + loginRes['msg'])

          elif 'goto2' in loginRes: # Cookie / 会话 ID 有效化

             dkUtil.printf("学号 " + sID + " 登录成功。")

             time.sleep(dkConfig.waitSec)
             ref = url + "wap/menu/student/temp/zzdk/_child_/edit?_t_s_=" + dkUtil.ts()
             header = dkGen.HttpHeader("dkGet", ref, wechatUa)

             dkGet = requests.get(ref, cookies = cookie, headers = header)
             # 访问打卡页面

             if dkGet.ok:
                  dkUtil.printf("学号 " + sID + " 获取打卡页面成功")
                  zzdk_token = (dkGet.text.splitlines()[80])[77:83] # 取得 zzdk_token

                  zxBool = 0

                  if sIdDict["是否在校"] == "在校":
                     zxBool = 1
                     locInfo = dkGen.LocInfo("湖南省长沙市") # 避免自相矛盾的数据
                  else: locInfo = dkGen.LocInfo(sIdDict["省市地址"])

                  time.sleep(dkConfig.waitSec)

                  webkitFormBoundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
                  
                  dkData = dkGen.DkData(sIdDict, locInfo, zzdk_token, zxBool, webkitFormBoundary, dkConfig)
                  
                  header = dkGen.HttpHeader("dkPost", ref, wechatUa, webkitFormBoundary)
                  
                  # dkPost = requests.post("http://test.com/" + "content/student/temp/zzdk?_t_s_=" + dkUtil.ts(), cookies = cookie, headers = header, data = dkData)
                  dkPost = requests.post(url + "content/student/temp/zzdk?_t_s_=" + dkUtil.ts(), cookies = cookie, headers = header, data = dkData)

                  # 提交打卡请求
                  if dkPost.ok:
                        dkRes = dkPost.json()
                        dkUtil.printf("学号 " + sID + " 打卡状态: ")
                        if dkRes["result"] == True:
                            dkUtil.printf("成功。")
                            submitStatus.success = True
                            return
                        else:
                            dkUtil.printf("失败。服务器传回失败原因为 \"" + dkRes["errorInfoList"][0]["message"] + '"')
                        if dkRes["errorInfoList"][0]["message"] == "已打卡，请勿重复提交 ！":
                            submitStatus.success = True
                            return

                        elif "非法请求" in dkRes["errorInfoList"][0]["message"]:
                            dkUtil.printf("已被服务器检测到脚本行为，请勿继续使用脚本")
                            exit(1)

                        else:
                            submitStatus.fails = submitStatus.fails + 1
                            return
                  else:
                      dkUtil.printf("学号 " + sID + " 提交打卡请求失败")
                      submitStatus.fails = submitStatus.fails + 1
                      return
             else:
                  dkUtil.printf("学号 " + sID + " 获取打卡页面失败")
                  submitStatus.fails = submitStatus.fails + 1
                  return

       else:
          dkUtil.printf("学号 " + sID + " 登录请求发送失败")
          submitStatus.fails = submitStatus.fails + 1
          return

    else: 
        dkUtil.printf("学号 " + sID + " 获取登录页面失败")
        submitStatus.fails = submitStatus.fails + 1
        return

if __name__ == "__main__":
    main(sys.argv[1:])