import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

@pytest.mark.asyncio
async def test_sensor_discovery(hass: HomeAssistant):
    # Simulate loading your custom component
    await async_setup_component(hass, "mqtt", {
        "mqtt": {
            "broker": "test.mosquitto.org"
        }
    })
    await async_setup_component(hass, "communifarm", {})

    # Simulate an incoming MQTT discovery message
    message = {
        "device_id": "cf-esp-01",
        "components": [{
            "type": "sensor",
            "sensor_type": "temperature",
            "name": "Test Temp",
            "state_topic": "cf/cf-esp-01/temp"
        }]
    }

    hass.async_create_task(
        hass.components.mqtt.async_publish("cf/discovery", json.dumps(message), 0, False)
    )
    await hass.async_block_till_done()

    # Verify that entity shows up
    assert "sensor.test_temp" in hass.states.async_entity_ids()
