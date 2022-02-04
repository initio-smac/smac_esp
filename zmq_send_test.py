from DEVICE.smac_client import client
import time
import uasyncio as asyncio

async def start():
    t1 = asyncio.create_task(client.main())
    t2 = asyncio.create_task(send())
    await t2
    #await client.initialize_zmq_connections()
    await t1

async def send():
    await asyncio.sleep(0)
    while 1:
        d = {}
        print("sending message: ", time.time())
        #client.send_message(frm="D1", to="#", cmd="g", message=d, tcp=True, udp=False )
        await asyncio.sleep(5)

asyncio.run(start())