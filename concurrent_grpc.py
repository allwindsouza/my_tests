import grpc
import threading
import time

from concurrent import futures

# Import the generated gRPC client and server modules
import grpc_module_pb2 as pb2
import grpc_module_pb2_grpc as pb2_grpc


# Define the gRPC server class
class HelloServiceServicer(pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        # Print "Hello, World!"
        print("Hello, World! \n")

        # Get the current timestamp
        timestamp = int(time.time())
        time.sleep(1)

        # Return a response with the timestamp
        return pb2.HelloResponse(message='Hello, World!', timestamp=timestamp)


# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
pb2_grpc.add_HelloServiceServicer_to_server(HelloServiceServicer(), server)
server.add_insecure_port('[::]:50051')

# Start the gRPC server in a separate thread
server_thread = threading.Thread(target=server.start)
server_thread.start()


# Define a function to make gRPC calls
def make_grpc_call():
    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # Create a gRPC stub
    stub = pb2_grpc.HelloServiceStub(channel)

    # Make a gRPC call
    response = stub.SayHello(pb2.HelloRequest())

    # Print the response
    print(response.message)
    print("\n Timestamp:", response.timestamp)


# Create multiple threads to make concurrent gRPC calls
num_threads = 10
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=make_grpc_call)
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Stop the gRPC server
server.stop(None)
