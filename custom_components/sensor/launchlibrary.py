"""
A component which allows you to get information about next launches
For more details about this component, please refer to the documentation at
https://github.com/HalfDecent/HA-Custom_components/launchlibrary
"""
import requests
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.entity import Entity

ATTR_STREAM = 'stream'
ATTR_LAUNCH_NAME = 'launch_name'
ATTR_LAUNCH_TIMESTAMP = 'timestamp'
ATTR_AGENCY_NAME = 'agengy'
ATTR_AGENCY_COUNTRY = 'agengy_country_code'
ATTR_COMPONENT = 'component'
ATTR_COMPONENT_VERSION = 'component_version'

SCAN_INTERVAL = timedelta(seconds=60)

ICON = 'mdi:rocket'
COMPONENT_NAME = 'launchlibrary'
COMPONENT_VERSION = '1.0.1'

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([LaunchSensor()])

class LaunchSensor(Entity):
    def __init__(self):
        self._state = None
        self._launchtimestamp = None
        self._launchname = None
        self._agencyname = None
        self._agencycountry = None
        self._launchstream = None
        self._component = COMPONENT_NAME
        self._componentversion = COMPONENT_VERSION
        self.update()

    def update(self):
        baseurl = "https://launchlibrary.net/1.4/"
        fetchurl = baseurl + 'launch/next/1'
        launch = requests.get(fetchurl).json()['launches'][0]
        self._state = launch["windowstart"]
        self._launchtimestamp = launch["wsstamp"]
        self._launchname = launch["name"]
        self._agencyname = launch["location"]["pads"][0]["agencies"][0]["name"]
        self._agencycountry = launch["location"]["countryCode"]
        try:
            launch["vidURLs"][0]
        except Exception:
            self._launchstream = None
        else:
            self._launchstream = launch["vidURLs"][0]

    @property
    def name(self):
        return 'nextlaunch'

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return {
            ATTR_LAUNCH_NAME: self._launchname,
            ATTR_LAUNCH_TIMESTAMP: self._launchtimestamp,
            ATTR_AGENCY_NAME: self._agencyname,
            ATTR_AGENCY_COUNTRY: self._agencycountry,
            ATTR_STREAM: self._launchstream,
            ATTR_COMPONENT: self._component,
            ATTR_COMPONENT_VERSION: self._componentversion
        }