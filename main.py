import asyncio
from asyncua import ua, uamethod, Server
async def main():

    server = Server()
    await server.init()

    server.set_endpoint("opc.tcp://10.4.1.182:4840/freeopcua/server/")
    server.set_server_name("Example a24")
    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )

    uri = "http://monUri"
    idx = await server.register_namespace(uri)

    while True:
        await asyncio.sleep(0.1)

