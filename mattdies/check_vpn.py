"""Checks the connection of the machine to the Mullvad VPN."""

import json
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

from gen_funcs import path_parents  # pylint: disable=import-error

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NotConnectedError(BaseException):
    """An exception class that represents the system not being connected to the VPN."""


@dataclass
class VPN():
    """A class to store all operations related to the VPN."""

    def get_mullvad_status_json(self) -> dict:
        """Returns the Mullvad status JSON dict displaying connection status.

        Returns:
            dict: The Mullvad status JSON dict displaying connection status.
        """
        mullvad_check_url = "https://am.i.mullvad.net/json"
        subprocess_cmd = f"curl {mullvad_check_url}"
        result_stdout = subprocess.run(subprocess_cmd, check=True, shell=True, capture_output=True).stdout.decode()
        return json.loads(result_stdout)


    def get_vpn_hostname(self) -> str:
        """Gets the VPN hostname from a secrets file.

        Returns:
            str: The VPN hostname.
        """
        vpn_hostname_path = path_parents(Path(__file__))[1] / "secrets/vpn_hostname"
        with vpn_hostname_path.open("r",encoding="utf-8") as infile:
            return infile.read()


    def __post_init__(self):
        """Checks the VPN connection status."""
        mullvad_status = self.get_mullvad_status_json()
        vpn_hostname = self.get_vpn_hostname()
        exit_ip = bool(mullvad_status["mullvad_exit_ip"])
        exit_ip_hostname = mullvad_status["mullvad_exit_ip_hostname"] == vpn_hostname
        self.connected = exit_ip and exit_ip_hostname
        self.ip_address = mullvad_status["ip"]


def check_vpn_status() -> bool:
    """Checks the VPN connection status.

    Raises:
        NotConnectedError: Raises an error if the VPN is not connected.

    Returns:
        bool: A boolean representing whether the VPN is connected.
    """
    vpn = VPN()
    if not vpn.connected:
        raise NotConnectedError("Not connected to the Mullvad VPN!")
    logger.info("VPN connected! IP address: %s", vpn.ip_address)


if __name__ == "__main__":
    check_vpn_status()
