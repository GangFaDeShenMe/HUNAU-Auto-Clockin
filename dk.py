#!/usr/bin/python3

import sys, getopt, requests, time, random
from hashlib import md5

def t():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': '

def ts():
    return str(round(time.time() * 1000))

def printf(str): # 根据 stdout 变量的情况选择是输出到 stdout 还是输出到指定的文件
    if stdout: print(str)
    else: log.write(str + '\n')

def genLocInfo(sAddr): # 生成地址信息
    locInfo = {}
    if sAddr == "湖南省长沙市":
            locInfo["dkdz"]           = '湖南省长沙市芙蓉区农大路1号'
            locInfo["dkdzZb"]         = str(round(113.09 + random.uniform(-0.01, 0.01), 4)) + ',' + str(round(28.18 + random.uniform(-0.01, 0.01), 4))
            locInfo["dkly"]           = 'baidu'      # ↑ 在农大经纬度 (113.09, 28.18) 各 ±0.01 范围内随机产生坐标，避免被检测 ↑
            locInfo["jzdSheng.dm"]    = "430000"     # 湖南省
            locInfo["jzdShi.dm"]      = "430100"     # 长沙市
            locInfo["jzdXian.dm"]     = "430102"     # 芙蓉区

    elif sAddr  == "xx省xx市":
            1

            # 要添加自定义省市，照上面的格式写就可以

    return locInfo

def main(argv):
   inputFile = ''
   outputFile = ''

   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('-h (显示用法)')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('用法: -i [登录信息文件，不指定时从 stdin 取得登录信息] -o [输出的 log 文件，不指定时向 stdout 输出]')
         print('      -h (显示用法)')
         print('湘农打卡小助手 V1.1 -GangFaDeShenMe')
         sys.exit(0)
      elif opt in ("-i", "--ifile"):
         inputFile = arg
      elif opt in ("-o", "--ofile"):
         outputFile = arg
   
   # 在此手动指定输出文件
   #outputFile = "2.txt"

   global stdout
   if outputFile == '':
      stdout = True
      printf(t() + "没有指定输出的 log 文件，默认输出到 stdout 。")
   else:
      global log
      log = open(outputFile, 'a')
      stdout = False
      
   printf(t() + '湘农打卡小助手 V1.1 -GangFaDeShenMe')

   # 在此手动指定输入文件
   #inputFile = '1.txt'

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
   #学号 密码 省市地址 详细地址 联系电话 是否在校(Y/N) 备注
   123 456 湖南省长沙市 湖南农业大学芷兰学生公寓12栋314 12365473214 y 无
   789 654 湖南省长沙市 湖南农业大学金岸学生公寓7栋108  16665473214 n 被隔离
   789 654 湖南省长沙市 湖南农业大学丰泽学生公寓4栋204  16665473214 y 无
   '''
   ##########################

   loginDict = {}

   if inputFile != '':
       printf(t() + "输入文件：" + inputFile)
       try:
           i = open(inputFile, "r")
       except IOError:
           printf(t() + "错误: 没有找到文件或读取文件失败")
           exit(1)

       else:
           for line in i:
               if line[0] != '#' and line[0] != '\n' and line[0] != ' ' and line[0] != '\t':
                  ID, pwd, sAddr, sDetailedAddr, sPhoneNo, sPresentStatus, sNote = line.rstrip().split(' ')
                  loginDict[ID] = {"密码" : pwd, "省市地址" : sAddr, "详细地址" : sDetailedAddr, "联系电话" : sPhoneNo, "是否在校" : sPresentStatus, "备注" : sNote}

           printf(t() + "读取输入文件成功")
           i.close()
   else :
       print(t() + "没有指定输入文件，从 stdin 读取登录信息。任何时候输入 x 结束输入。")
       
       global tp
       tp = ("学号: ", "密码", "省市地址", "详细地址", "联系电话", "是否在校(Y/N)", "备注")
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
       
       isSave = input(t() + "是否保存当前输入至脚本目录下的文件？输入 Y 确认，输入其他取消")
       if isSave == 'Y' or isSave == 'y':
           fileName = input("请输入文件名: ")
           try:
               saveFile = open(fileName, 'w')
           except IOError:
               print(t() + "错误: 文件建立或访问失败")
           else:
               for i in loginDict:
                   saveFile.write(i + ' ')
                   for j in tp[1:]:
                       saveFile.write(loginDict[i][j] + ' ')
                   saveFile.write('\n')

               saveFile.close()
               print(t() + "保存成功")
       else: print(t() + "保存已取消")

       if stdout == False : print("重导向输出至文件")

   for sID in loginDict:
       time.sleep(3)
       submit(sID, loginDict[sID])

   if stdout == False:
      log.close()
   else: input("按任意键继续。")   

def hunauEncrypt(sPwd): # 湘农密码加密法
    sMd5 = md5()
    sMd5.update(sPwd.encode('utf-8'))
    sMd5Str = sMd5.hexdigest()
    return sMd5Str[0:5] + 'a' + sMd5Str[5:9] + 'b' + sMd5Str[9:-2]

def genWechatUa(): # 随机挑选一条微信 UA ，防止被检测
        UAs = (r"Mozilla/5.0 (Linux; Android 11; MI 9 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220709 Mobile Safari/537.36 MMWEBID/6297 MicroMessenger/8.0.25.2200(0x28001953)", 
               r"Mozilla/5.0 (Linux; Android 11; 21091116C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/287 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (Linux; Android 10; SEA-AL10 Build/HUAWEISEA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/9538 MicroMessenger/8.0.27.2220(0x28001B53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220604 Mobile Safari/537.36 MMWEBID/8603 MicroMessenger/8.0.24.2180(0x28001851) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220709 Mobile Safari/537.36 MMWEBID/3066 MicroMessenger/8.0.25.2200(0x28001953) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (Linux; Android 10; HLK-AL00 Build/HONORHLK-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/2095 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (Linux; Android 10; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/5096 MicroMessenger/8.0.27.2220(0x28001B3F) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b34) NetType/4G Language/zh_CN",
               r"Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220505 Mobile Safari/537.36 MMWEBID/6304 MicroMessenger/8.0.23.2160(0x28001757) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3185 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/6210 MicroMessenger/8.0.16.2040(0x2800105F) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64] Edg/98.0.4758.102",
               r"Mozilla/5.0 (Linux; Android 11; M2004J7BC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/1368 MicroMessenger/8.0.27.2220(0x28001B53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               r"Mozilla/5.0 (Linux; Android 10; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1166 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/1731 MicroMessenger/7.0.10.1580(0x27000AFC) Process/toolsmp NetType/4G Language/zh_CN ABI/arm64"
              )
        return random.choice(UAs)

def submit(sID, sIdDict):
    url = "http://xgxt.hunau.edu.cn/" # 湖南农业大学学工平台

    header = {
      "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
      "Accept-Encoding" : "gzip, deflate",
      "Accept-Language": "zh-CN,zh;q=0.9",
      "Connection": "keep-alive",
      "DNT": "1",
      "Host": "xgxt.hunau.edu.cn",
      "Upgrade-Insecure-Requests" : "1",
      "User-Agent": genWechatUa() # 伪装成微信的 UA ，避免检测
    }

    loginGet = requests.get(url + "index", headers = header) # 访问学工平台登录页
    cookie = loginGet.cookies # 取得 Cookie （会话 ID）

    if loginGet.ok:
       time.sleep(2)
       loginPost = requests.post(url + "website/login", data = (('uname', sID), ('pd_mm', hunauEncrypt(sIdDict["密码"]))), cookies = cookie)
       # 提交登录请求

       if loginPost.ok:
          loginRes = loginPost.json()
        
          if 'error' in loginRes:
             printf(t() + "学号 " + sID + " 登录出错，服务器传回信息： " + loginRes['msg'])

          elif 'goto2' in loginRes: # Cookie / 会话 ID 有效化

             printf(t() + "学号 " + sID + " 登录成功。")

             time.sleep(2)
             dkGet = requests.get(url + "wap/menu/student/temp/zzdk/_child_/edit?_t_s_=" + ts(), cookies = cookie, headers = header)
             # 访问打卡页面

             if dkGet.ok:
                  zzdk_token = (dkGet.text.splitlines()[79])[77:83] # 取得 zzdk_token
                  zxBool = 0


                  if sIdDict["是否在校"] == "在校":
                     zxBool = 1
                     locInfo = genLocInfo("湖南省长沙市") # 避免自相矛盾的数据
                  else: locInfo = genLocInfo(sIdDict["省市地址"])

                  dkForm = {
                     "dkdz"         : locInfo["dkdz"],
                     "dkdzZb"       : locInfo["dkdzZb"],
                     "dkly"         : locInfo["dkly"],
                     "zzdk_token"   : zzdk_token,
                     "dkd"          : sIdDict["省市地址"],
                     "jzdValue"     : locInfo["jzdSheng.dm"] + ',' + locInfo["jzdShi.dm"] + ',' + locInfo["jzdXian.dm"],
                     "jzdSheng.dm"  : locInfo["jzdSheng.dm"],
                     "jzdShi.dm"    : locInfo["jzdShi.dm"],
                     "jzdXian.dm"   : locInfo["jzdXian.dm"],
                     "jzdDz"        : sIdDict["详细地址"],
                     "jzdDz2"       : sIdDict["详细地址"],
                     "lxdh"         : sIdDict["联系电话"],
                     "sfzx"         : zxBool,
                     "sfzx1"        : sIdDict["是否在校"],
                     "twM.dm"       : "01",
                     "tw1"          : "[35.0~37.2]正常",
                     "tw1M.dm"      : '',
                     "tw11"         : '',
                     "tw2M.dm"      : '',
                     "tw12"         : '',
                     "tw3M.dm"      : '',
                     "tw13"         : '',
                     "yczk.dm"      : "01",
                     "yczk1"        : "无症状",
                     "fbrq"         : '',
                     "jzInd"        : '0',
                     "jzYy"         : '',
                     "zdjg"         : '',
                     "fxrq"         : '',
                     "brStzk.dm"    : "01",
                     "brStzk1"      : "身体健康、无异常",
                     "brJccry.dm"   : "01",
                     "brJccry1"     : "未接触传染源",
                     "jrStzk.dm"    : "01",
                     "jrStzk1"      : "身体健康、无异常",
                     "jrJccry.dm"   : "01",
                     "jrJccry1"     : "未接触传染源",
                     "jkm"          : '1',
                     "jkm1"         : "绿色",
                     "xcm"          : '1',
                     "xcm1"         : "绿色",
                     "xgym"         : '',
                     "xgym1"        : '',
                     "hsjc"         : '',
                     "hsjc1"        : '',
                     "bz"           : sIdDict["是否在校"],
                     "operationType": "Create",
                     "dm"           : ''
                  }
 
                  time.sleep(2)
                  dkPost = requests.post(url + "content/student/temp/zzdk?_t_s_=" + ts(), cookies = cookie, headers = header, data = dkForm)
                  # 提交打卡请求

                  dkRes = dkPost.json()
                  
                  printf(t() + "学号 " + sID + " 打卡状态: ")
                  if dkRes["result"] == True:
                      printf(t() + "成功。")
                  else:
                      printf(t() + "失败。服务器传回失败原因为 \"" + dkRes["errorInfoList"][0]["message"] + '"')

             else:
                  printf("学号: " + sID + t() + "获取打卡页面失败")

       else:
          printf("学号: " + sID + t() + "登录请求发送失败")

    else: 
        printf("学号: " + sID + t() + "获取登录页面失败")

if __name__ == "__main__":
    main(sys.argv[1:])