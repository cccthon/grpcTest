#========================================================
#+++++++++++++++++  测试运行和测试报告设置   ++++++++++++++++
#   默认跑account目录下的全部用例
#   可以通过addTest方法添加指定测试用例进行连跑
#=========================================================
import grpc,sys,unittest,time,yaml,re
sys.path.append("..\\..\\lib\\public")
import HTMLTestRunnerEN
import public
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

#读入配置文件中数据
userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))
#####################################
#定义需要参与连跑的测试用例
#将account目录下的所有FM开头的python脚本加入测试套
testSuite = public.testSuite('../../test','FM*.py')

######################################
#开始主程序
if __name__ == '__main__':
    # testRunner = public.testRunner('../../report/index.html', userData['reportTitle'],userData['reportFitTitle'])
    report = open('../../report/index.html','wb')
    testRunner = HTMLTestRunnerEN.HTMLTestRunner(stream=report, title=userData['reportTitle'],description=userData['reportFitTitle'])
    testRunner.run(testSuite)
    report.close()

# time.sleep(10)
#获取测试结果
status = public.getCharInFile('../../report/index.html','</strong>')
print("Test Result " + str(status))

###################################
#通过邮件发送测试结果
print("send test result to mail...")
currTime = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))

mmeText = '\n' + str(userData['reportMailContent']) + '\n\n' + str(status) + '\n\n' + str(userData['reportMailContent2'])
fromAddr = userData['reportFromAddr']
toAddr = userData['reportToAddr']
subject = userData['reportSubject'] + currTime
smtpServer = userData['reportSmtpServer']
passwd= userData['reportPasswd']
public.sendMail(mmeText,fromAddr,toAddr,subject,smtpServer,passwd)
print("=================autoTest done.===================")