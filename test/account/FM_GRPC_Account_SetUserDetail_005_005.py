#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SetUserDetail_005_005
# 用例标题: 设置描述信息
# 预置条件: 
#   1.注册一个账号,记录id信息
# 测试步骤:
#   1.调用接口：SetUserDetail，设置性别：2保密；0男；1女；小于0大于2默认为2
#   2.调用接口：SetUserDetail，设置血型：0 A型；1 B型；2 AB型；3 o型；小于0大于3默认为A型
#   3.调用接口：SetUserDetail，设置介绍：中、英、数字、特殊字符；空介绍
#   4.调用接口：SetUserDetail，设置生日：时间戳
# 预期结果:
#   1.SetDescription成功，返回0
#   2.设置后获取到的用户信息正确
# 脚本作者: shencanhui
# 写作日期: 20170905
#=========================================================
import grpc,sys,unittest,yaml
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))



class SetUserDetail(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_SetUserDetail_Null(self):
        #设置用户详细信息：啥都不设置
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID))
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)


    def test_SetUserDetail_Gender_Male(self):
        #设置用户详细信息：性别男：0
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Gender = 0))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Gender, 0)

    def test_SetUserDetail_Gender_Female(self):
        #设置用户详细信息：性别女1
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Gender = 1))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Gender, 1)

    def test_SetUserDetail_Gender_Secrecy(self):
        #设置用户详细信息：性别保密2
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Gender = 2))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Gender, 2)

    def test_SetUserDetail_Gender_More(self):
        #设置用户详细信息：性别大于2时默认为2
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Gender = 3))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Gender, 2)

    def test_SetUserDetail_Gender_Less(self):
        #设置用户详细信息：性别少于0时默认为2
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Gender = -1))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Gender, 2)

    def test_SetUserDetail_BloodGroup_A(self):
        #设置用户详细信息：血型0为A型
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,BloodGroup = 0))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.BloodGroup, 0)

    def test_SetUserDetail_BloodGroup_B(self):
        #设置用户详细信息：血型1为B型
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,BloodGroup = 1))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.BloodGroup, 1)

    def test_SetUserDetail_BloodGroup_AB(self):
        #设置用户详细信息：血型2为AB型
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,BloodGroup = 2))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.BloodGroup, 2)

    def test_SetUserDetail_BloodGroup_o(self):
        #设置用户详细信息：血型3为o型
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,BloodGroup = 3))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.BloodGroup, 3)

    def test_SetUserDetail_BloodGroup_More(self):
        #设置用户详细信息：血型值大于3时默认为0
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,BloodGroup = 4))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.BloodGroup, 0)

    def test_SetUserDetail_BloodGroup_Less(self):
        #设置用户详细信息：血型值小于于0时默认为0
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,BloodGroup = -1))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.BloodGroup, 0)

    def test_SetUserDetail_Introduction(self):
        #设置用户详细信息：介绍包括：中文、字母、数字、特殊字符
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Introduction = '介绍this123!@#'))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Introduction, '介绍this123!@#')

    def test_SetUserDetail_Introduction_Null(self):
        #设置用户详细信息：介绍为空
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Introduction = ''))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Introduction, '')

    def test_SetUserDetail_Birthday(self):
        #设置用户详细信息：生日为时间戳
        setUserDetail = self.stub.SetUserDetail(account_pb2.User(Id = self.accountID,Birthday = 123456))
        getCachedUser = self.stub.GetCachedUserById(account_pb2.User(Id = self.accountID)).User
        #设置成功，返回值为：0
        self.assertEqual(setUserDetail.Success, 0)
        self.assertEqual(getCachedUser.Birthday, 123456)

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)


if __name__ == '__main__':
    unittest.main()