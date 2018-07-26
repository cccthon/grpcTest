#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_GetUserListByRegisterTime_001_008
# 用例标题: 通过注册时间获取用户列表信息
# 预置条件: 
#   1.注册一个账号，记录注册时间
# 测试步骤:
#   1.调用接口：GetUserListByRegisterTime通过注册时间获取用户列表
# 预期结果:
#   1.接口调用成功
#   2.参数符合预期
# 脚本作者: shencanhui
# 写作日期: 20171019
#=========================================================
import grpc,sys,unittest,yaml,time
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class GetUserListByRegisterTime(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User( AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id
        self.CreateTime = register.CreateTime - 86400
        print(register)
        print(self.CreateTime)
        # register1 = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User( AccountEmail = 'test111@test.com' ,UserPassword = userData['UserPasswd'])))
        # self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        # self.accountID1 = register1.Id
        # self.CreateTime1 = register1.CreateTime

    def test_GetUserListByRegisterTime(self):
        #parse time 将注册时间戳转换成2017-10-19 22:25:32格式
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.CreateTime))
        print(timestamp)
        #通过昵称获取用户列表相关信息
        GetUserListByRegisterTime = self.stub.GetUserListByRegisterTime(account_pb2.GetUserListRequest(RegisterTime = timestamp))
        print(GetUserListByRegisterTime)
        #返回用户列表
        # self.assertEqual(GetUserListByRegisterTime.List[0].User.CreateTime, self.CreateTime)

    # def test_GetUserListByRegisterTime_NotExistName(self):
    #     #查询用户通过不存在的nickName
    #     self.assertRaisesRegex(grpc._channel._Rendezvous,userData['UserNotExisted_returnCode'],self.stub.GetUserListByRegisterTime,account_pb2.User(NickName = 'testssssss'))

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)
        # unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID1))
        # #断言注销账号成功，返回0
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
