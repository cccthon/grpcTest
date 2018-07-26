import os,re,unittest,time,smtplib,pyodbc
from email.utils import parseaddr, formataddr
from email.header import Header
from email.mime.text import MIMEText
import HTMLTestRunnerEN
from email import encoders

#从文件中匹配相关字符
def getCharInFile(file,replacestr):
    html = open(file,'rb').readlines()
    for line in html:
      result = re.search('Status.+%',bytes.decode(line))
      if result:
         status = result.group().replace(replacestr,'')
         return status

#格式化邮箱地址、名称
def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

#定义需要连跑的测试用例，即测试套
def testSuite(testCaseDir,testCase):
    testSuite = unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(testCaseDir,pattern=testCase,top_level_dir=None)
    #discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suit in discover:
          testSuite.addTests(test_suit)
    return testSuite

#测试报告生成
def testRunner(reportDir,title,description):
    fr = open(reportDir,'wb')
    testRunner = HTMLTestRunnerEN.HTMLTestRunner(stream=fr, title=title,description=description)
    # fr.colse()
    return testRunner

#发送smtp邮件
def sendMail(mmeText,fromAddr,toAddr,header,smtpServer,passwd):
    msg = MIMEText(mmeText, 'plain', 'utf-8')
    msg['From'] = format_addr(fromAddr)
    msg['To'] = format_addr(toAddr)
    msg['Subject'] = Header(header, 'utf-8').encode()
    smtp = smtplib.SMTP(smtpServer, 25)
    # smtp.set_debuglevel(1)
    smtp.login(fromAddr, passwd)
    smtp.sendmail(fromAddr, toAddr, msg.as_string())
    smtp.quit()

# def specialTestCaseRun():
    #运行指定用例
    # suiteTest = unittest.TestSuite()
    # suiteTest.addTest(TestAccountFunctionsaa("test_getCachedUserByIdaa"))
    # suiteTest.addTest(TestAccountFunctionsaa("test_getCachedUserByIdaa"))
    # print('Suite_level_1 运行')
    # return suiteTest

def delete_db_data(server,port,database,uid,pwd,sql):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';PORT=' + port + ';DATABASE=' + database + ';UID=' + uid + ';PWD=' + pwd)
    cursor = cnxn.cursor()
    deleted = cursor.execute(sql).rowcount
    cnxn.commit()