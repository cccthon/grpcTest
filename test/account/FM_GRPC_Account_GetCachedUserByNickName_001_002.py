#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_GetCachedUserByNickName_001_002
# 用例标题: 通过昵称获取用户信息
# 预置条件: 
#   1.已经存在昵称为：account_test的账号
# 测试步骤:
#   1.调用接口：GetCachedUserByNickName，入参为：account_test
#   2.检查账号相关参数：id、AccountEmail、IsMobileVerified、Gender、AccountStatus、UserType
# 预期结果:
#   1.接口调用成功
#   2.参数符合预期
# 脚本作者: shencanhui
# 写作日期: 20170815
#=========================================================
import grpc,sys,unittest,yaml
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class GetCachedUserByNickName(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User( AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id
        #设置测试账号的昵称
        setNickName = self.stub.SetNickName(account_pb2.User(Id = self.accountID,NickName = userData['NickName']))
        #检查设置成功后，返回值为：0
        self.assertEqual(setNickName.Success, 0)

    def test_GetCachedUserByNickName(self):
        #通过昵称获取账号相关信息
        getCachedUser = self.stub.GetCachedUserByNickName(account_pb2.User(NickName = userData['NickName'])).User
        #断言该账号用户id为setup步骤注册时生成的id
        self.assertEqual(getCachedUser.Id,  self.accountID)
        self.assertEqual(getCachedUser.AccountEmail, userData['AccountEmail'])
        self.assertEqual(getCachedUser.NickName, userData['NickName'])

    def test_GetCachedUserByNickName_NotExistName(self):
        #查询用户通过不存在的nickName
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserNotExisted_returnCode'],self.stub.GetCachedUserByNickName,account_pb2.User(NickName = 'testssssss'))


    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
