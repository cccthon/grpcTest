#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_GetActivationByObj _001_008
# 用例标题: 获取验证码到邮箱
# 预置条件: 
#   1.发送验证码到邮箱   
# 测试步骤:
#   1.调用接口：GetActivationByObj ,获取验证码
# 预期结果:
#   1.验证码获取成功，与发送的一致
# 脚本作者: shencanhui
# 写作日期: 20171019
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class GetActivationByObj(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)
         #注册一个测试账号
        register = self.stub.RegisterByEmail(account_pb2.RegisterUserRequest(User = account_pb2.User(AccountEmail = userData['AccountEmail'] ,UserPassword = userData['UserPasswd'])))
        self.assertEqual(register.AccountStatus, userData['AccountStatus'])
        self.accountID = register.Id

    def test_SendActivationEmail(self):
        #发送验证码邮件到邮箱
        sendActivationEmail = self.stub.SendActivationEmail(account_pb2.SendActivationEmailRequest(UserId = self.accountID, ActivationCode = userData['ActivationCode'], Email = userData['SendActivationEmail'] ,Subject = userData['Subject'] ))
        #断言验证码邮件发送成功，返回0
        self.assertEqual(sendActivationEmail.Success, 0)
        #获取验证码
        getActivationByObj = self.stub.GetActivationByObj(account_pb2.ActivationRequest(ObjectId = self.accountID))
        vercode = getActivationByObj.VerCode
        activationCode = getActivationByObj.ActivationCode
        self.assertEqual(getActivationByObj.ActivationCode, userData['ActivationCode'])
        #激活账号。
        #AccountStatus: 0 新申请, 1 审核中, 2 正常, 3 锁定（此时交易员才可提取服务费）, 4 注销, 5 未激活,6 注销
        validateEmailLink = self.stub.ValidateEmailLink(account_pb2.ValidateEmailLinkRequest(UserId = self.accountID, VerCode = vercode,ActivationCode = activationCode,Token = str(uuid.uuid1())))
        self.assertEqual(validateEmailLink.Success, 0)

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
