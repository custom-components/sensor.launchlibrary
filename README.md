# custom_component to get info about next launches

![Version](https://img.shields.io/badge/version-1.0.1-green.svg?style=for-the-badge)

To get started:   
Put `/custom_components/sensor/launchlibrary.py` here:  
`<config directory>/custom_components/sensor/launchlibrary.py`  


Example configuration.yaml:  
```yaml
sensor:
  - platform: launchlibrary
```
 #### Sample overview
![Sample overview](overview.png)  
[Demo](https://ha-test-launchlibrary.halfdecent.io)

  

This component is using the [launchlibrary.net](http://launchlibrary.net/) API to get the information.