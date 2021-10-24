# Initial test file to send data payload to gspro.
import logging
import yaml
import socket
import json
from golf_shot import BallData, ClubHeadData
from gsproconnect import GSProConnect
import pathlib
import time

# configure log.
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)
_logger = logging.getLogger(__file__)


def load_base_config():
    import os

    print(os.listdir())
    config_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "config.yml")
    with open(config_path, "r") as f:
        try:
            _logger.info("Attempting to read configuration file")
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            _logger.exception(f"Error loading config file. {e}")
            raise e


def main():
    # read base config file:
    _cfg = load_base_config()
    print(_cfg)

    # create GSPro Connect class for specific LM.
    R10Connect = GSProConnect(
        _cfg["device_id"],
        _cfg["units"],
        _cfg["gspro"]["api_version"],
        _cfg["club_data"],
    )
    # open tcp connection from config.
    R10Connect.init_socket(_cfg["gspro"]["ip_address"], _cfg["gspro"]["port"])
    # send a heartbeat?
    R10Connect.send_heartbeat()

    _logger.info("Connecting to Garmin R10")
    r10_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r10_socket.connect((_cfg["garmin"]["ip_address"], _cfg["garmin"]["port"]))

    old_sum_of_values = 0
    while True:
        r10_data = r10_socket.recv(8095)
        print(r10_data)
        # TODO: Parse this data to something useful. and put it here.
        ball_data = BallData(
            ballspeed=184.5,
            spinaxis=-1.0,
            # totalspin=2500.0,
            backspin=2200.0,
            sidespin=1.0,
            hla=1.0,
            vla=14.5,
            carry=312.5,
        )
        club_head_data = ClubHeadData()

        # TODO : Do something to see if there is new data. Sum , compare values etc.
        new_sum_of_values = 1000
        if new_sum_of_values != old_sum_of_values:
            R10Connect.launch_ball(ball_data, club_head_data)
            old_sum_of_values = new_sum_of_values

        # Delay for 30 seconds for now. Will remove when I can figure out what loop conditionals
        # to prevent endless sending of data and recv from r10.
        time.sleep(30)

    # R10Connect.terminate_session()


if __name__ == "__main__":
    main()
