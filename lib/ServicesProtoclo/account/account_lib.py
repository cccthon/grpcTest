from __future__ import print_function
import os,sys
import grpc
sys.path.append("..")
import page.page_pb2
import page.page_pb2_grpc
import account.account_pb2
import account.account_pb2_grpc

print(sys.path)

def getCachedUserById(channel):
	stub = account_pb2_grpc.AccountSrvStub(channel)
	response = stub.GetCachedUserById(account_pb2.User(Id=2))
	print("============Greeter client received: " + response.User.AccountEmail)


channel = grpc.insecure_channel('192.168.1.148:45531')
if __name__ == '__main__':
  getCachedUserById(channel)