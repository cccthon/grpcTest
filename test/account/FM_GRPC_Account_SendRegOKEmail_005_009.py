#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SendRegOkEmail_005_009
# 用例标题: 发送注册成功的邮件到邮件
# 预置条件: 
#   1.注册一个账号
# 测试步骤:
#   1.调用接口：SendRegOkEmail发送账号注册成功的邮件
# 预期结果:
#   1.邮件发送成功，返回0
# 脚本作者: shencanhui
# 写作日期: 20171020
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class SendRegOkEmail(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_SendUpgradeInvestorEmail(self):
        #发送注册成功邮件到邮箱
        SendRegOkEmail = self.stub.SendRegOkEmail(account_pb2.SendActivationEmailRequest(UserId = self.accountID,ActivationCode = userData['ActivationCode'],Email = userData['SendActivationEmail'] ,Subject = 'Followme注册成功' ))
        #断言邮件发送成功，返回0
        self.assertEqual(SendRegOkEmail.Success, 0)

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
