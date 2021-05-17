#!/usr/bin/env python

import asyncio
import random
import grpc
import adder_pb2
import adder_pb2_grpc
import common

def make_credentials(args):
    assert args.authentication in ["server", "mutual"]
    assert args.signer in ["self", "root", "intermediate"]
    if args.signer == "self":
        root_certificate_for_server = open("server.crt", "br").read()
    elif args.signer == "root":
        root_certificate_for_server = open("root.crt", "br").read()
    else:
        root_certificate_for_server = open("intermediate.crt", "br").read()
    if args.authentication == "mutual":
        client_private_key = open("client.key", "br").read()
        client_certificate = open("client.crt", "br").read()
        credentials = grpc.ssl_channel_credentials(root_certificate_for_server, client_private_key,
                                                   client_certificate)
    else:
        credentials = grpc.ssl_channel_credentials(root_certificate_for_server)
    return credentials

async def main():
    args = common.parse_command_line_arguments("server")
    print(common.authentication_and_signer_summary(args))
    server_address = f"{args.server_host}:{args.server_port}"
    if args.authentication == "none":
        channel = grpc.aio.insecure_channel(server_address)
    else:
        credentials = make_credentials(args)
        channel = grpc.aio.secure_channel(server_address, credentials)
    stub = adder_pb2_grpc.AdderStub(channel)
    print(f"Connecting to server on {server_address}")
    a = random.randint(1, 10001)
    b = random.randint(1, 10001)
    request = adder_pb2.AddRequest(a=a, b=b)
    reply = await stub.Add(request)
    assert reply.sum == a + b
    print(f"Client: {request.a} + {request.b} = {reply.sum}")
    await channel.close()

if __name__ == "__main__":
    asyncio.run(main())
