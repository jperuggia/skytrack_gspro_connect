# Importing the relevant libraries
import websockets
import asyncio
import json
import time

# mimic what I think the garmin app would do on the phone.
# connec tto websocket and send the ball payload to websocket server.
# new "shot" is sent ever 30 seconds to test.
async def listen():
    url = "ws://127.0.0.3:9002"
    # Connect to the server
    counter = 0
    # while True:
    async with websockets.connect(url) as ws:
        while True:
            # print("sending a payload from the r10")
            # payload = f"PAYLOAD NAME {counter}"
            # counter += 1
            # await ws.send(payload)
            payload = {
                "BallSpeed": 147.5,
                "LaunchAngle": 14.3,
                "LaunchDirection": -0.7,
                "SpinAxis": -13.2,
                "TotalSpin": 3250.0,
            }
            print("sending payload")
            await ws.send(json.dumps(payload).encode("utf-8"))
            print("data sent")
            await asyncio.sleep(30)


# Start the connection
asyncio.get_event_loop().run_until_complete(listen())
