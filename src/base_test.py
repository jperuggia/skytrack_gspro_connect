# Initial test file to send data payload to gspro.
import logging
import yaml
import socket
import json
from golf_shot import BallData, ClubHeadData
from gsproconnect import GSProConnect
import pathlib


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
    SkyTrackConnect = GSProConnect(
        _cfg["device_id"],
        _cfg["units"],
        _cfg["gspro"]["api_version"],
        _cfg["club_data"],
    )

    # open tcp connection from config.
    SkyTrackConnect.init_socket(_cfg["gspro"]["ip_address"], _cfg["gspro"]["port"])

    _logger.info("Collecting Data from skytrack")
    # TODO: Connect to skytrack to get data from a shot and replace values. Need to validate
    # That the users device has a valid license for skytrack.
    _logger.info("Skytrack data obtained")

    # simulate a :BOMB:
    ball_data = BallData(
        ballspeed=166.8,
        spinaxis=-13.2,
        totalspin=2350.2,
        backspin=2350.2,
        sidespin=0.0,
        hla=0.0,
        vla=13.5,
        carry=300.0,
    )

    club_head_data = ClubHeadData()

    SkyTrackConnect.launch_ball(ball_data, club_head_data)

    #  Close this socket port.
    SkyTrackConnect.terminate_session()


if __name__ == "__main__":
    main()
