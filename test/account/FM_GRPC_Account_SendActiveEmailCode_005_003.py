#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SendActiveEmailCode_005_003
# 用例标题: 注册发验证码到邮箱
# 预置条件: 
#   
# 测试步骤:
#   1.调用接口：SendActiveEmailCode，发送验证码短信
# 预期结果:
#   3.发送成功，返回0.手机可以收到短信
# 脚本作者: shencanhui
# 写作日期: 20170815
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class SendActiveEmailCode(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        # #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_SendActiveSMS(self):
        #发送验证码邮件到邮箱
        sendActivationEmail = self.stub.SendActiveEmailCode(account_pb2.SendEmailCodeRequest(Email = userData['SendActivationEmail'], ActiveCode = userData['ActivationCode']))
        #断言验证码发送成功，返回0
        self.assertEqual(sendActivationEmail.Success, 0)

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        # pass
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
