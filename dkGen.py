import random, os, gol, platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from hashlib import md5
from requests_toolbelt import MultipartEncoder

class dkGen():
    def LocInfo(sAddr): # 生成地址信息
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

    def HunauEncrypt(sPwd): # 湘农密码加密法
        sMd5 = md5()
        sMd5.update(sPwd.encode('utf-8'))
        sMd5Str = sMd5.hexdigest()
        return sMd5Str[0:5] + 'a' + sMd5Str[5:9] + 'b' + sMd5Str[9:-2]

    def WechatUa(sID): # 根据学号，固定挑选一条微信 UA ，防止被检测
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
               #r"Mozilla/5.0 (Linux; Android 11; M2004J7BC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/1368 MicroMessenger/8.0.27.2220(0x28001B53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
               #r"Mozilla/5.0 (Linux; Android 10; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1166 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/1731 MicroMessenger/7.0.10.1580(0x27000AFC) Process/toolsmp NetType/4G Language/zh_CN ABI/arm64"
              )
        return UAs[int(sID[-1])]

    # 阶段， referer 字段（上一级的 URL），wechatUa，post body 内容长度
    def HttpHeader(phase, referer, wechatUa, webkitFormBoundary = "", url = "http://xgxt.hunau.edu.cn/", host = "xgxt.hunau.edu.cn"):
        if phase == "loginGet":
            header = {
                "Host": host,
                "Connection": "keep-alive",
                "Accept": r"*/*",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": wechatUa,
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6"
            }
        elif phase == "loginPost":
            header = {
                "Host": host,
                "Connection": "keep-alive",
                "Accept": r"*/*",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": wechatUa,
                "Origin": url, #
                "Referer": referer, #
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6"
                }
        elif phase == "dkGet":
            header = {
                "Host": host,
                "Connection": "keep-alive",
                "Accept": r"*/*",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": wechatUa,
                "Origin": url, #
                "Referer": referer, #
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6"
                }
        elif phase == "dkPost":
            header = {
                "Host": host,
                "Connection": "keep-alive",
                "Accept": r"*/*",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": wechatUa,
                "Content-Type": "multipart/form-data; boundary=" + webkitFormBoundary, #
                "Origin": url,
                "Referer": referer,
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6"
                }

        return header

    def HCscreenshot(sIdDict, dkConfig):
        path = os.getcwd()

        chromeOpts = Options()
        chromeOpts.headless = True

        mobEmu = {
            "deviceName": "iPhone 12 Pro"
        }

        if 'linux' in platform.platform().lower():
            chromeOpts.add_argument('--disable-gpu')
            chromeOpts.add_argument('--no-sandbox')
        chromeOpts.add_experimental_option('excludeSwitches', ['enable-logging'])
        chromeOpts.add_experimental_option("mobileEmulation", mobEmu)

        driver = webdriver.Chrome(options = chromeOpts)
        driver.get("file://" + path + "/hc-sim/hunan-hc/index.html")

        driver.execute_script('addStorageField("_name","#name","名字","' + sIdDict["姓名"] + '")')
        driver.execute_script('addStorageField("_idcard","#idcard","证件号码","' + sIdDict["身份证前后四位"] + '",presetFilters.idcard(4,4))')
        driver.execute_script('addStorageField("_phone","#phone","手机号码","' + sIdDict["联系电话"] + '",presetFilters.phone())')
        if sIdDict["是否在校"] == "在校":
            driver.execute_script('addStorageField("_sample_spot","#sample-spot","采样点","' + random.choice(
                [
                    "科教新村采样",
                    "龙马社区文体广场",
                    "农大医院1号采样点",
                    "农大医院2号采样点",
                    "农大医院3号采样点",
                    "农大医院4号采样点",
                    "农大医院5号采样点",
                    "农大医院6号采样点",
                    "湖南农业大学",
                    "湖南农大修业广场（北）",
                    "湖南农大网球场（东）",
                    "湖南农大网球场（南）",
                    "湖南农大网球场（西）",
                    "湖南农大网球场（北）",
                    "东湖街道便民核酸采样点",
                    "湖南农大田径场（北）",
                    "湖南农大二篮球场（东）",




                ]
                ) + '")')
            driver.execute_script('addStorageField("_test_institution","#test-institution","检测中心","长沙艾迪康医学检验实验室")')

        elif sIdDict["省市地址"] == "xx省xx市":
            driver.execute_script('addStorageField("_sample_spot","#sample-spot","采样点","' + random.choice(
                [
                    "XX采样点",
                    "XX采样点"

                ]
                ) + '")')
            driver.execute_script('addStorageField("_test_institution","#test-institution","检测中心","XXX医学检验实验室")')

        driver.execute_script('const traceback_hours=6+8*Math.random();setDynamicTime(".qrcode-tips-time"),setStaticTime("#covid-test-month",5,7,traceback_hours),setStaticTime("#covid-test-day",8,10,traceback_hours),setStaticTime("#covid-test-hour",11,13,traceback_hours),setStaticTime("#covid-test-min",14,16,traceback_hours),initServiceWorker("hunan-hc")')
        
        if dkConfig.saveHc == True:
            driver.save_screenshot(sIdDict["身份证前后四位"] + '.png')
        driver.save_screenshot('screenshot.png')

        if 'linux' in platform.platform().lower():
            hcScreenshotPath = path + "/screenshot.png"
        elif 'windows':
            hcScreenshotPath = path + "\\screenshot.png"
        else:
            hcScreenshotPath = path + "/screenshot.png"

        return hcScreenshotPath

    def DkData(sIdDict, locInfo, zzdk_token, zxBool, webkitFormBoundary, dkConfig):
        hcScreenshotPath = dkGen.HCscreenshot(sIdDict, dkConfig)
        dkData = {}
        
        dkForm = (
                     ("dkdz"         , (None, locInfo["dkdz"])),
                     ("dkdzZb"       , (None, locInfo["dkdzZb"])),
                     ("dkly"         , (None, locInfo["dkly"])),
                     ("xcmTjd"       , (None, "")),
                     ("zzdk_token"   , (None, zzdk_token)),
                     ("dkd"          , (None, sIdDict["省市地址"])),
                     ("jzdValue"     , (None, locInfo["jzdSheng.dm"] + ',' + locInfo["jzdShi.dm"] + ',' + locInfo["jzdXian.dm"])),
                     ("jzdSheng.dm"  , (None, locInfo["jzdSheng.dm"])),
                     ("jzdShi.dm"    , (None, locInfo["jzdShi.dm"])),
                     ("jzdXian.dm"   , (None, locInfo["jzdXian.dm"])),
                     ("jzdDz"        , (None, sIdDict["详细地址"])),
                     ("jzdDz2"       , (None, sIdDict["详细地址"])),
                     ("lxdh"         , (None, sIdDict["联系电话"])),
                     ("sfzx"         , (None, str(zxBool))),
                     ("sfzxText"     , (None, sIdDict["是否在校"])),
                     ("twM.dm"       , (None, "01")),
                     ("twMText"      , (None, "[35.0~37.2]正常")),
                     ("yczk.dm"      , (None, "01")),
                     ("yczkText"     , (None, "无症状")),
                     ("jkm"          , (None, "1")),
                     ("jkmText"      , (None, "绿色")),
                     ("xcm"          , (None, "1")),
                     ("xcmText"      , (None, "绿色")),
                     ("xgym"         , (None, "3")),
                     ("xgymText"     , (None, "已接种加强针")),
                     ("hsjc"         , (None, '1')),
                     ("hsjcText"     , (None, '是')),
                     ("jkmcl_pathFile", ("screenshot_wechat.png", open(hcScreenshotPath, 'rb'), 'image/png')),
                     ("jkmcl_pathFile",(None, "")),
                     ("jkmcl_pathFile_upload_file_hid_input", (None, "1_1")),
                     ("operationType", (None, "Create")),
                     ("dm"           , (None, '')), # 抓包抓到这些意义不明的值
                     ("tw1M.dm"      , (None, '')),
                     ("tw2M.dm"      , (None, '')),
                     ("tw3M.dm"      , (None, '')),
                     ("brStzk.dm"    , (None, '01')),
                     ("brJccry.dm"   , (None, '01')),
                     ("jrStzk.dm"    , (None, '01')),
                     ("jrJccry.dm"   , (None, '01')),
                     ("xcmcl"        , (None, '')),
                     ("zdy1"         , (None, '')),
                     ("zdy2"         , (None, '')),
                     ("zdy3"         , (None, '')),
                     ("zdy4"         , (None, '')),
                     ("zdy5"         , (None, '')),
                     ("zdy6"         , (None, '')),
                     ("bz"           , (None, '无')),

                  )

        dkData = MultipartEncoder(dkForm, boundary = webkitFormBoundary)

        return dkData

    pass




