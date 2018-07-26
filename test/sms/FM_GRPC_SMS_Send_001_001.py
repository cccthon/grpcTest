#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_SMS_Send_001_001
# 用例标题: 发送短信
# 预置条件: 
# 测试步骤:
#   1.调用接口：send短信
# 预期结果:
#   1.短信发送成功，目标可以收到短信
# 脚本作者: shencanhui
# 写作日期: 20171016
#=========================================================
import grpc,sys,unittest,yaml
sys.path.append("..\\..\\lib\\ServicesProtoclo\\sms")
import sms_pb2
import sms_pb2_grpc
# import page_pb2
# import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class Send(unittest.TestCase):
    def setUp(self):
        #连接sms测试服务器
        channel = grpc.insecure_channel(userData['sms_host'] + ':' + userData['sms_port'])
        self.stub = sms_pb2_grpc.SmsSrvStub(channel)

    def test_SendSMS(self):
        #发送email
        SendSMS = self.stub.Send(sms_pb2.SendRequest(PhoneNumbers = '17688824433', Content = 'followme sms test'))
        self.assertEqual(SendSMS.Success, 1)

    def tearDown(self):
        #清空测试环境
        pass

if __name__ == '__main__':
    unittest.main()