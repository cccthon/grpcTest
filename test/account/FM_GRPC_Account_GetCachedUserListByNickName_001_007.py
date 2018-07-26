#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_GetCachedUserListByNickName_001_007
# 用例标题: 通过昵称获取用户列表信息
# 预置条件: 
#   1.已经存在昵称为：account_test的账号
# 测试步骤:
#   1.调用接口：GetCachedUserListByNickName
#   2.检查账号相关参数：id、AccountEmail、IsMobileVerified、Gender、AccountStatus、UserType
# 预期结果:
#   1.接口调用成功
#   2.参数符合预期
# 脚本作者: shencanhui
# 写作日期: 20171019
#=========================================================
import grpc,sys,unittest,yaml
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class GetCachedUserListByNickName(unittest.TestCase):
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

    def test_GetCachedUserListByNickName(self):
        #通过昵称获取用户列表相关信息
        GetCachedUserListByNickName = self.stub.GetCachedUserListByNickName(account_pb2.User(NickName = userData['NickName']))
        #返回用户列表
        self.assertEqual(GetCachedUserListByNickName.List[0].User.NickName, userData['NickName'])


    def test_GetCachedUserListByNickName_NotExistName(self):
        #查询用户通过不存在的nickName
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserNotExisted_returnCode'],self.stub.GetCachedUserListByNickName,account_pb2.User(NickName = 'testssssss'))


    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
