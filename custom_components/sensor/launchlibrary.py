"""
A component which allows you to get information about next launches.

For more details about this component, please refer to the documentation at
https://github.com/HalfDecent/HA-Custom_components/launchlibrary
"""
from datetime import timedelta
import requests
from homeassistant.helpers.entity import Entity

__version__ = '1.1.0'

ATTR_STREAM = 'stream'
ATTR_LAUNCH_NAME = 'launch_name'
ATTR_LAUNCH_TIMESTAMP = 'timestamp'
ATTR_AGENCY_NAME = 'agency'
ATTR_AGENCY_COUNTRY = 'agency_country_code'

SCAN_INTERVAL = timedelta(seconds=60)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the platform."""

    add_devices([LaunchSensor()])


class LaunchSensor(Entity):
    """The sensor class."""
    def __init__(self):
        """Initialize the sensor platform."""
        self.update()

    def update(self):
        """Update the sensor values."""
        baseurl = "https://launchlibrary.net/1.4/"
        fetchurl = baseurl + 'launch/next/1'
        launch = requests.get(fetchurl).json()['launches'][0]
        try:
            self._state = launch["windowstart"]
        except IndexError:
            self._state = None
        try:
            self._launchtimestamp = launch["wsstamp"]
        except IndexError:
            self._launchtimestamp = None
        try:
            self._launchname = launch["name"]
        except IndexError:
            self._launchname = None
        try:
            self._agencyname = (launch["location"]["pads"]
                                [0]["agencies"][0]["name"])
        except IndexError:
            self._agencyname = None
        try:
            self._agencycountry = launch["location"]["countryCode"]
        except IndexError:
            self._agencycountry = None
        try:
            self._launchstream = launch["vidURLs"][0]
        except IndexError:
            self._launchstream = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'nextlaunch'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return 'mdi:rocket'

    @property
    def device_state_attributes(self):
        """Return attributes of the sensor."""
        return {
            ATTR_LAUNCH_NAME: self._launchname,
            ATTR_LAUNCH_TIMESTAMP: self._launchtimestamp,
            ATTR_AGENCY_NAME: self._agencyname,
            ATTR_AGENCY_COUNTRY: self._agencycountry,
            ATTR_STREAM: self._launchstream,
        }
