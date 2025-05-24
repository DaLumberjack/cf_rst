from homeassistant.core import HomeAssistant
import json

DOMAIN = "communifarm"

async def async_setup(hass: HomeAssistant, config: dict):
    async def discovery_handler(msg):
        data = json.loads(msg.payload)
        device_id = data["device_id"]
        for comp in data["components"]:
            if comp["type"] == "sensor":
                hass.async_create_task(hass.helpers.discovery.async_load_platform(
                    "sensor", DOMAIN, comp, config))
            elif comp["type"] == "switch":
                hass.async_create_task(hass.helpers.discovery.async_load_platform(
                    "switch", DOMAIN, comp, config))

    await hass.components.mqtt.async_subscribe("cf/discovery", discovery_handler)
    return True
