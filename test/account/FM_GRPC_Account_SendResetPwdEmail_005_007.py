#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SendResetPwdEmail_005_007
# 用例标题: 发送重新设置密码邮件到邮箱
# 预置条件: 
#   1.
# 测试步骤:
#   1.调用接口：SendResetPwdEmail，发送重新设置密码邮件
# 预期结果:
#   1.发送重新设置密码邮件成功
# 脚本作者: shencanhui
# 写作日期: 20171020
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class SendResetPwdEmail(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_SendResetPwdEmail(self):
        #发送重新设置密码邮件到邮箱
        SendResetPwdEmail = self.stub.SendResetPwdEmail(account_pb2.SendActivationEmailRequest(UserId = self.accountID,ActivationCode = userData['ActivationCode'],Email = userData['SendActivationEmail'] ,Subject = 'Followme 密码重置' ))
        #断言邮件发送成功，返回0
        self.assertEqual(SendResetPwdEmail.Success, 0)
       
    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
