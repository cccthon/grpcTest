#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SetFavorite_005_003
# 用例标题: 设置喜好
# 预置条件: 
#   1.注册一个账号,记录id信息
# 测试步骤:
#   1.调用接口：SetFavorite 对TradeVariety；TradeExperience；RiskPropensity设置中文；
#               英文；特殊字符。不对长度进行测试，由数据库约束
# 预期结果:
#   1.SetFavorite成功，返回0
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

class SetFavorite(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_SetFavorite_TradeVariety(self):
        #设置交易多样化。字符与空字符
        setFavorite1 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,TradeVariety = '我123abc!@#'))
        setFavorite2 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,TradeVariety = ''))
        #设置成功，返回值为：0
        self.assertEqual(setFavorite1.Success, 0)
        self.assertEqual(setFavorite2.Success, 0)
    
    def test_SetFavorite_TradeExperience(self):
        #设置交易经验，字符与空字符
        setFavorite1 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,TradeExperience = '我123abc!@#'))
        setFavorite2 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,TradeExperience = ''))
        #设置成功，返回值为：0
        self.assertEqual(setFavorite1.Success, 0)
        self.assertEqual(setFavorite2.Success, 0)

    def test_SetFavorite_RiskPropensity(self):
        #设置风险趋势。字符与空字符
        setFavorite1 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,RiskPropensity = '我123abc!@#'))
        setFavorite2 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,RiskPropensity = ''))
        #设置成功，返回值为：0
        self.assertEqual(setFavorite1.Success, 0)
        self.assertEqual(setFavorite2.Success, 0)
    
    def test_SetFavorite_MultiPar(self):
        #设置风险趋势,多个入参
        setFavorite1 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,TradeVariety = '我123abc!@#',TradeExperience = '我123abc!@#'))
        setFavorite2 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,TradeVariety = '我123abc!@#',RiskPropensity = '我123abc!@#'))
        setFavorite3 = self.stub.SetFavorite(account_pb2.User(Id = self.accountID,TradeVariety = '我123abc!@#',TradeExperience = '我123abc!@#',RiskPropensity = '我123abc!@#'))
        #设置成功，返回值为：0
        self.assertEqual(setFavorite1.Success, 0)
        self.assertEqual(setFavorite2.Success, 0)
        self.assertEqual(setFavorite3.Success, 0)

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)


if __name__ == '__main__':
    unittest.main()