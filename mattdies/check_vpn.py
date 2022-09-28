"""Checks the connection of the machine to the Mullvad VPN."""

import json
import subprocess


class NotConnectedError(BaseException):
    """An exception class that represents the system not being connected to the VPN."""


def get_mullvad_status_json() -> dict:
    """Returns the Mullvad status JSON dict displaying connection status.

    Returns:
        dict: The Mullvad status JSON dict displaying connection status.
    """
    mullvad_check_url = "https://am.i.mullvad.net/json"
    subprocess_cmd = f"curl {mullvad_check_url}"
    result_stdout = subprocess.run(subprocess_cmd, check=True, shell=True, capture_output=True).stdout.decode()
    return json.loads(result_stdout)


def check_mullvad_status() -> bool:
    """Checks the Mullvad VPN connection status.

    Raises:
        NotConnectedError: Raises an error if the VPN is not connected.

    Returns:
        bool: A boolean representing whether the Mullvad VPN is connected.
    """
    mullvad_status = get_mullvad_status_json()
    exit_ip = bool(mullvad_status["mullvad_exit_ip"])
    exit_ip_hostname = mullvad_status["mullvad_exit_ip_hostname"] == "ch5-wireguard"
    connected = exit_ip and exit_ip_hostname
    if not connected:
        raise NotConnectedError("Not connected to the Mullvad VPN!")
    print(f"VPN connected! IP address: {mullvad_status['ip']}")
    return connected


if __name__ == "__main__":
    check_mullvad_status()
