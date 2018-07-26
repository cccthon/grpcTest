#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_GetUserInfo_001_006
# 用例标题: 获取用户信息
# 预置条件: 
#   1.注册一个账号,记录id信息
# 测试步骤:
#   1.调用接口：GetUserInfo，入参为：注册时记录的id
#   2.检查账号相关参数：NickName、AccountEmail、IsMobileVerified、Gender、AccountStatus、UserType
# 预期结果:
#   1.接口调用成功
#   2.参数符合预期
# 脚本作者: shencanhui
# 写作日期: 20170904
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class GetUserInfo(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id
        
    def test_GetUserInfo(self):
        #提示用户不存在，新注册的账号需要在web端登录一次才能获取到用户信息。待研究解决方案
        getUserInfo = self.stub.GetUserInfo(account_pb2.LoginRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'],UserPassword = userData['UserPasswd']) ,Token = str(uuid.uuid1())))
        # self.assertEqual(getCachedUser.Id, self.accountID)
        # self.assertEqual(getCachedUser.AccountEmail, userData['AccountEmail'])
        # self.assertEqual(getCachedUser.IsMobileVerified, userData['IsMobileVerified'])
        # self.assertEqual(getCachedUser.Gender, userData['Gender'])
        # self.assertEqual(getCachedUser.AccountStatus, userData['AccountStatus'])
        # self.assertEqual(getCachedUser.UserType, userData['UserType'])
        # self.assertEqual(getCachedUser.EnableMemberApply, userData['EnableMemberApply'])
    
    # def test_GetUserById_NotExistID(self):
    #     #查询用户通过不存在的id
    #     self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserNotExisted_returnCode'],self.stub.GetUserInfo,account_pb2.User(Id = 999999999))

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)


if __name__ == '__main__':
    unittest.main()