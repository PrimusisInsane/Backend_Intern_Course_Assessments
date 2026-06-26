import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proto import user_lookup_pb2
from proto import user_lookup_pb2_grpc


def get_user(user_id: int):
    channel = grpc.insecure_channel("localhost:50051")
    stub = user_lookup_pb2_grpc.UserLookupServiceStub(channel)
    request = user_lookup_pb2.UserLookupRequest(user_id=user_id)
    response = stub.GetUser(request)
    return response


if __name__ == "__main__":
    result = get_user(1)
    print(f"Found: {result.found}")
    print(f"ID: {result.id}")
    print(f"Name: {result.name}")
    print(f"Email: {result.email}")
    print(f"Role: {result.role}")