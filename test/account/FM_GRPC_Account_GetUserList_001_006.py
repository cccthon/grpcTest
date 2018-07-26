#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_GetUserList_001_006
# 用例标题: 批量获取用户信息
# 预置条件: 
#   1.注册一个账号,记录id信息
# 测试步骤:
#   1.调用接口：GetUserList
# 预期结果:
#   1.接口调用成功
#   2.批量返回用户信息
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

class GetUserList(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id
        #注册一个测试账号
        register1 = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = 'test123@test.com' ,UserPassword = '123456')))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID1 = register1.Id

    def test_GetUserList(self):
        GetUserList = self.stub.GetUserList(account_pb2.GetUserListRequest(List = [account_pb2.User(Id = self.accountID),account_pb2.User(Id = self.accountID1)]))
        self.assertEqual(GetUserList.List[0].User.AccountEmail, userData['AccountEmail'])
        self.assertEqual(GetUserList.List[1].User.AccountEmail, "test123@test.com")

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        # pass
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)
        unregister1 = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID1))
        #断言注销账号成功，返回0
        self.assertEqual(unregister1.Success, 0)
if __name__ == '__main__':
    unittest.main()