import socket
import logging
from golf_shot import BallData, ClubHeadData

# configure log.
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)
_logger = logging.getLogger(__file__)


class GSProConnect:
    def __init__(self, device_id, units, api_version, club_data=False) -> None:
        self._device_id = device_id
        self._units = units
        self._api_version = api_version
        self._send_club_data = club_data

        self._socket = None
        self._shot_number = 0

    def init_socket(self, ip_address, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip_address, port))

    # TODO: Handle the response from GSPRO
    def launch_ball(self, ball_data: BallData, club_data: ClubHeadData = None) -> None:
        _logger.info("Sending data to GSPRO to launch ball")
        self._shot_number += 1
        _logger.info(f"Session Shot Number: {self._shot_number}")

        self._socket.sendall()

    # TODO: When script ends does socket auto close :shrug:
    def terminate_session(self):
        self._socket.close()

