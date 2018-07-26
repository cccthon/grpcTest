#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_ResetPasswordAndActivationAndActivation_005_007 
# 用例标题: 修改账号密码
# 预置条件: 
#   1.注册一个账号,记录id信息
# 测试步骤:
#   1.调用接口：ResetPasswordAndActivation，修改账号密码
# 预期结果:
#   1.无返回值，接口调用成功即可
# 脚本作者: shencanhui
# 写作日期: 20170905
# 此接口未调通
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class ResetPasswordAndActivation(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_ResetPasswordAndActivation(self):
        #修改密码成功,返回0
        resetPasswordAndActivation = self.stub.ResetPasswordAndActivation(account_pb2.ResetPasswordAndActivationRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'],UserPassword = userData['UserPasswd']),ID = 1))
        # ResetPasswordAndActivation = self.stub.test_ResetPasswordAndActivation(account_pb2.User(AccountEmail = userData['AccountEmail'],UserPassword = 'abc123汉字'))
        self.assertEqual(resetPasswordAndActivation.Success, 0)

    # def test_ResetPasswordAndActivation_SpecialChar(self):
    #     #修改密码为带特殊字符
    #     ResetPasswordAndActivation = self.stub.ResetPasswordAndActivation(account_pb2.User(AccountEmail = userData['AccountEmail'],UserPassword = '!@#$%^'))
    #     self.assertEqual(ResetPasswordAndActivation.Success, 0)

    # def test_ResetPasswordAndActivation_Null(self):
    #     #修改密码为:空密码
    #     self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.ResetPasswordAndActivation,account_pb2.User(AccountEmail = userData['AccountEmail'],UserPassword = ''))

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)


if __name__ == '__main__':
    unittest.main()