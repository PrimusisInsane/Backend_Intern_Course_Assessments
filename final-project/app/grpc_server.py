import os
import sys
from concurrent import futures

import grpc

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.repositories.user_repo import get_user_by_id
from proto import user_lookup_pb2, user_lookup_pb2_grpc


class UserLookupServicer(user_lookup_pb2_grpc.UserLookupServiceServicer):
    def GetUser(self, request, context):
        db = SessionLocal()
        try:
            user = get_user_by_id(db, request.user_id)
            if not user:
                return user_lookup_pb2.UserLookupResponse(found=False)
            return user_lookup_pb2.UserLookupResponse(
                id=user.id, name=user.name, email=user.email, role=user.role, found=True
            )
        finally:
            db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    user_lookup_pb2_grpc.add_UserLookupServiceServicer_to_server(UserLookupServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC UserLookupService running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
