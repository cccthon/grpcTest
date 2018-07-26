#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SendCustomSMS_005_011
# 用例标题: 注册发送短息验证码
# 预置条件: 
#   
# 测试步骤:
#   1.调用接口：SendActiveSMS，发送验证码短信
# 预期结果:
#   3.发送成功，返回0.手机可以收到短信
# 脚本作者: shencanhui
# 写作日期: 20170815
# 以下为consul短信邮件模板名
# const (
#   SmsRegVerify        = "regVerifySMS"
#   SmsRegVerifyPyramid = "regVerifyPyramidSMS"
#   SmsUpgrade          = "Upgrade"
#   SmsLoseTradeRemind  = "LoseTradeRemindSMS"
#   SmsResetPwdByPhone  = "ResetPwdByPhone"
# )

# const (
#   EmailRegVerify          = "regVerifyEmail"
#   EmailValidateCode       = "SendEmailValidateCode"
#   EmailResetPassword      = "ResetPwdEmail"
#   EmailUpgradeInvestor    = "UpgradeInvestorVerifyEmail"
#   EmailRegOkVerify        = "RegOkVerifyEmail"
#   EmailCommon             = "CommonEmail"
#   EmailEnableMemberApply  = "EnableMemberApplyEmail"
#   EmailPlan100            = "Plan100"
#   EmailReviewMemberPass   = "ReviewMemberPassEmail"
#   EmailReviewMemberUnPass = "ReviewMemberUnPassEmail"
#   EmailUpgradeAccount4    = "UpgradeAccount4"
#   EmailUpgradeAccount5    = "UpgradeAccount5"
#   EmailUpgradeBegin4      = "UpgradeBegin4"
#   EmailUpgradeBegin5      = "UpgradeBegin5"
#   EmailUpgradeFail4       = "UpgradeFail4"
#   EmailUpgradeFail5       = "UpgradeFail5"
#   EmailUpgradeFinish4     = "UpgradeFinish4"
#   EmailUpgradeFinish5     = "UpgradeFinish5"
#   EmailUpMemberOkVerify   = "UpMemberOkVerifyEmail"
# )
#=========================================================
import grpc,sys,unittest,yaml,uuid
sys.path.append("..\\..\\lib\\ServicesProtoclo\\account")
import account_pb2
import account_pb2_grpc
import page_pb2
import page_pb2_grpc

userData = yaml.load(open('../../conf/config.yml', 'r',encoding='utf-8'))

class SendCustomSMS(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)

    def test_SendCustomSMS(self):
        #发送验证码到手机
        sendActivationEmail = self.stub.SendCustomSMS(account_pb2.CustomSMSRequest(Phone = userData['AccountMobile'], Template = 'Upgrade', List = [account_pb2.TemplateReplaceMap(Key = "UserTypeName",Value = "8888")]))
        #断言验证码发送成功，返回0
        self.assertEqual(sendActivationEmail.Success, 0)

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        pass
        # unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
