#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_RegisterByMobileOrEmail_020_003
# 用例标题: 通过手机或邮件注册
# 预置条件: 
#   
# 测试步骤:
#   1.注册一个账号,记录id信息
# 预期结果:
#   1.检查注册成功后的user属性
# 脚本作者: shencanhui
# 写作日期: 20171018
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class RegisterByMobileOrEmail(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
    
    def test_RegisterByMobileOrEmail_email(self):
        #注册一个测试账号
        register = self.stub.RegisterByMobileOrEmail(account_pb2.RegisterByMobileOrEmailRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.assertEqual(register.AccountEmail, userData['AccountEmail'])
        self.accountID = register.Id
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

    def test_RegisterByMobileOrEmail_emailNullPWD(self):
        #注册一个测试账号,不输入密码。返回密码无效
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.RegisterByMobileOrEmail,account_pb2.RegisterByMobileOrEmailRequest(User = account_pb2.User(AccountEmail = 'testAccount1@test.com')))

    def test_RegisterByMobileOrEmail_mobile(self):
        #通过手机号码注册一个测试账号。为了保证手机号码未注册，故此处使用不存在的11位手机号。保证注册成功即可
        register = self.stub.RegisterByMobileOrEmail(account_pb2.RegisterByMobileOrEmailRequest(User = account_pb2.User(AccountMobile = '98745612300' ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountMobile, '98745612300')
        self.accountID = register.Id
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

    def test_RegisterByMobileOrEmail_mobileNullPWD(self):
        #注册一个测试账号,不输入密码。返回密码无效
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.RegisterByMobileOrEmail,account_pb2.RegisterByMobileOrEmailRequest(User = account_pb2.User(AccountMobile = '13888888888')))


    def tearDown(self):
        #本用例由于空密码未注册成功，所以不需要注销账号。故注销账号步骤单独写到注销成功的测试方法里
        #清空测试环境
        #注销测试账号
        pass
        # unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()