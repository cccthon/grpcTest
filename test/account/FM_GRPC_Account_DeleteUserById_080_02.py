#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_DeleteUserById_080_002
# 用例标题: 从u_user表中删除用户
# 预置条件: 
#   1.注册一个账号
# 测试步骤:
#   1.调用接口：DeleteUserById
# 预期结果:
#   1.删除用户成功，返回成功
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

class DeleteUserById(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_DeleteUserById(self):
        #删除用户，返回成功
        DeleteUserById = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        self.assertEqual(DeleteUserById.Success, 0)
    
    def tearDown(self):
        #清空测试环境
        #注销测试账号
        # pass
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()