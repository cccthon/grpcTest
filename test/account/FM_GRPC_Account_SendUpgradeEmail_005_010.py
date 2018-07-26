#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: FM_GRPC_Account_SendUpgradeEmail_005_010
# 用例标题: 发送账号升级邮件到邮箱
# 预置条件: 
#   1.注册一个账号
# 测试步骤:
#   1.调用接口：SendUpgradeEmail发送升级会员成功的邮件
# 预期结果:
#   1.邮件发送成功，返回0
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

class SendUpgradeEmail(unittest.TestCase):
    def setUp(self):
        #连接account测试服务器
        channel = grpc.insecure_channel(userData['account_host'] + ':' + userData['account_port'])
        self.stub = account_pb2_grpc.AccountSrvStub(channel)

    def test_SendUpgradeEmail_UpMemberOkVerifyEmail(self):
        #发送UpMemberOkVerifyEmail邮件到邮箱.template在consul上面配置。key需要替换的字段。value为替换为:xx
        SendUpgradeEmail = self.stub.SendUpgradeEmail(account_pb2.UpgradeEmailRequest(Email = userData['SendActivationEmail'] ,Title = 'Followme Update Member Ok Verify Email' ,Template = 'UpMemberOkVerifyEmail',List = [account_pb2.TemplateReplaceMap(Key = "Name",Value = "test")]))
        #断言邮件发送成功，返回0
        self.assertEqual(SendUpgradeEmail.Success, 0)

    def tearDown(self):
        #清空测试环境
        #注销测试账号
        pass
        # unregister = self.stub.DeleteUserById(account_pb2.User(Id = self.accountID))
        #断言注销账号成功，返回0
        # self.assertEqual(unregister.Success, 0)

if __name__ == '__main__':
    unittest.main()
