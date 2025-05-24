from homeassistant.components.sensor import SensorEntity

def setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return

    class CFSensor(SensorEntity):
        def __init__(self):
            self._attr_name = discovery_info["name"]
            self._attr_unique_id = discovery_info["state_topic"]
            self._attr_native_unit_of_measurement = discovery_info.get("unit", "")
            self._attr_native_value = None

        async def async_added_to_hass(self):
            async def update(msg):
                self._attr_native_value = float(msg.payload)
                self.async_write_ha_state()
            await hass.components.mqtt.async_subscribe(discovery_info["state_topic"], update)

    add_entities([CFSensor()])
