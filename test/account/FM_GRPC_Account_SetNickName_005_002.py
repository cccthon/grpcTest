#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SetNickName_005_002
# 用例标题: 设置nickname
# 预置条件: 
#   1.注册一个账号,记录id信息
# 测试步骤:
#   1.调用接口：SetNickName 设置中文；超长；超短昵称
#   2.调用接口：SetNickName 设置无效的昵称(少于或大于64个字符)；特殊字符
# 预期结果:
#   1.Nickname设置成功，返回0
#   1.Nickname设置失败，invalid userinfo
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

class SetNickName(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_SetNickName(self):
        #设置用户昵称
        setNickName = self.stub.SetNickName(account_pb2.User(Id = self.accountID,NickName = userData['NickName']))
        #检查设置成功后，返回值为：0
        self.assertEqual(setNickName.Success, 0)
    
    def test_SetNickName_withChineseStr(self):
        #设置带中文的昵称
        setNickName = self.stub.SetNickName(account_pb2.User(Id = self.accountID,NickName = '我是中文昵称_'))
        #检查设置成功后，返回值为：0
        self.assertEqual(setNickName.Success, 0)

    def test_SetNickName_withMaxStr(self):
        #设置64个字符的昵称
        setNickName = self.stub.SetNickName(account_pb2.User(Id = self.accountID,NickName = '1111111111111111111111111111111111111111111111111111111111112345'))
        #检查设置成功后，返回值为：0
        self.assertEqual(setNickName.Success, 0)

    def test_SetNickName_withMinStr(self):
        #设置3个字符的昵称
        setNickName = self.stub.SetNickName(account_pb2.User(Id = self.accountID,NickName = '我a6'))
        #检查设置成功后，返回值为：0
        self.assertEqual(setNickName.Success, 0)

    def test_SetNickName_withSpecialStr(self):
        #设置昵称带特殊字符，设置失败
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.SetNickName,account_pb2.User(NickName = '!@#$%^'))

    def test_SetNickName_LessStr(self):
        #设置昵称少于3个字符
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.SetNickName,account_pb2.User(NickName = 'a3'))

    def test_SetNickName_MoreStr(self):
        #设置昵称大于65个字符
        self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserInvalid_returnCode'],self.stub.SetNickName,account_pb2.User(NickName = '11111111111111111111111111111111111111111111111111111111111123456'))

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)


if __name__ == '__main__':
    unittest.main()