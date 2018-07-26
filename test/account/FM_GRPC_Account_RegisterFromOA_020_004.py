#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_RegisterFromOA_020_004
# 用例标题: 通过OA注册
# 预置条件: 
#   
# 测试步骤:
#   1.注册一个账号,记录id信息
# 预期结果:
#   1.检查注册成功后的user属性
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

class RegisterFromOA(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
    
    def test_RegisterByEmail(self):
        #注册一个测试账号
        register = self.stub.RegisterFromOA(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.accountID = register.Id
        #OA注册的账号，accountstatus为：2
        self.assertEqual(register.AccountStatus, 2)
        self.assertEqual(register.AccountEmail, userData['AccountEmail'])

    def tearDown(self):
        #本用例由于空密码未注册成功，所以不需要注销账号。故注销账号步骤单独写到注销成功的测试方法里
        #清空测试环境
        #注销测试账号
        # pass
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()