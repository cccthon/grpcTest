#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_UpdateUserInfoAndUserAccount_030_002
# 用例标题: 审核处于oa审核中的用户
# 预置条件: 
#   
# 测试步骤:
#   1.使用接口UpdateUserInfoAndUserAccount审核oa中待审核的账号
# 预期结果:
#   1.审核通过后，返回账号属性
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

class UpdateUserInfoAndUserAccount(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)

    def test_UpdateUserInfoAndUserAccount(self):
        UpdateUserInfo = self.stub.UpdateUserInfoAndUserAccount(account_pb2.UpdateUserInfoAndUserAccountRequest(
            User = account_pb2.User(Id = 1371, AccountEmail = 'fm_copytrade_004@126.com'),
            UserAccount = account_pb2.UserAccount(UserType = 1, BrokerId = 4, MT4Account = '995995995', MT4Password = '123456', ManagerAccount = 'd16994402')))
        self.assertEqual(UpdateUserInfo.MT4Account, '995995995')
        self.assertEqual(UpdateUserInfo.BrokerId, 4)
        #成功后，将改数据从数据库删除。待下次使用同样的数据测试不报错
        public.delete_db_data(userData['mssql_host'],userData['mssql_port'],userData['FM_OS_DB'],userData['db_user'],userData['db_passwd'],"delete from [" + userData['FM_OS_DB'] + "].[dbo].[T_UserAccount] where MT4Account='995995995'")

    def tearDown(self):
        #本用例由于空密码未注册成功，所以不需要注销账号。故注销账号步骤单独写到注销成功的测试方法里
        #清空测试环境
        #注销测试账号
        pass
        # unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()