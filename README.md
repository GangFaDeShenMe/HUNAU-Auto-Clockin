# HUNAU-Auto-Clockin  
湘农打卡小助手  

一个基于 python3 的湖南农业大学自动打卡脚本

## 安装方法：
1. 下载安装 python3  
   ```
   https://www.python.org/downloads/
   ```
2. 安装 python库 request  
    
   打开 cmd 或 powershell 输入  
   ```
   pip3 install requests  
   ```  
   若报错请检查环境变量。  
   
3. 下载脚本到你喜欢的地方。

## 用法  
1. 第一次运行脚本时，请直接双击打开脚本，根据提示输入对应信息。  
   
   例如：  
   ![image](https://user-images.githubusercontent.com/54745033/199635825-656361ec-5d09-4088-baba-b902b80391ac.png)  
   
   然后保存文件：  
   ![image](https://user-images.githubusercontent.com/54745033/199635879-26471bef-ea9e-46e4-a57a-792187f5bd05.png)  
   
   这样下次启动脚本时，只需要执行  
   ```
   python ./dk.py -i 1.txt
   ```
   就可以自动读取上次保存的信息。
   
2. 设置自动运行  
   
   命令行参数里带上 `-i [在此写上带路径的文件名] ` 和 `-o [在此写上带路径的文件名]` 可指定输入文件和输出文件。注意使用绝对路径。
   
   Windows 用户参考这篇文章  
   ```
   https://blog.csdn.net/u012849872/article/details/82719372
   ```
   Linux 用户参考这篇文章  
   ```
   https://www.runoob.com/w3cnote/linux-crontab-tasks.html
   ```
