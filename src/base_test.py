import asyncio
import websockets
import os
import socket
from threading import Thread
import yaml
import json
import logging
import pathlib
from golf_shot import BallData, ClubHeadData
from gsproconnect import GSProConnect

# configure log.
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)
_logger = logging.getLogger(__file__)

_configuration = {}
_gspro_client = None


def load_base_config():
    config_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "config.yml")
    with open(config_path, "r") as f:
        try:
            _logger.info("Attempting to read configuration file")
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            _logger.exception(f"Error loading config file. {e}")
            raise e


async def garmin_socket_handler(websocket, path):
    while True:
        garmin_data = await websocket.recv()
        r_10_data = json.loads(garmin_data)
        ball_data = BallData(
            ballspeed=r_10_data["BallSpeed"],
            spinaxis=r_10_data["SpinAxis"],
            totalspin=r_10_data["TotalSpin"],
            hla=r_10_data["LaunchDirection"],
            vla=r_10_data["LaunchAngle"],
            # Optional values, just using defaults from docs
            backspin=2500.0,
            sidespin=-800.0,
            carry=256.5,
        )
        club_head_data = ClubHeadData()
        print("Sending ball data to gspro")
        _gspro_client.launch_ball(ball_data, club_head_data)


async def main():
    global _configuration
    _configuration = load_base_config()
    global _gspro_client
    _gspro_client = GSProConnect(
        _cfg["device_id"],
        _cfg["units"],
        _cfg["gspro"]["api_version"],
        _cfg["club_data"],
    )
    _gspro_client.init_socket(_cfg["gspro"]["ip_address"], _cfg["gspro"]["port"])

    ws_server_host = _cfg["garmin"]["ip_address"]
    ws_server_port = _cfg["garmin"]["port"]

    async with websockets.serve(garmin_socket_handler, ws_server_host, ws_server_port):
        await asyncio.Future()


if __name__ == "__main__":
    _cfg = load_base_config()
    asyncio.run(main())
