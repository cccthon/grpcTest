import os,sys
import grpc
sys.path.append("..")
print(sys.path)
import member.member_pb2
import member.member_pb2_grpc
import member_pb2_grpc
import member_pb2

def getUserInfoByUserId(channel):
	stub = member_pb2_grpc.MemberSrvStub(channel)
	response = stub.GetUserInfoByUserId(member_pb2.GetUserInfoByUserIdRequest(userID="1"))
	print("============Greeter client received: " + response.Model.NickName)

def regUserMemberInfo(channel):
    stub = member_pb2_grpc.MemberSrvStub(channel)
    response = stub.RegUserMemberInfo(member_pb2.RegUserMemberInfoRequest(userId=1,memberId=72))
    print("============Greeter client received: " + response.Model.ParentIds)

channel = grpc.insecure_channel('192.168.1.148:10086')
# channel = grpc.insecure_channel('192.168.0.59:33431')

if __name__ == '__main__':
  # getUserInfoByUserId(channel)
  regUserMemberInfo(channel)