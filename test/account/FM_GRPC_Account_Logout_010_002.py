#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_Logout_010_001
# 用例标题: 退出登录
# 预置条件: 
#   1.注册一个账号,激活并登录
# 测试步骤:
#   1.调用接口：Logout登出
# 预期结果:
#   1.登出成功
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

class Logout(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
        #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_Logout(self):
        #新注册的账号需要先激活才能登录
        #发送验证码邮件到邮箱
        sendActivationEmail = self.stub.SendActivationEmail(account_pb2.SendActivationEmailRequest(UserId = self.accountID,ActivationCode = userData['ActivationCode'],Email = userData['SendActivationEmail'] ,Subject = userData['Subject'] ))
        #断言验证码邮件发送成功，返回0
        self.assertEqual(sendActivationEmail.Success, 0)
        #获取验证码
        getActivationByObj = self.stub.GetActivationByObj(account_pb2.ActivationRequest(ObjectId = self.accountID))
        vercode = getActivationByObj.VerCode
        activationCode = getActivationByObj.ActivationCode
        #激活账号。
        #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
        validateEmailLink = self.stub.ValidateEmailLink(account_pb2.ValidateEmailLinkRequest(UserId = self.accountID, VerCode = vercode,ActivationCode = activationCode,Token = str(uuid.uuid1())))
        self.assertEqual(validateEmailLink.Success, 0)
        #登录成功
        token = str(uuid.uuid1())
        Login = self.stub.Login(account_pb2.LoginRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'],UserPassword = userData['UserPasswd']) ,Token = token))
        self.assertEqual(Login.Id, self.accountID)
        self.assertEqual(Login.AccountEmail, userData['AccountEmail'])
        #退出登录
        Logout = self.stub.Logout(account_pb2.TokenAndVcode(Token = token))
        self.assertEqual(Logout.Success, 0)

   
    def tearDown(self):
        #清空测试环境
        #注销测试账号
        # pass
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()