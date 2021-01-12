import logging
from homeassistant.components.switch import SwitchDevice

from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN, )
from .my_camera import MyChuangmiCamera
from miio import Device, DeviceException
#from .helps import retry_async
_LOGGER = logging.getLogger(__name__)

#@retry_async(limit=1, delay=5, catch_exceptions=True)
async def async_setup_platform(hass, config, async_add_entities, _discovery_info=None):
    devices = []
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)    
    _LOGGER.info("Initializing Xiaomi camera with host %s (token %s...)", host, token[:5])
    
    camera = MyChuangmiCamera(host,token)
    switch = MyCameraSwitch(camera, name)
    devices.append(switch)
    async_add_entities(devices, False)
    _LOGGER.info("Init xiaomi camera success")

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the Xiaomi camera platform by config_entry."""
    return await async_setup_platform(
        hass,
        config_entry,
        async_add_devices,
        discovery_info=None)


class MyCameraSwitch(SwitchDevice):

    def __init__(self, camera, name):
        self._camera = camera
        self._name = name;

    @property
    def name(self):
        """Name of the device."""
        return self._name
    
    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._camera.status().power

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._camera.on()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._camera.off()
