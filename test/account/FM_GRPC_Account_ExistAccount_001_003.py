#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_ExistAccount_001_003
# 用例标题: 检查用户是否存在
# 预置条件: 
#   1.注册一个账号,记录id信息
# 测试步骤:
#   1.调用接口：ExistAccount
#   2.通过用户名、email、手机号、昵称来查询存在与不存在的账号信息
# 预期结果:
#   1.账号信息存在。返回："already existed"
#   2.账号信息不存在。返回："user not existed"
# 脚本作者: shencanhui
# 写作日期: 20170904
#=========================================================
import grpc,sys,unittest,yaml
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class ExistAccount(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_ExistAccount_byEmail(self):
        #通过email查询已经存在的用户
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserExisted_returnCode'],self.stub.ExistAccount,account_pb2.User(AccountEmail = userData['AccountEmail']))
        
    def test_ExistAccount_byInvalidEmail(self):
        #通过错误的email查询用户
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserNotExisted_returnCode'],self.stub.ExistAccount,account_pb2.User(AccountEmail = 'invalidEmail@email.com'))
        

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)


if __name__ == '__main__':
    unittest.main()