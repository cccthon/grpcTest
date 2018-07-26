#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_MarketingRegisterByMobile_090_001
# 用例标题: MarketingRegisterByMobile
# 预置条件: 
#   
# 测试步骤:
#   1.注册一个账号,记录id信息
# 预期结果:
#   1.检查注册成功后的user属性
# 脚本作者: shencanhui
# 写作日期: 20171018
# 活动专用接口，已经废弃
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class MarketingRegisterByMobile(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.assertEqual(register.AccountEmail, userData['AccountEmail'])
        self.accountID = register.Id
    
    def test_MarketingRegisterByMobile(self):
        #注册一个测试账号
        MarketingRegister = self.stub.MarketingRegisterByMobile(account_pb2.MarketingRegisterByMobileRequest(User = account_pb2.User(AccountMobile = userData['AccountMobile'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(MarketingRegister.IsMobileVerified, True)

    # def test_RegisterByEmail_nullPWD(self):
    #     #注册一个测试账号,不输入密码。返回密码无效
    #     self.assertRaisesRegex(grpc._channel._Rendezvous,userData['PasswdInvalid_returnCode'],self.stub.MarketingRegisterByMobile,account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = 'testAccount1@test.com')))

    # def test_RegisterByEmail_lessPWD(self):
    #     #注册一个测试账号，超短密码。返回用户无效
    #     self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.MarketingRegisterByMobile,account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = 'testAccount2@test.com', UserPassword = 'f')))

    # def test_RegisterByEmail_morePWD(self):
    #     #注册一个测试账号，超长密码。返回用户无效
    #     self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.MarketingRegisterByMobile,account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = 'testAccount2@test.com', UserPassword = 'f11111111111111111111111111111111111111111')))

    def tearDown(self):
        #本用例由于空密码未注册成功，所以不需要注销账号。故注销账号步骤单独写到注销成功的测试方法里
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()