"""Xiaomi Chuangmi camera (chuangmi.camera.ipc009) support."""
import click
import logging
from typing import Any, Dict

from miio.click_common import command, format_output
from miio.device import Device

_LOGGER = logging.getLogger(__name__)


class MyCameraStatus:
    """Container for status reports from the Xiaomi Chuangmi Camera."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Request:
        ["power"]
        Response:
        ["on"]
        """
        self.data = data

    @property
    def power(self) -> bool:
        """Camera power."""
        return self.data["power"] == "on"


    def __repr__(self) -> str:
        s = (
            "<CameraStatus "
            "power=%s>"
            % (
                self.power,
            )
        )
        return s

    def __json__(self):
        return self.data


class MyChuangmiCamera(Device):
    """Main class representing the Xiaomi Chuangmi Camera."""

    @command(
        default_output=format_output(
            "",
            "Power: {result.power}\n"
            "\n",
        )
    )
    def status(self) -> MyCameraStatus:
        """Retrieve properties."""
        properties = [
            "power",
        ]

        values = self.send("get_prop", properties)

        return MyCameraStatus(dict(zip(properties, values)))

    @command(default_output=format_output("Power on"))
    def on(self):
        """Power on."""
        return self.send("set_power", ["on"])

    @command(default_output=format_output("Power off"))
    def off(self):
        """Power off."""
        return self.send("set_power", ["off"])
