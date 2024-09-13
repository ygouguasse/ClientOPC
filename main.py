import asyncio
import logging

from asyncua import Client

class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("New data change event", node, val)

    def event_notification(self, event):
        print("New event", event)

async def main():
    url = "opc.tcp://10.4.1.145:4840"
    async with Client(url=url) as client:

        uri = "http://monURI"
        idx = await client.get_namespace_index(uri)
        myvert = await client.nodes.root.get_child("/Objects/2:LED1/2:Vert")
        mybleu = await client.nodes.root.get_child("/Objects/2:LED1/2:Blue")
        myrouge = await client.nodes.root.get_child("/Objects/2:LED1/2:Rouge")
        obj = await client.nodes.root.get_child("Objects/2:LED1")

        # subscribing to a variable node
        handler = SubHandler()
        sub = await client.create_subscription(10, handler)
        handle = await sub.subscribe_data_change(myvert)
        handle = await sub.subscribe_data_change(mybleu)
        handle = await sub.subscribe_data_change(myrouge)
        await asyncio.sleep(0.1)
        # we can also subscribe to events from server
        await sub.subscribe_events()

        # calling a method on server


        while True:
            await asyncio.sleep(1)
            print("Entrez votre commande")
            cmd = input()
            if(cmd == "red"):
                await myrouge.write_value(True)
            elif(cmd == "allumer"):
                await obj.call_method("2:methode_lumiere_allume")
            elif(cmd == "fermer"):
                await obj.call_method("2:methode")

if __name__ == "__main__":
    asyncio.run(main())

