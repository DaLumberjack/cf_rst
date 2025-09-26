from homeassistant.components.switch import SwitchEntity

def setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return

    class CFSwitch(SwitchEntity):
        def __init__(self):
            self._attr_name = discovery_info["name"]
            self._attr_unique_id = discovery_info["command_topic"]
            self._attr_is_on = False
            self._command_topic = discovery_info["command_topic"]
            self._state_topic = discovery_info["state_topic"]

        async def async_added_to_hass(self):
            async def update(msg):
                self._attr_is_on = msg.payload == "ON"
                self.async_write_ha_state()

            await hass.components.mqtt.async_subscribe(self._state_topic, update)

        async def async_turn_on(self, **kwargs):
            await hass.components.mqtt.async_publish(self._command_topic, "ON")

        async def async_turn_off(self, **kwargs):
            await hass.components.mqtt.async_publish(self._command_topic, "OFF")

    add_entities([CFSwitch()])
