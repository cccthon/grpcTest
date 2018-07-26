#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Email_Send_001_001
# 用例标题: 发送邮件
# 预置条件: 
# 测试步骤:
#   1.调用接口：Send
# 预期结果:
#   1.邮件发送成功
# 脚本作者: shencanhui
# 写作日期: 20171016
#=========================================================
import grpc,sys,unittest,yaml
sys.path.append("..\\..\\lib\\ServicesProtoclo\\email")
import email_pb2
import email_pb2_grpc
# import page_pb2
# import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class Send(unittest.TestCase):
    def setUp(self):
        #连接email测试服务器
        channel = grpc.insecure_channel(userData['email_host'] + ':' + userData['email_port'])
        self.stub = email_pb2_grpc.EmailSrvStub(channel)

    def test_SendEmail(self):
        #发送email
        Sendmail = self.stub.Send(email_pb2.SendMailRequest(To = 'shencanhui@followme.com', Subject = 'test', Body = 'test123'))
        self.assertEqual(Sendmail.Success, 1)

    def tearDown(self):
        #清空测试环境
        pass


if __name__ == '__main__':
    unittest.main()