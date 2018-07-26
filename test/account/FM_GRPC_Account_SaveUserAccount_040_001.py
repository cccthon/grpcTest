#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SaveUserAccount_040_001
# 用例标题: 将注册的不需要审核的用户提取到t_useraccount表
# 预置条件: 
#   
# 测试步骤:
#   1.调用该接口SaveUserAccount将新注册的账号提取到t_useraccount表
# 预期结果:
#   1.返回成功
# 脚本作者: shencanhui
# 写作日期: 20171018
#=========================================================
import grpc,sys,unittest,yaml,uuid,random
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
sys.path.append("..\\..\\lib\\public")
import public
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class SaveUserAccount(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)

    def test_SaveUserAccount(self):
        #将注册的用户提取到t_useraccount表
        SaveUserAccount = self.stub.SaveUserAccount(account_pb2.SaveUserAccountRequest(User = account_pb2.User(AccountEmail = 'fm_copytrade_001@126.com'),
            BrokerID = 5, MT4Account = '996996996', IsTrader = 1, AccountCreateType = 0, IsBind = 1))
        self.assertEqual(SaveUserAccount.Success, 0)
        #成功后，将该数据从数据库删除。待下次使用同样的数据测试不报错
        public.delete_db_data(userData['mssql_host'],userData['mssql_port'],userData['FM_OS_DB'],userData['db_user'],userData['db_passwd'],"delete from [" + userData['FM_OS_DB'] + "].[dbo].[T_UserAccount] where MT4Account='996996996'")

    def tearDown(self):
        #本用例由于空密码未注册成功，所以不需要注销账号。故注销账号步骤单独写到注销成功的测试方法里
        #清空测试环境
        #注销测试账号
        pass
        # unregister = self.stub.DeleteUserById(account_pb2.User(Id = 7679))
        #断言注销账号成功，返回0
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()