#!/usr/bin/env python

import asyncio
import grpc
import adder_pb2
import adder_pb2_grpc
import common

class Adder(adder_pb2_grpc.AdderServicer):

    async def Add(self, request, context):
        reply = adder_pb2.AddReply(sum=request.a + request.b)
        print(f"Server: {request.a} + {request.b} = {reply.sum}")
        return reply

async def main():
    args = common.parse_command_line_arguments("server")
    server = grpc.aio.server()
    server_address = f"{args.server_host}:{args.server_port}"
    if args.server_authenticated:
        print("Server is authenticated by client")
        server_private_key = open("server.key", "br").read()
        server_certificate = open("server.crt", "br").read()
        credentials = grpc.ssl_server_credentials([(server_private_key, server_certificate)])
        server.add_secure_port(server_address, credentials)
    else:
        print("Server is not authenticated by client")
        server.add_insecure_port(server_address)
    adder_pb2_grpc.add_AdderServicer_to_server(Adder(), server)
    await server.start()
    print(f"Started server on {server_address}")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(main())